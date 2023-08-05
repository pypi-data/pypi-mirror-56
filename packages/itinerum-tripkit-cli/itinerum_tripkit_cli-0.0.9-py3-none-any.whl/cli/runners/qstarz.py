#!/usr/bin/env python
# Kyle Fitzsimmons, 2019
import click
import logging
import os
import pickle
import sys

from tripkit import TripKit
from tripkit.utils.misc import temp_path

logger = logging.getLogger('itinerum-tripkit-cli.runners.qstarz')


def setup(cfg):
    tripkit = TripKit(config=cfg)
    tripkit.setup(force=False)
    return tripkit


def load_users(tripkit, user_id):
    if user_id:
        logger.info(f'Loading user by ID: {user_id}')
        user = tripkit.load_user_by_orig_id(orig_id=user_id)
        if not user:
            click.echo(f'Error: Valid data for user {user_id} not found.')
            sys.exit(1)
        return [user]
    return tripkit.load_users()


def write_input_data(tripkit, user):
    tripkit.io.geojson.write_inputs(
        fn_base=user.uuid,
        coordinates=user.coordinates,
        prompts=user.prompt_responses,
        cancelled_prompts=user.cancelled_prompt_responses,
    )


def cache_prepared_data(tripkit, user):
    pickle_fp = temp_path(f'{user.uuid}.pickle')
    if not os.path.exists(pickle_fp):
        logger.debug('Pre-processing raw coordinates data to remove empty points and duplicates...')
        prepared_coordinates = tripkit.process.canue.preprocess.run(user.uuid, user.coordinates)
        with open(pickle_fp, 'wb') as pickle_f:
            pickle.dump(prepared_coordinates, pickle_f)
    with open(pickle_fp, 'rb') as pickle_f:
        logger.debug('Loading pre-processed coordinates data from cache...')
        prepared_coordinates = pickle.load(pickle_f)
    return prepared_coordinates


def detect_activity_locations(cfg, tripkit, user, prepared_coordinates, write_geo):
    logger.debug('Clustering coordinates to determine activity locations between trips...')
    locations = user.activity_locations
    if not locations:
        kmeans_groups = tripkit.process.clustering.kmeans.run(prepared_coordinates)
        delta_heading_stdev_groups = tripkit.process.clustering.delta_heading_stdev.run(prepared_coordinates)
        locations = tripkit.process.activities.canue.detect_locations.run(kmeans_groups, delta_heading_stdev_groups)
    if write_geo:
        tripkit.io.geojson.write_activity_locations(fn_base=user.uuid, locations=locations)
    return locations


def detect_trips(cfg, tripkit, user, prepared_coordinates, locations, write_geo, append_to=None):
    logger.debug('Detecting trips from GPS coordinates data...')
    user.trips = tripkit.process.trip_detection.canue.algorithm.run(cfg, prepared_coordinates, locations)
    tripkit.database.save_trips(user, user.trips)
    if write_geo:
        tripkit.io.geojson.write_trips(fn_base=user.uuid, trips=user.trips)
    trip_summaries = tripkit.process.trip_detection.canue.summarize.run(user, cfg.TIMEZONE)
    fn_base = append_to if append_to else user.uuid
    tripkit.io.csv.write_trip_summaries(fn_base=fn_base, summaries=trip_summaries, append=append_to)


def detect_complete_day_summaries(cfg, tripkit, user, append=False):
    logger.debug('Generating complete days summaries...')
    complete_day_summaries = tripkit.process.complete_days.canue.counter.run(user.trips, cfg.TIMEZONE)
    tripkit.database.save_trip_day_summaries(user, complete_day_summaries, cfg.TIMEZONE)
    tripkit.io.csv.write_complete_days({user.uuid: complete_day_summaries}, append=append)


def detect_activity_summaries(cfg, tripkit, user, locations, append=False):
    logger.debug('Generating dwell time at activity locations summaries...')
    activity = tripkit.process.activities.canue.tally_times.run(user, locations, cfg.ACTIVITY_LOCATION_PROXIMITY_METERS)
    activity_summaries = tripkit.process.activities.canue.summarize.run_full(activity, cfg.TIMEZONE)
    tripkit.io.csv.write_activities_daily(activity_summaries['records'], extra_cols=activity_summaries['duration_keys'], append=append)


def create_condensed_output(cfg, tripkit, user, prepared_coordinates, locations):
    logger.debug('Detecting trips from GPS coordinates data...')
    user.trips = tripkit.process.trip_detection.canue.algorithm.run(cfg, prepared_coordinates, locations)
    trip_summaries = tripkit.process.trip_detection.canue.summarize.run(user, cfg.TIMEZONE)
    complete_day_summaries = tripkit.process.complete_days.canue.counter.run(user.trips, cfg.TIMEZONE)
    tripkit.io.csv.write_condensed_activity_locations(user)
    tripkit.io.csv.write_condensed_trip_summaries(user, trip_summaries, complete_day_summaries)


@click.command()
@click.option('-u', '--user', 'user_id', help='The user ID to process a single user only.')
@click.option('-t', '--trips', 'trips_only', is_flag=True, help='Detect only trips for the given user(s).')
@click.option('-cd', '--complete-days', 'complete_days_only', is_flag=True, help='Detect only complete day summaries for the given user(s).')
@click.option('-a', '--activities', 'activity_summaries_only', is_flag=True, help='Detect only activities summaries for the given user(s).')
@click.option('-cn', '--condensed', 'condensed_output', is_flag=True, help='(QStarz only) Create a condensed output with a locations file, trips summaries, and aggregate survey summary.')
@click.option('-wi', '--write-inputs', is_flag=True, help='Write input .csv coordinates data to GIS format.')
@click.option('-wg', '--write-geo', is_flag=True, help='Write output GIS data for each user in survey.')
@click.pass_context
def run(ctx, user_id, trips_only, complete_days_only, activity_summaries_only, condensed_output, write_inputs, write_geo):
    if sum([trips_only, complete_days_only, activity_summaries_only, condensed_output]) > 1:
        click.echo('Error: Only one exclusive mode can be run at a time.')
        sys.exit(1)

    cfg = ctx.obj['config']
    cfg.INPUT_DATA_TYPE = 'qstarz'
    tripkit = setup(cfg)
    users = load_users(tripkit, user_id)
    append_fn_base = cfg.SURVEY_NAME if not user_id else None
    append_mode = user_id is None

    for user in users:
        if write_inputs:
            if len(users) > 1:
                click.echo('Warning: Multiple users selected, continue writing input data? (y/n)')
                sys.exit(1)
            write_input_data(tripkit, user)

        if trips_only:
            if not user.coordinates.count():
                click.echo(f'No coordinates available for user: {user.uuid}')
                sys.exit(1)
            prepared_coordinates = cache_prepared_data(tripkit, user)
            locations = detect_activity_locations(cfg, tripkit, user, prepared_coordinates, write_geo)
            detect_trips(cfg, tripkit, user, prepared_coordinates, locations, write_geo, append_to=append_fn_base)
        elif complete_days_only:
            if not user.trips:
                click.echo(f'No trips available for user: {user.uuid}')
                sys.exit(1)
            detect_complete_day_summaries(cfg, tripkit, user, append=append_mode)
        elif activity_summaries_only:
            if not user.trips:
                click.echo(f'No trips available for user: {user.uuid}')
                sys.exit(1)
            prepared_coordinates = cache_prepared_data(tripkit, user)
            locations = detect_activity_locations(cfg, tripkit, user, prepared_coordinates, write_geo)
            detect_activity_summaries(cfg, tripkit, user, locations, append=append_mode)
        elif condensed_output:
            prepared_coordinates = cache_prepared_data(tripkit, user)
            locations = detect_activity_locations(cfg, tripkit, user, prepared_coordinates, write_geo)
            create_condensed_output(cfg, tripkit, user, prepared_coordinates, locations)
        else:
            prepared_coordinates = cache_prepared_data(tripkit, user)
            locations = detect_activity_locations(cfg, tripkit, user, prepared_coordinates, write_geo)
            detect_trips(cfg, tripkit, user, prepared_coordinates, locations, write_geo, append_to=append_fn_base)
            if not user.trips:
                click.echo(f'No trips available for user: {user.uuid}')
                sys.exit(1)
            detect_complete_day_summaries(cfg, tripkit, user, append=append_mode)
            detect_activity_summaries(cfg, tripkit, user, locations, append=append_mode)

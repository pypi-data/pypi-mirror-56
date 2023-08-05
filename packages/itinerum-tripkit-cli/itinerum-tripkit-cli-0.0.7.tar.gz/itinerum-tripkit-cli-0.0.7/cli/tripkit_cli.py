#!/usr/bin/env python3
# Kyle Fitzsimmons, 2019
import click
import importlib.util
import logging
import os
import sys

from cli import runners


def dynamic_import(filepath, module_name):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# TODO: rename function
@click.command()
@click.option('-c', '--config', 'config_fp', default='./tripkit_config.py', help='A Python file of global variables to set processing parameters.')
@click.option('-v', '--verbose', is_flag=True, help='Enable info logging output to console.')
@click.option('-vv', '--very-verbose', is_flag=True, help='Enable debug logging output to console.')
@click.option('-u', '--user', 'user_id', help='The user ID to process a single user only.')
@click.option('-t', '--trips', 'trips_only', is_flag=True, help='Detect only trips for the given user(s).')
@click.option('-cd', '--complete-days', 'complete_days_only', is_flag=True, help='Detect only complete day summaries for the given user(s).')
@click.option('-a', '--activities', 'activity_summaries_only', is_flag=True, help='Detect only activities summaries for the given user(s).')
@click.option('-cn', '--condensed', 'condensed_output', is_flag=True, help='(QStarz only) Create a condensed output with a locations file, trips summaries, and aggregate survey summary.')
@click.option('-wi', '--write-inputs', is_flag=True, help='Write input .csv coordinates data to GIS format.')
@click.option('-wg', '--write-geo', is_flag=True, help='Write output GIS data for each user in survey.')
@click.pass_context
def main(ctx, config_fp, verbose, very_verbose, *ivk_args, **ivk_kwargs):
    '''
    The itinerum-tripkit-cli provides an interface for using the itinerum-tripkit processing library
    on Itinerum or QStarz .csv data.
    '''
    if not os.path.exists(config_fp):
        click.echo('Error: config could not be found.')
        sys.exit(1)
    cfg = dynamic_import(config_fp, 'tripkit_config')
    ctx.obj = {'config': cfg}

    logging.getLogger('peewee').setLevel(logging.INFO)  # mute peewee query debugs
    if verbose:
        logging.basicConfig(level=logging.INFO)
    if very_verbose:
        logging.basicConfig(level=logging.DEBUG)

    if cfg.INPUT_DATA_TYPE == 'itinerum':
        ctx.invoke(runners.itinerum.run, **ivk_kwargs)
    elif cfg.INPUT_DATA_TYPE == 'qstarz':
        ctx.invoke(runners.qstarz.run, **ivk_kwargs)
    else:
        click.echo(f'Data type {cfg.INPUT_DATA_TYPE} not recognized.')

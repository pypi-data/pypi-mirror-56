import sys
import logging
import json

import click

from .dbc_reader import read_dbc, init
from .c_generator import c_gen
from .gui import gui
from .validator import validate

def setup_logging():
    """ setup logging """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    handler = logging.FileHandler('fcp.log')
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

@click.command(name='read_dbc')
@click.argument('dbc')
@click.argument('json_file')
@click.argument('device_config')
def read_dbc_cmd(dbc, json_file, device_config):
    logger = setup_logging()
    read_dbc(dbc, json_file, device_config, logger)


@click.command(name='c-gen')
@click.argument('templates')
@click.argument('output')
@click.argument('json_file')
@click.argument('skel')
def c_gen_cmd(templates, output, json_file, skel):
    logger = setup_logging()
    c_gen(templates, output, json_file, skel, logger)

@click.command(name='init')
@click.argument('json_file')
def init_cmd(json_file):
    logger = setup_logging()
    init(json_file, logger)

@click.command(name='validate')
@click.argument('json_file')
def validate_cmd(json_file):
    logger = setup_logging()
    with open(json_file) as f:
        j = f.read()

    r, msg = validate(logger, json.loads(j))
    if r:
        print("JSON validated")
    else:
        print(msg)

@click.command(name='gui')
def gui_cmd():
    logger = setup_logging()
    gui(logger)


@click.group()
def main():
    pass

main.add_command(read_dbc_cmd)
main.add_command(c_gen_cmd)
main.add_command(init_cmd)
main.add_command(validate_cmd)
main.add_command(gui_cmd)

if __name__ == "__main__":
    main()

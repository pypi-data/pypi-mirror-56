import os
import logging
import configparser

import click

logger = logging.getLogger(__name__)
folder = click.get_app_dir("Pyborg")


def mk_folder():
    try:
        os.makedirs(os.path.join(folder, "brains"))
        os.makedirs(os.path.join(folder, "tmp"))
        logger.info("pyborg folder created.")
    except OSError:
        logger.info("pyborg folder already exists.")


def init_systemd(unit_file="pyborg_out.service", packager="poetry", command="pyborg http", wd=None):
    "setup systemd unit files for (new) pyborg prod deploys."
    config = configparser.ConfigParser()

    config["Unit"]['Description'] = "Pyborg multiplexing server"
    config["Unit"]['After'] = "network.target"
    if wd:
        config['Service']['WorkingDirectory'] = wd
    config['Service']['ExecStart'] = "{} run {}".format(packager, command)
    config['Service']['ExecReload'] = "/bin/kill -HUP $MAINPID"
    config['Service']['KillMode'] = "process"
    config['Service']['Restart'] = "on-failure"
    config['Service']['User'] = "pyborg"

    config["Install"]["WantedBy"] = "multi-user.target"
    with open(unit_file) as fp:
        config.write(fp)

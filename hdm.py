#!/usr/bin/env python

import os
import sys
import json
import subprocess
import socket
from optparse import OptionParser
from pathlib import Path

def print_error_msg(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(1)


def parse_arguments():
    parser = OptionParser()

    parser.add_option("-d", "--delete", action="store_true",
                      default=False,
                      help="Remove configurations")

    parser.add_option("-r", "--reload", action="store_true",
                      default=False,
                      help="Reload configurations")

    return parser.parse_args()


def stow(df_dir_path, home_dir_path, module):
    subprocess.run(f"stow {module} --dir={df_dir_path} --target={home_dir_path}",
                   shell=True, stdout=subprocess.PIPE)


def unstow(df_dir_path, home_dir_path, module):
    subprocess.run(f"stow -D {module} --dir={df_dir_path} --target={home_dir_path}",
                   shell=True, stdout=subprocess.PIPE)


def restow(df_dir_path, home_dir_path, module):
    subprocess.run(f"stow -R {module} --dir={df_dir_path} --target={home_dir_path}",
                   shell=True, stdout=subprocess.PIPE)

def ostow(df_dir_path, home_dir_path, module, options):
    if options.delete:
        unstow(df_dir_path, home_dir_path, module)
    elif options.reload:
        restow(df_dir_path, home_dir_path, module)
    else:
        stow(df_dir_path, home_dir_path, module)


def stow_all_in_dir(df_dir_path, home_dir_path, options):
    modules = next(os.walk(df_dir_path))[1]
    for module in modules:
        ostow(df_dir_path, home_dir_path, module, options)


def stow_with_cfg(df_dir_path, home_dir_path, options, cfg):
    hostname = socket.gethostname()
    target_all = cfg.get("*") or []
    target_cur = cfg.get(hostname) or []

    for module in target_all + target_cur:
        module_path = df_dir_path / module
        ostow(module_path.parent, home_dir_path, module_path.name, options)


def hdm():
    (options, args) = parse_arguments()

    if len(args) < 1:
        print_error_msg("Missing argument [DIRECTORY]")

    HOME_DIR = os.getenv('HOME')
    DOTFILE_DIR = args[0]

    home_dir = Path(HOME_DIR)
    df_dir = Path(DOTFILE_DIR)
    hdm_config_file = df_dir / "hdmrc.json"

    # Check if the passed argument is a directory
    if not df_dir.is_dir():
        print_error_msg(f"{DOTFILE_DIR} is not a directory.")

    # if hdmrc.json doesn't exist, perform a flat stow in df_dir
    if not hdm_config_file.is_file():
        flat_stow(df_dir, home_dir, options)
        sys.exit(0)

    # if hdmrc.json exists, parse it and stow
    with open(hdm_config_file) as hdm_cfg:
        cfg = json.load(hdm_cfg)
        stow_with_cfg(df_dir, home_dir, options, cfg)


if __name__ == "__main__":
    hdm()


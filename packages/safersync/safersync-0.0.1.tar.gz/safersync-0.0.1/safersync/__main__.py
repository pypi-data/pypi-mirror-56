#!/usr/bin/env python3

import argparse
import os
from .verify_dir import verifyDir
from .action_new import actionNew
from .action_start import actionStart

parser = argparse.ArgumentParser()

parser.add_argument("action", choices=["new", "start"], help="""
    Action to be done: `new`, for setting up a new backup configuration.
    `start`, to start a new backup operation. Both command requires specifying
    `--from` and `--to`, the `new` command checks and fixes everything required
    to map a source folder to destination, while the `start` will only start
    synchronisation when everything is okay.
""")

parser.add_argument("--src", "-s", type=str, required=True, help="""
    Source folder to be synchronised. Must be an existing folder.
""")

parser.add_argument("--dest", "-d", type=str, required=True, help="""
    Destination folder to be synchronised. Must be an existing folder.
""")

args = parser.parse_args()

## ---------------------------------------------------------------------------

srcdir = os.path.realpath(args.src)
dstdir = os.path.realpath(args.dest)

def error(s, code=1):
    print("Error: %s" % s)
    exit(code)

if not verifyDir(srcdir, assert_set_up=(args.action!="new")):
    error("Source dir does not exist.")

if not verifyDir(dstdir, assert_set_up=(args.action!="new")):
    error("Destination dir does not exist.")

if args.action == "new":
    actionNew(src=srcdir, dst=dstdir)
    exit()

if args.action == "start":
    actionStart(src=srcdir, dst=dstdir)
    exit()

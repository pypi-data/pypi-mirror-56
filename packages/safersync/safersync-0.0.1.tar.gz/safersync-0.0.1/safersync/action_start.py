#!/usr/bin/env python3

import os
import subprocess
from .userinput import choose
from .filenames import *
from .lockfile import FileLock
import time

def error(s, code=1):
    print("Error: %s" % s)
    exit(code)

def actionStart(src, dst):
    srcMarkerFile = os.path.join(src, SRC_MARKER_FILE)
    dstMarkerFile = os.path.join(dst, DST_MARKER_FILE)

    if not os.path.isfile(srcMarkerFile):
        error("Source folder is not set up for backup.", 10)

    if not os.path.isfile(dstMarkerFile):
        error("Destination folder is not set up for backup, or not connected yet.", 10)

    if open(srcMarkerFile, "r").read() != open(dstMarkerFile, "r").read():
        error("Backup source and destination MISMATCH, check twice!", 10)

    print("Acquiring lock on destination: %s" % dst)
    with FileLock(os.path.join(dst, DST_LOCK_FILE)) as lock:
        command = [
            "rsync",
            "--archive",
            "--verbose",
            #"--dry-run",
            "--exclude", ".srsync-*",
            src + "/",
            dst,
        ]
        print(" ".join(command))
        subprocess.run(command)

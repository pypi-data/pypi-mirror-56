#!/usr/bin/env python3

import os

def verifyDir(spec, assert_set_up=False):
    """Verify if a given specification for source or destination folder is
    valid."""
    if not os.path.isdir(spec): return False


    return True

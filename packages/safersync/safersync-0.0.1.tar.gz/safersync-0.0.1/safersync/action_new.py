#!/usr/bin/env python3

import os
from .userinput import choose
from .filenames import *

def actionNew(src, dst):
    srcMarkerFile = os.path.join(src, SRC_MARKER_FILE)
    dstMarkerFile = os.path.join(dst, DST_MARKER_FILE)

    initSrcMarker = False
    if os.path.isfile(srcMarkerFile): # TODO verify marker file size
        print("Source directory is already set to be backed up.")
        print("Do you want to re-initialize it?")
        print("This is NOT necessary if you just want to create a new backup!")
        if "y" == choose("Y-Yes / N-No, default: N", "yn", "n"):
            initSrcMarker = True
    else:
        initSrcMarker = True
        
    if initSrcMarker:
        print("Source directory is MARKED for back up.")
        open(srcMarkerFile, "w+").write(os.urandom(32).hex())

    srcMarkerContent = open(srcMarkerFile, "r").read()
    assert 64 == len(srcMarkerContent)


    initDstMarker = False
    if os.path.isfile(dstMarkerFile):
        dstMarkerContent = open(dstMarkerFile, "r").read()
        if srcMarkerContent == dstMarkerContent:
            print("The backup relationship")
            print(" FROM: %s" % src)
            print(" TO:   %s" % dst)
            print("already exists. Do nothing.")
            exit()
        else:
            print("Error: trying to overwrite mismatched backup destination!")
            print(" FROM: %s" % src)
            print(" TO:   %s" % dst)
            print("is set up for different backups!")
            print("Refusing to do anything. If you believe this is an error,")
            print("type [confirm to override] below.")
            x = input("Do you really want to override?   : ").lower()
            if not "confirm to override" in x:
                print("Abort.")
                exit()

            print("Destination is forced to be backup of given source path.")
            open(dstMarkerFile, "w+").write(srcMarkerContent)

    else:
        print("Trying to set up backup")
        print(" FROM: %s" % src)
        print(" TO:   %s" % dst)
        yn = choose("Is this correct? Y for yes, N for no.", "yn", default="n")
        if yn != "y":
            print("Abort.")
            exit()

        open(dstMarkerFile, "w+").write(srcMarkerContent)
        print("Backup set up.")

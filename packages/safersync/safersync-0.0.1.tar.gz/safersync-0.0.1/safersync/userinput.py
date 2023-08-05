#!/usr/bin/env python3

def choose(description, choices, default=""):
    choices = choices.lower()

    while True:
        try:
            action = input(description + "   : ").lower()
            if default != "" and default in choices and action == "":
                return default

            if len(action) == 1 and action in choices:
                return action
        except KeyboardInterrupt:
            print("User aborted input.")
            exit(2)

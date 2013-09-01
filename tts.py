import os
from pytts import pytts

def say(string):
    pytts().say(string)

def sayNB(string):
    pytts().sayNB(string)

if __name__ == "__main__":
    say("Look, it works! Even with 'apostrophes' and \"quotes\".")

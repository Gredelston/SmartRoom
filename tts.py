import os

def say(string):
    os.system('echo "%s" | festival --tts' % string)

say("Hello")
say("World")
say("Hello World")

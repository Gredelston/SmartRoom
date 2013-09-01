import os

def say(string):
    string = string.replace('"','')
    string = string.replace('\'','')
    os.system('echo "%s" | festival --tts' % string)

if __name__ == "__main__":
    say("Look, it works! Even with 'apostrophes' and \"quotes\".")
import pexpect
import os

class Player:
    
    def __init__(self, playIndex=None):
        """
        When the Player is instantiated, spawn pianobar in the terminal.
        If music defaults to playing, pause it and go to the station select screen.
        """

        # First things first, clear that pesky state config file.
        # Otherwise, pianobar will default to playing a station,
        # which just throws everything off.
        if os.path.isfile(os.path.expanduser("~" + "/.config/pianobar/state")):
            print "Clearing state config file."
            os.system("rm ~/.config/pianobar/state")

        # Spawn the Pianobar
        self.child = pexpect.spawn('pianobar')

        # Now that we're waiting for a station, get the station dict.
        self.updateStations()

        # Initialize a few variables up in this bitch.
        self.waitingForStation = True
        self.currentStationIndex = -1 # By convention, this means no station yet.
        self.playing = False



    def playByIndex(self, index):
        """
        Takes in the index of a station to be played, and plays that station.
        """

        # Make sure the index supplied is valid.
        if not self.validateIndex(index):
            print "ERROR: Please supply a valid station number!"
            return

        # Make sure we're waiting for station.
        if not self.waitingForStation:
            print 'Switching to station select.'
            self.child.send('s') # Change station
            self.waitingForStation = True
        else:
            print 'Already at station select.'

        self.child.sendline(str(index))
        self.playing = True
        self.waitingForStation = False
        self.currentStationIndex = int(index)

        print "Now playing station: " + self.indexDict[str(index)]

    def next(self):
        """
        Skips to the next track.
        """
        print 'Skipping track...'
        if self.waitingForStation:
            self.child.send('\n')
            self.waitingForStation = False
        self.child.send('n')

    def quit(self):
        """
        Exits gracefully from the Pianobar.
        """
        if self.waitingForStation:
            self.child.send('\n')
            self.child.expect('#')
            self.waitingForStation = False
            self.currentStationIndex = 0
        print "Exiting from Pandora player."
        self.child.sendline('q')

    def exit(self):
        self.quit()

    def validateIndex(self, index):
        """
        Returns True if index is a viable station index,
        and False if not.
        """
        return str(index) in self.indexDict.keys()

    def updateStations(self):
        """
        To be called whenever we reach the Station Select screen.
        Creates self.stationDict, which contains all stations:
        {stationTitle: stationIndex}
        and self.indexDict, which does it backward:
        {stationIndex: stationTitle}
        """

        self.child.expect('station:')

        lines = self.child.before.split('\r\n')
        stationList = [line for line in lines if "q" in line or "Q" in line]
        stationDict = {}
        indexDict = {}

        for i in stationList:
            name = " ".join(i.split()[3:])
            index = i.split()[1][:-1]
            stationDict[name] = index
            indexDict[index] = name

        self.stationDict = stationDict
        self.indexDict = indexDict



player = Player()
player.playByIndex(2)

import time
time.sleep(10)
print ''

player.playByIndex(4)

time.sleep(5)

player.next()

time.sleep(5)

player.quit()
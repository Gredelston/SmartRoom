import pexpect

class Player:
    
    def __init__(self, playIndex=None):
        """
        When the Player is instantiated, spawn pianobar in the terminal.
        By default, assume we don't want any music playing.
        This can be overridden with the optional argument playIndex.
        """

        self.child = pexpect.spawn('pianobar') # spawn the pianobar

        # We don't know whether it will start with a station already playing,
        # so allow for either situation
        i = self.child.expect(['#', 'Select station:'])

        if i==0: # Station is already playing.
            self.child.sendline('S') # Pause
            self.child.sendline('s') # Change station
            self.expect('Select station:')
        if i==1: # At station select screen.
            pass # everything is A-OK

        # Now that we're waiting for a station, get the station dict.
        self.updateStations()

        # If requested, play the specified station.
        if playIndex != None and isinstance(x, int):
            self.child.sendline(playIndex)
            self.waitingForStation = False
            self.currentStationIndex = playIndex
            self.playing = True
        else: # No station was requested
            self.waitingForStation = True
            self.currentStationIndex = -1
            self.playing = False

    def updateStations(self):
        """
        To be called whenever we reach the Station Select screen.
        Creates self.stationDict, which contains all stations:
        {stationTitle: stationIndex}
        """
        stationList = [i for i in self.child.before.split('\r\n') if "q" in i or "Q" in i]
        stationDict = {}
        for i in stationList:
            print "ITEM: " + i
            stationDict[" ".join(i.split()[3:])] = i.split()[1][:-1]
        print "Station dict: " , stationDict
        self.stationDict = stationDict

player = Player()

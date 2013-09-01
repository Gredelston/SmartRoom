import pexpect
import os

class Player:
    
    def __init__(self, playIndex=None):
        """
        When the Player is instantiated, spawn pianobar in the terminal.
        If music defaults to playing, pause it and go to the station select screen.
        """
        print 'Launching Pandora player...'

        # First things first, clear that pesky state config file.
        # Otherwise, pianobar will default to playing a station,
        # which just throws everything off.
        if os.path.isfile(os.path.expanduser("~" + "/.config/pianobar/state")):
            os.system("rm ~/.config/pianobar/state")

        # Spawn the Pianobar
        self.child = pexpect.spawn('pianobar')

        # Now that we're waiting for a station, get the station dict.
        self.updateStations()

        # Initialize a few variables up in this bitch.
        self.waitingForStation = True
        self.currentStationIndex = -1 # By convention, this means no station yet.
        self.playing = False

        self.track = None
        self.artist = None
        self.album = None


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
            self.child.send('s') # Change station
            self.waitingForStation = True
        else:
            pass

        self.child.sendline(str(index))
        self.playing = True
        self.waitingForStation = False
        self.currentStationIndex = int(index)
        self.currentStationName = self.indexDict[str(self.currentStationIndex)]

        print "Now playing station: " + self.indexDict[str(index)]

    def thumbsUp(self):
        """
        Thumbs up the current track.
        """
        self.updateTrack()
        print "Liked track " + self.track
        if self.waitingForStation:
            self.child.send('\n')
            self.waitingForStation = False
        self.child.send('+')

    def thumbsDown(self):
        """
        Thumbs down the current track.
        """
        self.updateTrack()
        print "Disliked track " + self.track
        if self.waitingForStation:
            self.child.send('\n')
            self.waitingForStation = False
        self.child.send('-')

    def next(self):
        """
        Skips to the next track.
        """
        print 'Skipping track...'
        if self.waitingForStation:
            self.child.send('\n')
            self.waitingForStation = False
        self.child.send('n')

    def updateTrack(self):
        """
        Figures out the name of the track currently playing.
        """
        # Flip through all the tracks that have happened since last time.
        newTrackFlag = False
        while True:
            i = self.child.expect(['\|>', pexpect.TIMEOUT], timeout=1)
            if i == 0: # Found another track
                newTrackFlag = True
            elif i == 1: # That was the last one!
                break

        # If this track is different from the old one,
        if newTrackFlag:
            # Get ["'Track', 'Name'", 'by', '"Artist', 'Name"', 'on', '"Album', 'Name"', '<3'?, '\xlb[2K']
            self.child.expect('#')
            wordList = self.child.before.split()

            hitByOn = 0
            trackList = []
            artistList = []
            albumList = []

            # parse that shit
            for i in range(len(wordList)):
                # if we're at the track
                if hitByOn == 0:
                    # if we're changing to the artist (happens at "by")
                    if i != 0 and (wordList[i-1][-1] == '"' and wordList[i] == 'by' and wordList[i+1][0] == '"'):
                        hitByOn = 1
                        continue
                    else:
                        trackList.append(wordList[i])

                # if we're at the artist
                elif hitByOn == 1:
                    # if we're changing to the album (happens at "on")
                    if wordList[i-1][-1] == '"' and wordList[i] == 'on' and wordList[i+1][0] == '"':
                        hitByOn = 2
                        continue
                    else:
                        artistList.append(wordList[i])

                # if we're at the album
                elif hitByOn == 2:
                    # if we're done
                    if wordList[i] == '<3' or i == len(wordList)-1:
                        break
                    else:
                        albumList.append(wordList[i])

            # Put that thing back where it came from, or so help me
            # (So help me! So help me!)
            self.track = " ".join(trackList)
            self.artist = " ".join(artistList)
            self.album = " ".join(albumList)


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

    def __str__(self):
        self.updateTrack()
        return 'Currently playing ' + self.track + " by " + self.artist + " on " + self.album


# Cool shit to show you that shit works!
if __name == "__main__":
    import time
    import tts

    player = Player()

    player.playByIndex(7)
    print player

    time.sleep(3)

    player.playByIndex(3)
    time.sleep(5)
    player.next()
    player.next()

    print player
    tts.say(player.__str__())

    time.sleep(5)

    player.quit()
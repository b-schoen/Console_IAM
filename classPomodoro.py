from classAlarm import Alarm
from classAlarm import QuickAlarm
from gtts import gTTS
import datetime
import subprocess
import sys
import time

class SmallPomo:

    #TODO: Import POMO Ratio

    #TODO: Import POMO score f(ratio * completed)

    #TODO: Pomo manager for multiple pomos in succession
    
    #TODO: Trailing pomos, ratio becomes more lopsided over time up to superbreak
    
    #TODO: Cleanup audio files
    
    #TODO: Optional: Generalize to N Pomos

    def __init__(self, workInterval, playInterval):
        
        self.workInterval = workInterval
        self.playInterval = playInterval
        
        self.start = datetime.datetime.now()
        
        #unique pomo ID by start time
        self.pomoID = str(self.start.hour) + "-" + str(self.start.minute)

        #set strings for the messages to say at each alarm
        
        self.workEndString = "Done working. You have " +str(workInterval)+ "minutes to play."
        
        self.playEndString = "Done playing."
        
        #create QuickAlarms to go off after the set intervals
        
        self.workEndAlarm = QuickAlarm(self.workEndString, workInterval)
        self.playEndAlarm = QuickAlarm(self.playEndString, workInterval+playInterval)
    
        #play start message to let user know pomo has begun
        
        self.playStartMessage()
    
    def playStartMessage(self):
        
        self.startWorkString = "Made it to a new Pomo. You have " + str(self.workInterval) + "minutes to work"

        tts = gTTS(text = self.startWorkString, lang="en")
        
        self.audio_file_name = "pomo_"+self.pomoID+".mp3"

        tts.save(self.audio_file_name)
        
        self.playAudioFile(self.audio_file_name)
        
    def playAudioFile(self, file_name):
        
        subprocess.Popen(['mplayer',file_name]).wait()
    
    def toAlarmFormat(self, hour, minute):
    
        alarmFormatted = str(hour)+":"+str(minute)
        
        return alarmFormatted

class MediumPomo:

    def __init__(self, workInterval, playInterval):
        
        #denotes how long work interval decreases for subsequent pomos
        #work interval is softened by the formula (workInterval*=softening_factor)
        #repeated for each pomo after the first
        self.softening_factor = 0.6666
        
        #create list for all pomos
        self.pomoList = []

        self.createPomo(0, workInterval,playInterval)
    
        #create an offset to indicate how long is between the start of the first and second pomo
        self.pomoOffset = workInterval+playInterval
        
        workInterval*=self.softening_factor
    
        self.createPomo(self.pomoOffset, workInterval - self.softening_factor, playInterval)

    def createPomo(self, delay, workInterval, playInterval):

        time.sleep(delay*60)

        #create a new Pomo and add it to the list
        self.pomoList.append(SmallPomo(workInterval,playInterval))

#class BigPomo:

class PomoManager:

    def __init__(self, workInterval, playInterval, smallMediumBig):
        
        #superbreak is the break taken after all pomos in manager are completed
        self.superbreak = workInterval+playInterval
        
        if(smallMediumBig == "small"):
            self.pomo = SmallPomo(workInterval, playInterval)
        
        if(smallMediumBig == "medium"):
            self.pomo = MediumPomo(workInterval, playInterval)

        self.waitForSuperbreak()
        
    def waitForSuperbreak(self):
        
        time.sleep(self.superbreak*60)
        
        self.startSuperbreak()
        
    def startSuperbreak(self):
        
        #create and play start superbreak message
        self.startSuperbreakString = "Made it to a superbreak! You have " + str(self.superbreak) + "minutes to take a break"
        
        tts = gTTS(text = self.startWorkString, lang="en")
        
        self.audio_file_name = "superbreak.mp3"
        
        tts.save(self.audio_file_name)
        
        self.playAudioFile(self.audio_file_name)
    
        #create alarm for end of superbreak
        
        self.superbreakEndString = "End of superbreak"
        
        self.superbreakEndAlarm = QuickAlarm(self.superbreakEndString, self.superbreak)
    
    def playAudioFile(self, file_name):
        
        subprocess.Popen(['mplayer',file_name]).wait()

if __name__ == "__main__":
    
    print("Started main")
    
    #mp = MediumPomo(15,10)

    #pm = PomoManager(15,10,"small")


                                  



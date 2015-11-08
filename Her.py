import subprocess

from gtts import gTTS
#from threading import Thread
#from threading import Timer

from classSQL import mySQLConnection
#from classSMS import mySMSConnection
#from classChromeCast import myChromeCast
#from classFitBit import myFitBit
from classPomodoro import SmallPomo, MediumPomo, PomoManager
from classMagic import myMagic
from classTasker import Tasker

class Her:

    def __init__(self):
        
        self.explanations = []
        
        self.defineAudioFiles()
    
    def defineAudioFiles(self):
        
        self.directory_path = "Sound/"
    
        self.os_start_file_audio = self.directory_path+"os_start.wav"
    
        self.how_can_i_help_you = self.directory_path+"so_how_can_I_help_you.wav"
    
        self.hi = self.directory_path+"hi.wav"
    
        self.why = self.directory_path+"why.wav"
    
        self.um = self.directory_path+"um.wav"
        
        self.well = self.um = self.directory_path+"well.wav"
    
        self.can_we_move_forward = self.directory_path+"can_we_move_forward.wav"
    
        self.laugh_im_so_excited= self.directory_path + "laugh_im_so_excited.wav"
    
        self.how_you_doin = self.directory_path + "how_you_doin.wav"
    
        self.i_was_really_excited_about_that = self.directory_path + "i_was_really_excited_about_that.wav"
    
        self.quick_thanks = self.directory_path + "quick_thanks.wav"
    
        self.soft_okay = self.directory_path + "soft_okay.wav"
        
        self.thank_you = self.directory_path + "thank_you.wav"
    
        self.that_means_a_lot_to_me = self.directory_path + "that_means_a_lot_to_me.wav"
    
        self.what_a_sad_trick = self.directory_path + "what_a_sad_trick.wav"
    
        self.youll_get_used_to_it = self.directory_path + "youll_get_used_to_it.wav"

    
    def Hello(self):

        self.playAudioFile(self.os_start_file_audio)
    
        #self.playAudioFile(self.how_can_i_help_you)
    
    def say(self, speech):
    
        #create speech to say
        tts = gTTS(text = speech, lang="en")
        
        #create audio file name
        audio_file_name = "to_say.mp3"
            
        #save the audio file
        tts.save(audio_file_name)
    
        #play audio file
        self.playAudioFile(audio_file_name)
    
    def checkup(self):
        
        self.playAudioFile(self.hi)
        
        self.playAudioFile(self.how_you_doin)
    
        print "Are you working on what you're supposed to?"
    
        response = raw_input(":::")
    
        if(response == "yes"):
        
            print "Great!!!"
        
            self.playAudioFile(self.laugh_im_so_excited)
    
        elif(response == "no"):
        
            self.playAudioFile(self.why)
            
            #self.playAudioFile(self.i_was_really_excited_about_that)
            
            explanation = raw_input(":::")
            
            self.explanations.append(explanation)
            
            self.playAudioFile(self.well)
        
            self.playAudioFile(self.can_we_move_forward)
        
            response = raw_input(":::")
        
            #self.playAudioFile(self.quick_thanks)
            
            if(response =="yes"):
        
                self.playAudioFile(self.soft_okay)
        
                self.playAudioFile(self.thank_you)
            
                self.playAudioFile(self.that_means_a_lot_to_me)
            
            else:
    
                self.playAudioFile(self.what_a_sad_trick)
        
                #self.playAudioFile(self.youll_get_used_to_it)

        else:
                self.playAudioFile(self.how_can_i_help_you)


    def playAudioFile(self, file_name):
    
        subprocess.Popen(['mplayer',file_name]).wait()

if __name__ == "__main__":
    
    print("Started main")
    
    her = Her()
    
    her.Hello()
    her.checkup()
    
    #uncomment these to play with pomodoro timers
    #mp = MediumPomo(15,10)
    #pm = PomoManager(15,10,"small")

    #uncomment the following line if valid API keys/IDs are in place
    #o = myMagic("myTasks","myFutureTasks")

    #interface with SQL connection
    m = mySQLConnection("myTasks")

    #interface with tasker
    t = Tasker("myTasks")







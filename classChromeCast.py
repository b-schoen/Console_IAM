from __future__ import print_function
import time
import pychromecast
from pychromecast.controllers.youtube import YouTubeController

class myChromeCast:
    
    #Leapcast?

    def __init__(self):
        
        self.ChromeCastName = "FILL"
        self.cast = pychromecast.get_chromecast(friendly_name=self.ChromeCastName)
    
        self.mc = self.cast.media_controller

    def playVideo(self, youtubeLink):
        
        self.quitApp()
        
        self.yt = YouTubeController()
        
        self.cast.register_handler(self.yt)
    
        self.yt.play_video(youtubeLink)

    def play(self):
    
        self.mc.play()

    def pause(self):

        self.mc.pause()

    def quitApp(self):

        self.cast.quit_app()

if __name__ == "__main__":
    
    print("Started main")

    c = myChromeCast()
from gtts import gTTS
from threading import Thread
import datetime
import sys
import time
import os
import subprocess

#TODO: Use args and kwargs to do "init overloading" instead of multiple classes
#			Can use len(args) to call either "QuickAlarm Contruct" function (not class) etc.

class Alarm:

	def __init__(self, task_string, time_string):

		print "Starting"

		self.time_string_list = time_string.split(":")

		self.alarmHour=self.time_string_list[0]
		self.alarmMinute=self.time_string_list[1]

		#to uniquely identify the audio file
		self.alarmID = self.alarmHour+"-"+self.alarmMinute

		#add greeting to text string
		task_string="Hey, time to "+task_string

		#create speech to say when alarm goes off
		tts = gTTS(text = task_string, lang="en")

		self.audio_file_name = "alarm_"+self.alarmID+".mp3"

		#save the audio file
		tts.save(self.audio_file_name)

		#start a thread monitoring for when it goes off
		self.monitorThread = Thread(target=self.monitorAlarm)
		self.hasntGoneOff = True
		self.monitorThread.start()
		#self.monitorThread.join()

	def monitorAlarm(self):

		while self.hasntGoneOff:

			#every minute, check if the hour and minute match
			time.sleep(60)

			##DEBUG
			print "Checking: "+self.alarmID

			now = datetime.datetime.now()

			print "Hi I'm alarm "+self.alarmID

			print "The time now is: "

			print now.hour
			print now.minute

			print "I go off at: "

			print self.alarmHour
			print self.alarmMinute

			print "Hour equality is: "
			print (now.hour == int(self.alarmHour))
			print "Minute equality is: "
			print (now.minute == int(self.alarmMinute))

			##END DEBUG

			#if the current time is equal to the alarm's time to go off, call the "go off" function
			if(now.hour == int(self.alarmHour) and now.minute == int(self.alarmMinute)):

				self.goOff()

				#clean up after the alarm goes off		
				self.cleanUp()

	def goOff(self):

		#stop the main look in monitorAlarm, allowing the function to finish and thus the thread to close
		self.hasntGoneOff=False

		#play created audio file
		self.playAudioFile(self.audio_file_name)

		print "I went off"
		print "---------------------"

	def cleanUp(self):

		#delete the previously created audio file
		os.remove(self.audio_file_name)

	def playAudioFile(self, file_name):

		subprocess.Popen(['mplayer',file_name]).wait()

class QuickAlarm:

	def __init__(self, taskName, time_from_now):

		self.currentTime = datetime.datetime.now()

		self.quickAlarmEnd = self.currentTime + datetime.timedelta(minutes=time_from_now)

		self.formattedQuickAlarmTime = self.toAlarmFormat(self.quickAlarmEnd.hour, self.quickAlarmEnd.minute)

		self.alarm = Alarm(taskName, self.formattedQuickAlarmTime)

	def toAlarmFormat(self, hour, minute):
    
		alarmFormatted = str(hour)+":"+str(minute)
        
		return alarmFormatted

class SuperQuickAlarm:

	def __init__(self, time_from_now):

		self.superQuickAlarm = QuickAlarm("Super Quick Alarm", time_from_now)

if __name__ == "__main__":

	print("Started main")

	a = Alarm("test me", "1:07")
	b = Alarm("test me too", "1:08")
	
	q = QuickAlarm("Testing",2)

	sq = SuperQuickAlarm(3)







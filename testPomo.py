from datetime import datetime
from classFitBit import myFitBit

f = myFitBit()

currentMinute = datetime.now().minute
currentHour = datetime.now().hour

#can make pomo class
pomoWork = 15
pomoRest = 10

#need to adjust for 51+10>60

f.setAlarm(currentHour, currentMinute+pomoWork)
f.setAlarm(currentHour, currentMinute+pomoWork+pomoRest)
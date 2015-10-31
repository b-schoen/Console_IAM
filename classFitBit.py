import fitbit
import datetime
import pytz

class myFitBit:

    def __init__(self):
        
        self.customer_key = 'FILL'
        
        self.customer_secret = 'FILL'
        
        self.user_key = 'FILL'
        
        self.user_secret = 'FILL'
        
        self.authd_client = fitbit.Fitbit(self.customer_key, self.customer_secret, resource_owner_key=self.user_key, resource_owner_secret=self.user_secret)
        
        self.device_ID = FILL
        
        self.authd_client.sleep()

    def getDevices(self):

        return self.authd_client.get_devices()

    def getAlarms(self):

        return self.authd_client.get_alarms(self.device_ID)

    def setAlarm(self, hour, minute):
        
        hour=int(hour)
        minute=int(minute)
        
        #Set specifically to Los Angeles time zone
        hour+=7
    
    
        alarm_time = datetime.datetime(2015, 1, 1, hour, minute, 0, 0, pytz.UTC)
        week_days = []

        self.authd_client.add_alarm(self.device_ID,alarm_time,week_days)

if __name__ == "__main__":
    
    print("Started main")
    
    f = myFitBit()
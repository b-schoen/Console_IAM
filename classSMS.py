import smtplib
import textmagic.client
from Queue import Queue

class mySMSConnection:

    def __init__(self):
        
        self.server = smtplib.SMTP( "smtp.gmail.com", 587 )
        self.server.starttls()
        self.server.login( 'FILL', 'FILL' )
    
        self.client = textmagic.client.TextMagicClient('FILL', 'FILL')
    
        self.receivedMessages = Queue()

    def send(self, message):

        self.server.sendmail( 'FILL', 'FILL', '%s' % (message))

    def receive(self):
        
        #12069396420

        response = self.client.receive("0")
        for message in response['messages']:
            
            #from_number = message['from']
            #text = message['text']
            #id = message['message_id']

            #self.printSMS(from_number,text, id)
            
            self.receivedMessages.put(message)

            self.remove(message)

    def getMostRecentMessage(self):
    
        return self.receivedMessages.get()

    def remove(self, message):
        
        self.client.delete_reply(message['message_id'])
    
    def clearMostRecent(self):
        
        response = self.client.receive("0")
        for message in response['messages']:
            
            self.remove(message)



    def printSMS(self, from_number, text, id):

        print "From: " + str(from_number)
        print "Received: " + str(text)
        print "With ID: " + str(id)

#TODO: Quickalarms in 15,30,45 mins

if __name__ == "__main__":
    
    print("Started main")
    
    do = mySMSConnection()


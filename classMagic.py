from classSQL import mySQLConnection
from classSMS import mySMSConnection
#from classChromeCast import myChromeCast
#from classFitBit import myFitBit
from classPomodoro import SmallPomo, MediumPomo, PomoManager

class myMagic:
    
    #TODO: Catch exceptions so these don't die

    def __init__(self,nowTable,futureTable):
        
        self.nowTable = nowTable
        self.futureTable = futureTable

        self.nowSQL = mySQLConnection(nowTable)
        
        self.futureSQL = mySQLConnection(futureTable)
        
        self.mySMS = mySMSConnection()
    
        #self.myCast = myChromeCast()
    
        #self.myFit = myFitBit()
        
    def startListening(self):
    
        while(True):
            
            self.mySMS.receive()

            if(not self.mySMS.receivedMessages.empty()):

                recentMessage = self.mySMS.getMostRecentMessage()
                
                #print recentMessage['text']

                self.process(recentMessage)


    def process(self, recentMessage):

        content = recentMessage['text']

        parsed_content = content.split()
        
        print "Received content: " + str(content)
        
        #insert command
        if parsed_content[0] == "Insert" and len(parsed_content) > 2:
            
            self.nowSQL.insert(str(parsed_content[1]), str(parsed_content[2]))

        #remove command
        elif parsed_content[0] == "Remove" and len(parsed_content) > 1:
    
            self.nowSQL.remove(str(parsed_content[1]))

        #done command
        elif parsed_content[0] == "Done" and len(parsed_content) > 1:
    
            self.nowSQL.done(str(parsed_content[1]))

        #getList command
        elif parsed_content[0] == "List" and len(parsed_content) > 0:
    
            self.sendList(self.nowTable)

        #insert in future command
        elif parsed_content[0] == "Future" and len(parsed_content) > 0:
    
            self.futureSQL.insert(str(parsed_content[1]), str(parsed_content[2]))

    def sendList(self, table):
        
        if(table == self.nowTable):
            
            list_in_sql_format = self.nowSQL.retrieveList()
        
        elif(table == self.futureTable):
        
            list_in_sql_format = self.futureSQL.retrieveList()
        
        else:
        
            print("Error, no such table to list")
        
        text=""

        for row in list_in_sql_format:

            text += str(row[1])+" "+str(row[0])+"\n"

        self.mySMS.send(text)

    def pomo(self, workInterval, playInterval, smallMediumBig):

        self.myPomoManager = PomoManager(workInterval,playInterval,smallMediumBig)

    def alarm(self, *args):

        if(len(args)==3):
        
            print "yay 3 args"

        else:
            print "Error, this function only accepts 1, 2, or 3 args."

    def now(self):
    
        self.nowSQL.listall()

    def future(self):

        self.futureSQL.listall()



if __name__ == "__main__":
    
    print("Started main")
    
    o = myMagic("myTasks","myFutureTasks")



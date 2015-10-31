
import sqlite3
from termcolor import colored

class mySQLConnection:

    def __init__(self, table):

        self.connection = sqlite3.connect("tasks.db")
        self.cursor = self.connection.cursor()

        self.table = table

        #define sql queries
        #priorities are defined by color Red,Orange,Black,Done
        self.getRedPriority = """SELECT * FROM "%s" WHERE priority=2""" % (self.table)
        self.getOrangePriority = """SELECT * FROM "%s" WHERE priority=1""" % (self.table)
        self.getBlackPriority = """SELECT * FROM "%s" WHERE priority=0""" % (self.table)
        self.getDonePriority = """SELECT * FROM "%s" WHERE priority=-1""" % (self.table)

        self.getInPriorityOrder_LowHigh = """SELECT * FROM "%s" ORDER BY priority""" % (self.table)
        self.getInPriorityOrder_HighLow = """SELECT * FROM "%s" ORDER BY priority DESC""" % (self.table)

        self.getRandom = """SELECT * FROM "%s" WHERE priority!=-1 ORDER BY RANDOM() LIMIT 1""" % (self.table)
        self.getRandomHighPriority = """SELECT * FROM "%s" WHERE priority>=2 ORDER BY RANDOM() LIMIT 1""" % (self.table)
        self.getRandomBlack ="""SELECT * FROM "%s" WHERE priority=0 ORDER BY RANDOM() LIMIT 1""" % (self.table)

        self.getTopPriority ="""SELECT * FROM "%s" ORDER BY priority DESC LIMIT 1""" % (self.table)

        self.removeDoneItems = """DELETE FROM "%s" WHERE priority=-1""" % (self.table)

        self.REMOVEALL = """DELETE FROM "%s" """ % (self.table)

    def insert(self, taskName, priority):
        
    	taskName=str(taskName)
    	priority=int(priority)
    	sql_command = """INSERT INTO "%s" (taskName, priority) VALUES ("%s", "%s");""" % (self.table,taskName,priority)
        self.executeAndSave(sql_command)
    
    def remove(self, taskName):
        
        taskName=str(taskName)
        sql_command="""DELETE FROM "%s" WHERE taskName="%s" """ % (self.table,taskName)
        self.executeAndSave(sql_command)

    def done(self, taskName):

        #if it exists, mark it as done
        if(self.exists(taskName)):
            taskName=str(taskName)
            sql_command="""UPDATE "%s" SET priority = -1 WHERE taskName = "%s" """ % (self.table,taskName)
            self.executeAndSave(sql_command)
        #if not, insert it then (recursively) mark it as done
        else:
            self.insert(taskName,0)
            self.done(taskName)

    def exists(self, taskName):

        self.checkIfExists = """SELECT EXISTS(SELECT 1 FROM "%s" WHERE taskName="%s" LIMIT 1)""" % (self.table,taskName)

        result = self.retrieveSingleResult(self.checkIfExists)

        doesExist = result[0][0]

        return doesExist

    def display(self,color): 

    	color=str(color)

    	if color == "red":
    		self.displayResults(self.getRedPriority)
    	if color == "orange":
    		self.displayResults(self.getOrangePriority)
    	if color == "black":
    		self.displayResults(self.getBlackPriority)
        if color == "done":
            self.displayResults(self.getDonePriority)

    def listall(self):
        
    	self.displayResults(self.getInPriorityOrder_HighLow)

    def highlight(self, taskName):

    	#doesn't have to get, but more organized

    	sql_command = """SELECT * FROM "%s" WHERE taskName="%s" """ % (self.table,taskName)

    	self.cursor.execute(sql_command)

    	result = self.cursor.fetchall()

        desired = str(result[0][0])

        desired = self.myFormat(desired)

        print colored(desired, 'blue', attrs=['reverse'])

    def light(self, *args):

        #generalized highlight

        for arg in args:

            self.highlight(arg)

    def highlightList(self, taskName):

        #get highlighted
        sql_command = """SELECT * FROM "%s" WHERE taskName="%s" """ % (self.table,taskName)

    	self.cursor.execute(sql_command)

    	result = self.cursor.fetchall()

        desired = str(result[0][0])

        #get list
        rows = self.retrieveList()

        #display
        self.displayHeader()

        for row in rows:

            if(row[0] == desired):
                text = str(row[1])+"          "+str(row[0])
                text = self.myFormat(text)
                print colored(text, 'blue', attrs=['reverse', 'blink'])
            else:
                text = str(row[1])+"          "+str(row[0])
                text = self.myFormat(text)
                self.printByPriority(text,int(row[1]))

    def top(self):

        self.cursor.execute(self.getTopPriority)

        result = self.cursor.fetchall()

        desired = str(result[0][0])

        desired = self.myFormat(desired)

        print colored(desired, 'red', attrs=['reverse', 'blink'])

    def topList(self):

        #get top
        result = self.retrieveSingleResult(self.getTopPriority)

        desired = str(result[0][0])

        #get list
        rows = self.retrieveList()

        #display
        self.displayHeader()

        for row in rows:

            if(row[0] == desired):
                text = str(row[1])+"          "+str(row[0])
                text = self.myFormat(text)
                print colored(text, 'red', attrs=['reverse', 'blink'])
            else:
                text = str(row[1])+"          "+str(row[0])
                text = self.myFormat(text)
                self.printByPriority(text,int(row[1]))

    def random(self):

        self.cursor.execute(self.getRandom)

        result = self.cursor.fetchall()

        desired = str(result[0][0])

        desired = self.myFormat(desired)

        print colored(desired, 'cyan', attrs=['reverse', 'blink'])

    def randomHigh(self):

        #get random high priority task
        result = self.retrieveSingleResult(self.getRandomHighPriority)

        desired = str(result[0][0])

        print colored(desired, 'magenta', attrs=['reverse'])

    def randomList(self):

        #get random
        result = self.retrieveSingleResult(self.getRandom)

        desired = str(result[0][0])

        #get list
        rows = self.retrieveList()

        #display
        self.displayHeader()

        for row in rows:

            if(row[0] == desired):
                text = str(row[1])+"          "+str(row[0])
                text = self.myFormat(text)
                print colored(text, 'cyan', attrs=['reverse', 'blink'])
            else:
                text = str(row[1])+"          "+str(row[0])
                text = self.myFormat(text)
                self.printByPriority(text,int(row[1]))

    def executeAndSave(self, sql_command):
        
        self.cursor.execute(sql_command)
        self.connection.commit()

    def retrieveList(self):

        self.cursor.execute(self.getInPriorityOrder_HighLow)

        result = self.cursor.fetchall()

        return result

    def retrieveSingleResult(self, query):

        self.cursor.execute(query)

        result = self.cursor.fetchall()

        return result

    def displayHeader(self):

        print "---------------------------------------------"
        print self.headerFormat(self.table)
        print "---------------------------------------------"
        print "priority     taskName"
        print "---------------------------------------------"

    def displayResults(self, query):

        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        self.displayHeader()

        for row in rows:

            text = str(row[1])+"          "+str(row[0])
            text = self.myFormat(text)
            self.printByPriority(text,int(row[1]))
    
    def printByPriority(self, string, priority):

            string = self.myFormat(string)

            if priority == 2:
                print colored (string, "red")
            elif priority == 1:
                print colored (string, "yellow")
            elif priority == 0:
                print string
            elif priority == -1:
                print colored(string, "green", attrs=['reverse'])
            else:
                print colored(string, "magenta")

    def myFormat(self, string):

        result = '{0: <40}'.format(string)

        return result    

    def headerFormat(self, string):

        result = '{0: <45}'.format(string)

        colored_result = colored(result, 'blue', attrs=['reverse'])

        return colored_result

    def clearScreen(self):

        for x in xrange(12):
            print('\n')

    def clearDone(self):

        self.executeAndSave(self.removeDoneItems)

    def clearTable(self):

    	decision = raw_input("Are you sure you want to do this? (yes/no): ")

    	if(decision == "yes"):

    		self.executeAndSave(self.REMOVEALL)

    	else:

    		print "Aborted"

if __name__ == "__main__":

    print("Started main")

    m = mySQLConnection("myTasks")

    #TODO: Write script to do this

    #currently: python -i runSQL.py



import sqlite3
import subprocess
import time
from termcolor import colored

#TODO: Return from field for general case of want field Y from field X

class mySQLConnection:

    def __init__(self, table):

        self.connection = sqlite3.connect("tasks.db")
        self.cursor = self.connection.cursor()

        self.table = table

        #define positions in entries
        self.id_position = 0
        self.taskName_position = 1
        self.priority_position = 2

        #define priority values
        self.magentaValue = 5          #critically past due
        self.redValue = 4              #critically due soon
        self.orangeValue = 3           #actually due at some point soon
        self.cyanValue = 2             #actually due at some point in future
        self.blueValue = 1             #time matters
        self.blackValue = 0            #build
        self.doneValue = -1            #done

        #define sql queries -------------------------------------------------------------------------

        self.getAllColoredPriority = """SELECT * FROM "%s" WHERE priority>"%s" ORDER BY priority DESC""" % (self.table, self.blackValue)
        self.getHighPriority = """SELECT * FROM "%s" WHERE priority>="%s" ORDER BY priority DESC""" % (self.table, self.redValue)
        self.getRedPriority = """SELECT * FROM "%s" WHERE priority="%s" """ % (self.table, self.redValue)
        self.getOrangePriority = """SELECT * FROM "%s" WHERE priority="%s" """ % (self.table, self.orangeValue)
        self.getBlackPriority = """SELECT * FROM "%s" WHERE priority="%s" """ % (self.table, self.blackValue)
        self.getDonePriority = """SELECT * FROM "%s" WHERE priority="%s" """ % (self.table, self.doneValue)

        #not done
        self.getNotDonePriority = """SELECT * FROM "%s" WHERE priority!="%s" ORDER BY priority DESC """ % (self.table, self.doneValue)
        self.getNotDoneReverse = """SELECT * FROM "%s" WHERE priority!="%s" ORDER BY priority """ % (self.table, self.doneValue)
        self.getNotDoneRandom = """SELECT * FROM "%s" WHERE priority!="%s" ORDER BY RANDOM() """ % (self.table, self.doneValue)

        self.getInRandomOrder = """SELECT * FROM "%s" ORDER BY RANDOM()""" % (self.table)
        self.getInPriorityOrder_LowHigh = """SELECT * FROM "%s" ORDER BY priority""" % (self.table)
        self.getInPriorityOrder_HighLow = """SELECT * FROM "%s" ORDER BY priority DESC""" % (self.table)

        self.getRandom = """SELECT * FROM "%s" WHERE priority!="%s" ORDER BY RANDOM() LIMIT 1""" % (self.table, self.doneValue)
        self.getRandomHighPriority = """SELECT * FROM "%s" WHERE priority>="%s" ORDER BY RANDOM() LIMIT 1""" % (self.table,self.redValue)
        self.getRandomColored = """SELECT * FROM "%s" WHERE priority>"%s" ORDER BY RANDOM() LIMIT 1""" % (self.table,self.blackValue)
        self.getRandomBlack ="""SELECT * FROM "%s" WHERE priority="%s" ORDER BY RANDOM() LIMIT 1""" % (self.table, self.blackValue)
       

        self.getTopPriority ="""SELECT * FROM "%s" ORDER BY priority DESC LIMIT 1""" % (self.table)

        self.removeDoneItems = """DELETE FROM "%s" WHERE priority="%s" """ % (self.table, self.doneValue)

        self.REMOVEALL = """DELETE FROM "%s" """ % (self.table)
    
        #create table -------------------------------------------------------------------------------------
        
        #creates table if none exists
        self.createTable()

    #Basic functions -----------------------------------------------------
    
    def createTable(self):
    
        self.createTableWithName = """CREATE TABLE IF NOT EXISTS "%s" (ID INT PRIMARY KEY, taskName VARCHAR, priority INT);""" % self.table
        self.executeAndSave(self.createTableWithName)

    def insert(self, taskName, priority):
      
    	sql_command = """INSERT INTO "%s" (taskName, priority) VALUES ("%s", "%s");""" % (self.table,taskName,priority)
        self.executeAndSave(sql_command)
    
    def remove(self, taskName):
        
        sql_command="""DELETE FROM "%s" WHERE taskName="%s" """ % (self.table,taskName)
        self.executeAndSave(sql_command)

    def update(self, taskName, priority):

        sql_command = """UPDATE "%s" SET priority="%s" WHERE taskName="%s" """ % (self.table,priority,taskName)
        self.executeAndSave(sql_command)

    def done(self, taskName):

        #if it exists, mark it as done
        if(self.exists(taskName)):
            taskName=str(taskName)
            sql_command="""UPDATE "%s" SET priority = "%s" WHERE taskName = "%s" """ % (self.table,self.doneValue,taskName)
            self.executeAndSave(sql_command)
        #if not, insert it then (recursively) mark it as done
        else:
            self.insert(taskName,self.doneValue)

    def exists(self, taskName):

        self.checkIfExists = """SELECT EXISTS(SELECT 1 FROM "%s" WHERE taskName="%s" LIMIT 1)""" % (self.table,taskName)

        result = self.retrieveSingleResult(self.checkIfExists)

        doesExist = int(result[0][0])

        return doesExist

    def display(self,color): 

    	color=str(color)

        if color == "high":
    		self.displayResults(self.getHighPriority)
    	elif color == "red":
    		self.displayResults(self.getRedPriority)
    	elif color == "orange":
    		self.displayResults(self.getOrangePriority)
    	elif color == "black":
    		self.displayResults(self.getBlackPriority)
        elif color == "done":
            self.displayResults(self.getDonePriority)

    #Basic id based functions --------------------------------------------

    #just find entry using task_id then call normal functions

    def removeid(self, task_id):
        
        entry = self.entry_from_id(task_id)

        my_taskName = entry[self.taskName_position]

        self.remove(my_taskName)

    def updateid(self, task_id, priority):

        entry = self.entry_from_id(task_id)

        my_taskName = entry[self.taskName_position]

        self.update(my_taskName, priority)

    def doneid(self, task_id):

        entry = self.entry_from_id(task_id)

        my_taskName = entry[self.taskName_position]

        self.done(my_taskName)

    def lightid(self, *task_ids):

        taskNames = []

        for task_id in task_ids:        

            entry = self.entry_from_id(task_id)

            my_taskName = entry[self.taskName_position]

            formatted = self.stringFormat(my_taskName)

            print colored(formatted, 'blue', attrs=['reverse'])

    #Listing -----------------------------------------------------

    def listall(self):

        self.clearScreen()
        
    	self.displayResults(self.getInPriorityOrder_HighLow)

    def listrev(self):

        self.clearScreen()

        self.displayResults(self.getNotDoneReverse)

    def listrand(self):

        self.clearScreen()

        self.displayResults(self.getNotDoneRandom)

    def listdone(self):

        self.clearScreen()

        self.displayResults(self.getDonePriority)

    def listrem(self):

        self.clearScreen()

        self.displayResults(self.getNotDonePriority)

    def listreal(self):

        self.clearScreen()

        self.displayResults(self.getAllColoredPriority)

    def listhigh(self):

        self.clearScreen()

        self.displayResults(self.getHighPriority)

    def highlight(self, taskName):

    	#doesn't have to get, but more organized

    	sql_command = """SELECT * FROM "%s" WHERE taskName="%s" """ % (self.table,taskName)

    	self.cursor.execute(sql_command)

    	result = self.cursor.fetchall()

        desired = str(result[0][self.taskName_position])

        desired = self.stringFormat(desired)

        print colored(desired, 'blue', attrs=['reverse'])

    def light(self, *taskNames):

        #generalized highlight

        for taskName in taskNames:

            if(self.exists(taskName)):

                self.highlight(taskName)

            else:

                self.insert(taskName,self.blackValue)
        
                self.highlight(taskName)

    def highlightList(self, taskName):

        #get highlighted
        sql_command = """SELECT * FROM "%s" WHERE taskName="%s" """ % (self.table,taskName)

    	self.cursor.execute(sql_command)

    	result = self.cursor.fetchall()

        desired = str(result[0][self.taskName_position])

        #get list
        rows = self.retrieveList()

        #display
        self.displayHeader()

        for row in rows:

            if(row[self.taskName_position] == desired):
                text = self.myFormat(row)
                print colored(text, 'blue', attrs=['reverse', 'blink'])
            else:
                text = self.myFormat(row)
                self.printByPriority(row)

    def top(self):

        self.cursor.execute(self.getTopPriority)

        result = self.cursor.fetchall()

        desired = str(result[0][self.taskName_position])

        desired = self.stringFormat(desired)

        print colored(desired, 'red', attrs=['reverse', 'blink'])

    def topList(self):

        #get top
        result = self.retrieveSingleResult(self.getTopPriority)

        desired = str(result[0][self.taskName_position])

        #get list
        rows = self.retrieveList()

        #display
        self.displayHeader()

        for row in rows:

            if(row[self.taskName_position] == desired):
                text = self.myFormat(row)
                print colored(text, 'red', attrs=['reverse', 'blink'])
            else:
                self.printByPriority(row)

    def random(self):

        self.cursor.execute(self.getRandom)

        result = self.cursor.fetchall()

        desired = str(result[0][self.taskName_position])

        desired = self.stringFormat(desired)

        print colored(desired, 'cyan', attrs=['reverse', 'blink'])

    def randomHigh(self):

        #get random high priority task
        result = self.retrieveSingleResult(self.getRandomHighPriority)

        desired = str(result[0][self.taskName_position])

        print colored(desired, 'magenta', attrs=['reverse'])

    def randomList(self):

        #get random
        result = self.retrieveSingleResult(self.getRandom)

        desired = str(result[0][self.taskName_position])

        print desired

        #get list
        rows = self.retrieveList()

        #display
        self.displayHeader()

        for row in rows:

            if(row[self.taskName_position] == desired):
                text = self.myFormat(row)
                print colored(text, 'cyan', attrs=['reverse', 'blink'])
            else:
                self.printByPriority(row)

    def grab(self, numberToGrab):

        self.clearScreen()

        #grab 'numberToGrab' many non-zero priority tasks
        sql_command = """SELECT * FROM "%s" WHERE priority>"%s" ORDER BY RANDOM() LIMIT "%s" """ % (self.table,self.blackValue,numberToGrab)
        
        self.displayResults(sql_command)

    #Execute -----------------------------------------------------

    def executeAndSave(self, sql_command):
        
        self.cursor.execute(sql_command)
        self.connection.commit()

    #Retrieve -----------------------------------------------------


    #retrieve generic query results

    def retrieveList(self):

        self.cursor.execute(self.getInPriorityOrder_HighLow)

        result = self.cursor.fetchall()

        return result

    def retrieveSingleResult(self, query):

        self.cursor.execute(query)

        result = self.cursor.fetchall()

        return result

    def retrieveResult(self, query):

        self.cursor.execute(query)

        result = self.cursor.fetchall()

        return result

    #return named result of specific type
    #TODO: Alter print so easily switchable between return and print (the other functions should return)

    def returnRandomColored(self):

        self.cursor.execute(self.getRandomColored)

        result = self.cursor.fetchall()

        desired = str(result[0][self.taskName_position])

        return desired

    #return entry from field

    def entry_from_id(self, task_id):

        sql_command = """SELECT * FROM "%s" WHERE ID = "%s" """ % (self.table, task_id)

        result = self.retrieveSingleResult(sql_command)

        return result[0]

    def entry_from_name(self, taskName):

        sql_command = """SELECT * FROM "%s" WHERE taskName = "%s" """ % (self.table, taskName)

        result = self.retrieveSingleResult(sql_command)

        return result[0]

    #return field from another field

    def priority_from_name(self, taskName):

        sql_command = """SELECT * FROM "%s" WHERE taskName = "%s" """ % (self.table,taskName)

        result = self.retrieveSingleResult(sql_command)

        desired = result[0]

        priority = desired[self.priority_position]

        return priority

    #Display -----------------------------------------------------

    def displayHeader(self):

        print "------------------------------------------------------------------------------------"
        print self.headerFormat(self.table)
        print "------------------------------------------------------------------------------------"
        print "priority    taskName                                                      ROW ID    "
        print "------------------------------------------------------------------------------------"

    def displayResults(self, query):

        self.cursor.execute(query)

        rows = self.cursor.fetchall()

        self.displayHeader()

        for row in rows:

            self.printByPriority(row)
    
    def printByPriority(self, row):

            string = self.myFormat(row)

            priority = int(row[self.priority_position])

            text = self.colorString(string, priority)

            print text

    def colorString(self, string, priority):

        if priority == self.redValue:
            text = colored (string, "red")
        elif priority == self.orangeValue:
            text = colored (string, "yellow")
        elif priority == self.cyanValue:
            text = colored (string, "cyan")
        elif priority == self.blueValue:
            text = colored (string, "blue")
        elif priority == self.blackValue:
            text = string
        elif priority == self.doneValue:
            text = colored(string, "green", attrs=['reverse'])
        else:
            text = colored(string, "magenta")

        return text

    def reversedColorString(self, string, priority):

        text = self.colorString(string,priority)

        text = colored(text, attrs=['reverse'])

        return text

    def stringFormat(self, string):

        result = '{: <40}'.format(string)

        return result

    def myFormat(self, row):

        my_id = str(row[self.id_position])
        my_taskName = str(row[self.taskName_position])
        my_priority = str(row[self.priority_position])

        result = '{: <10}  {: <60}  {:<10}'.format(my_priority,my_taskName,my_id)

        return result    

    def headerFormat(self, string):

        result = '{: <84}'.format(string)

        colored_result = colored(result, 'blue', attrs=['reverse'])

        return colored_result

    #Clear -----------------------------------------------------

    def clearScreen(self):

        for x in xrange(20):
            print('\n')

    def clearDone(self):

        self.executeAndSave(self.removeDoneItems)

    def clearTable(self):

    	decision = raw_input("Are you sure you want to do this? (yes/no): ")

    	if(decision == "yes"):

    		self.executeAndSave(self.REMOVEALL)

    	else:

    		print "Aborted"

    #Alter -----------------------------------------------------

    def shiftTable(self, value):

        #shift table priority values by this value (except for done)
        sql_command = """UPDATE "%s" SET priority = priority + "%s" WHERE priority!="%s" """ % (self.table, value,self.doneValue)
        self.executeAndSave(sql_command)


    #Alert -----------------------------------------------------

    def alert(self, results):

        #generate alerts for sql objects (using notify-send)

        for result in results: 

            time.sleep(0.2)
        
            result_string = str(result[self.taskName_position])+"\n"+ str(result[self.priority_position])

            #in milliseconds
            display_time = str(60000)

            subprocess.Popen(['notify-send','-t',display_time,result_string])

    def alertHigh(self):

        results = self.retrieveResult(self.getHighPriority)

        self.alert(results)

if __name__ == "__main__":

    print("Started main")

    m = mySQLConnection("myTasks")

    #TODO: Write script to do this

    #currently: python -i runSQL.py

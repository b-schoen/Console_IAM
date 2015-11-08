import sqlite3
import time
import datetime

from termcolor import colored

from classSQL import mySQLConnection

#TODO: Start with breaks? (makegrab option)

#TODO: Can create notifications at start and end of blocks
#TODO: Impliment "Extend" functionality, where prompted (for priority
#        > black?) and can extend by 10 minutes, add 5 minutes to break
#TODO: Superbreak structure

#TODO: Find a way to generalize now so can be modular (if not included make own?)
#       Until fixed, none can use any other sequentially (b/c each must set now)

#TODO: Add "final"

class Tasker:

    def __init__(self, table):

        self.table=table

        self.sqlConnection = mySQLConnection(table)

        #smallest time step (unit)
        self.unit_delta = 5
        self.unit_interval = datetime.timedelta(minutes=self.unit_delta)

        #the %I forces 12 hour time
        self.time_format = "%I:%M"

        #multiples of unit_interval
        self.default_work_factor = 4
        self.default_break_factor = 1
        self.default_start_factor = 1

        self.default_number_of_items = 2

    #create a task plan for that single task
    def make(self, taskName):

         priority = self.sqlConnection.priority_from_name(taskName)

         now = self.next_round_time()

         now = self.display_task_interval(now, taskName, priority)

         now = self.display_break_interval(now)

         now = self.display_start_interval(now)

    def makenow(self, taskName):

         priority = self.sqlConnection.priority_from_name(taskName)

         now = datetime.datetime.now()

         now = self.display_task_interval(now, taskName, priority)

         now = self.display_break_interval(now)

         now = self.display_start_interval(now)

    def makemult(self, *taskNames):

        #this should just be a for do self.make(taskName)

        now = self.next_round_time()

        for taskName in taskNames:

            priority = self.sqlConnection.priority_from_name(taskName)

            now = self.display_task_interval(now, taskName, priority)

            now = self.display_break_interval(now)

            now = self.display_start_interval(now)

    def makegrab(self, numberOfItems):

        #create tuple of taskNames

        taskNames = []

        for x in range(0, numberOfItems):

            taskName = self.sqlConnection.returnRandomColored()
            taskNames.append(taskName)

        self.makemult(*taskNames)

    #def breakfirst(self, numberOfItems

    #for use if done early (starts with a break then back started)
    def early(self):

        #TODO: Still need to fix time wise
        #       This problem is recurring (when want to break apart or start non standard)

        now = self.next_round_time()

        self.makegrab(self.default_number_of_items)

#Display intervals --------------------------------------------------------------------------

    def display_task_interval(self, datetime_obj, taskName, priority):

        for x in range(0,self.default_work_factor):

            display_string = self.format_datetime(datetime_obj) + " " + taskName

            text = self.sqlConnection.colorString(display_string,priority)

            print text

            datetime_obj = self.add_interval(datetime_obj)

        return datetime_obj

    def display_break_interval(self, datetime_obj):

        for x in range(0,self.default_break_factor):

            display_string = self.format_datetime(datetime_obj) + " " + "----Break"

            print display_string

            datetime_obj = self.add_interval(datetime_obj)

        return datetime_obj

    def display_start_interval(self, datetime_obj):

        for x in range(0,self.default_start_factor):

            display_string = self.format_datetime(datetime_obj) + " " + "--Start"

            print display_string

            datetime_obj = self.add_interval(datetime_obj)

        return datetime_obj


#Display general entries and format --------------------------------------------------------- 

    #display next hour in unit_interval intervals
    def display_next_hour(self):

        now = self.next_round_time()

        for x in range(0,12):

            self.display(now)

            now = self.add_interval(now)

    #display formatted datetime_obj  
    def display(self, datetime_obj):
        
        print self.format_datetime(datetime_obj)
  
    def format_datetime(self, datetime_obj):

        formatted_datetime_obj = datetime_obj.strftime(self.time_format)

        return formatted_datetime_obj

#Modify time ----------------------------------------------------------------

    def add_interval(self, datetime_obj):

        datetime_obj += self.unit_interval

        return datetime_obj

    def next_round_time(self):

        now = datetime.datetime.now()

        now=self.round_time(now)

        return now

    #round time up to nearest unit_interval
    def round_time(self, datetime_obj):

        overage = int(datetime_obj.minute) % self.unit_delta

        distance_to_round = self.unit_delta - overage

        round_timedelta = datetime.timedelta(minutes=distance_to_round)

        datetime_obj += round_timedelta

        return datetime_obj

#Notifications -------------------------------------------------------------

    def notifyMe(self, message, delay):

        #TODO: Notifications that are cross platform (is coloring?)
        print "In progress"

if __name__ == "__main__":

    myTasker = Tasker("myTasks")

    myTasker.display_next_hour()

from datetime import datetime
from database import Database

class TaskManager:
    def __init__(self):
        self.db = Database("profile.db")
        self.allProfiles = []
        self.allDeadlines = []
        self.allIDs = []
        self.allTasks = []
        self.allDueDeadlines = []
        self.allReminders = []
        self.allDueReminders = []

    def setAllDueDeadlines(self):
        self.allDeadlines.clear()
        self.allIDs.clear()
        self.allTasks.clear()
        self.allDueDeadlines.clear()
        self.allProfiles = self.db.fetchIDs()
        
        for self.x in self.allProfiles:
            self.allProfileTasks = self.db.fetchTasks(str(self.x)[2:-3])
            for self.y in self.allProfileTasks:
                self.allDeadlines.append(self.db.getDeadline(str(self.x)[2:-3], str(self.y)[2:-3]))
                self.allIDs.append(str(self.x)[2:-3])
                self.allTasks.append(str(self.y)[2:-3])

        if len(self.allDeadlines) == 0:
            self.allDueDeadlines.clear()
        else:
            for index, self.z in enumerate(self.allDeadlines):
                try:
                    newDeadline = datetime.strptime(str(self.z)[2:-3], "%d/%m/%Y %I:%M %p")
                    if newDeadline <= datetime.now():
                        self.allDueDeadlines.append(newDeadline)
                        self.allDueDeadlines.append(self.allTasks[index])
                        self.allDueDeadlines.append(self.allIDs[index])
                except:
                    pass

    def getAllDueDeadlines(self):
        self.setAllDueDeadlines()
        return self.allDueDeadlines

    def setAllDueReminders(self):
        self.allReminders.clear()
        self.allIDs.clear()
        self.allTasks.clear()
        self.allDueReminders.clear()
        self.allProfiles = self.db.fetchIDs()

        for self.x in self.allProfiles:
            self.allProfileTasks = self.db.fetchTasks(str(self.x)[2:-3])
            for self.y in self.allProfileTasks:
                self.allReminders.append(self.db.getReminder(str(self.x)[2:-3], str(self.y)[2:-3]))
                self.allIDs.append(str(self.x)[2:-3])
                self.allTasks.append(str(self.y)[2:-3])

        if len(self.allReminders) == 0:
            self.allDueReminders.clear()
        else:
            for index, self.z in enumerate(self.allReminders):
                try:
                    newReminder = datetime.strptime(str(self.z)[2:-3], "%d/%m/%Y %I:%M %p")
                    if newReminder <= datetime.now():
                        self.allDueReminders.append(newReminder)
                        self.allDueReminders.append(self.allTasks[index])
                        self.allDueReminders.append(self.allIDs[index])
                except:
                    pass

    def getAllDueReminders(self):
        self.setAllDueReminders()
        return self.allDueReminders

    
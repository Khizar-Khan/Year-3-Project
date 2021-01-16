from datetime import datetime
import threading

from database import Database

#deadline = "01012099"
#deadlineObj = datetime.strptime(deadline, "%d%m%Y")

class TaskManager:
    def __init__(self):
        self.db = Database("profile.db")

    def setDeadlineTimer(self, id, task):
        def deadlineTimerSet():
            while True:
                if self.deadline < datetime.now():
                    print("DEADLINE: " + task)
                    return

        self.deadline = datetime.strptime(str(self.db.getDeadline(id, task))[2:-3], "%d/%m/%Y %I:%M %p")
        threading.Thread(target=deadlineTimerSet).start()
import sqlite3
import uuid

class Database:
    def __init__(self, databaseName):
        # Connect to database
        self.conn = sqlite3.connect(databaseName)

        # Create cursor
        self.c = self.conn.cursor()

        # Create table
        self.c.execute("CREATE TABLE IF NOT EXISTS profiles (id text, name text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS tasks (id text, task text, deadline TEXT, reminder TEXT, important INTEGER, description TEXT)")

        # Commit
        self.conn.commit()

    # Profiles
    def fetchProfileNames(self):
        self.c.execute("SELECT name FROM profiles")
        profileNames = self.c.fetchall()
        return profileNames

    def fetchIDByName(self, name):
        self.c.execute("SELECT id FROM profiles WHERE name=?", (name,))
        profileID = self.c.fetchall()
        return profileID

    def fetchIDs(self):
        self.c.execute("SELECT id FROM profiles")
        ids = self.c.fetchall()
        return ids

    def fetchProfileById(self, id):
        self.c.execute("SELECT name FROM profiles WHERE id=?", (id,))
        profileID = self.c.fetchone()
        return profileID

    def insertProfile(self, name):
        id = str(uuid.uuid4())
        self.c.execute("INSERT INTO profiles (id, name) VALUES (?,?)", (id, name))
        self.conn.commit()

    def removeProfile(self, id):
        self.c.execute("DELETE FROM profiles WHERE id=?", (id,))
        self.conn.commit()

    def updateProfile(self, name, id):
        self.c.execute("UPDATE profiles SET name=? WHERE id=?", (name, id))
        self.conn.commit()
        
    # Tasks
    def fetchTasks(self, id):
        self.c.execute("SELECT task FROM tasks WHERE id = ?", (id,))
        tasks = self.c.fetchall()
        return tasks

    def insertTask(self, id, task):
        self.c.execute("INSERT INTO tasks (id, task, deadline, reminder, important, description) VALUES (?,?,0,0,0,?)", (id, task,""))
        self.conn.commit()

    def removeTask(self, id, task):
        self.c.execute("DELETE FROM tasks WHERE id=? AND task=?", (id, task))
        self.conn.commit()

    def removeTasks(self, id):
        self.c.execute("DELETE FROM tasks WHERE id=?", (id,))
        self.conn.commit()

    def setTaskDetail(self, id, task, whichDetail, setDetail):
        if whichDetail == 1:
            self.c.execute("UPDATE tasks SET deadline=? WHERE id=? AND task=?", (setDetail, id, task))
            self.conn.commit()
            pass
        elif whichDetail == 2:
            self.c.execute("UPDATE tasks SET reminder=? WHERE id=? AND task=?", (setDetail, id, task))
            self.conn.commit()
            pass
        elif whichDetail == 3:
            self.c.execute("UPDATE tasks SET description=? WHERE id=? AND task=?", (setDetail, id, task))
            self.conn.commit()
        elif whichDetail == 4:
            self.c.execute("UPDATE tasks SET important=? WHERE id=? AND task=?", (setDetail, id, task))
            self.conn.commit()
            pass
        else:
            return

    def getIfTaskImportant(self, id, task):
        self.c.execute("SELECT important FROM tasks WHERE id=? AND task=?", (id, task))
        important = self.c.fetchone()
        return important

    def getDeadline(self, id, task):
        self.c.execute("SELECT deadline FROM tasks WHERE id=? AND task=?", (id, task))
        deadline = self.c.fetchone()
        return deadline

    def getReminder(self, id, task):
        self.c.execute("SELECT reminder FROM tasks WHERE id=? AND task=?", (id, task))
        reminder = self.c.fetchone()
        return reminder

    def getTaskDescription(self, id, task):
        self.c.execute("SELECT description FROM tasks WHERE id=? AND task=?", (id, task))
        taskDescription = self.c.fetchall()
        return taskDescription
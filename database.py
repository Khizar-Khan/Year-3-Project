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
        self.c.execute("CREATE TABLE IF NOT EXISTS tasks (id text, task text)")

        # Commit
        self.conn.commit()

    # Profiles
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

    # Tasks
    def fetchTasks(self, id):
        self.c.execute("SELECT task FROM tasks WHERE id = ?", (id,))
        tasks = self.c.fetchall()
        return tasks

    def insertTask(self, id, task):
        self.c.execute("INSERT INTO tasks (id, task) VALUES (?,?)", (id, task))
        self.conn.commit()

    def removeTask(self, id, task):
        self.c.execute("DELETE FROM tasks WHERE id=? AND task=?", (id, task))
        self.conn.commit()

    def removeTasks(self, id):
        self.c.execute("DELETE FROM tasks WHERE id=?", (id,))
        self.conn.commit()
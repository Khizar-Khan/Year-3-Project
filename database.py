import sqlite3

class db:
    def __init__(self, databaseName):
        # Connect to database
        self.conn = sqlite3.connect(databaseName)

        # Create cursor
        self.c = self.conn.cursor()

        # Create table
        self.c.execute("CREATE TABLE IF NOT EXISTS profiles (name text)")
        self.c.execute("CREATE TABLE IF NOT EXISTS tasks (name text, task text)")

        # Commit
        self.conn.commit()

    # Profiles
    def fetchProfiles(self):
        self.c.execute("SELECT * FROM profiles")
        names = self.c.fetchall()
        return names

    def insertProfile(self, name):
        self.c.execute("INSERT INTO profiles VALUES (?)", (name,))
        self.conn.commit()

    def removeProfile(self, name):
        self.c.execute("DELETE FROM profiles WHERE name=?", (name,))
        self.conn.commit()

    # Tasks
    def fetchTasks(self, name):
        self.c.execute("SELECT task FROM tasks WHERE name = ?", (name,))
        tasks = self.c.fetchall()
        return tasks

    def insertTask(self, name, task):
        self.c.execute("INSERT INTO tasks (name, task) VALUES (?,?)", (name, task))
        self.conn.commit()

    def removeTask(self, name, task):
        self.c.execute("DELETE FROM tasks WHERE name=? AND task=?", (name, task))
        self.conn.commit()

    def removeTasks(self, name):
        self.c.execute("DELETE FROM tasks WHERE name=?", (name,))
        self.conn.commit()
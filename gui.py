#-------IMPORTS-------#
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database import db

import re
#---------END---------#


#------VARIABLES------#
windowHeight = 600
windowWidth = 700
maxWindowMultiplier = 1.25

taskButtonColour = "yellow"

db = db("profile.db")
profiles = db.fetchProfiles()
#---------END---------#


#------FUNCTIONS------#
def profileWindow():
    def createProfile():
        profileName = re.sub('[\W_]+', '', input.get())
        if len(profileName) > 0:
            db.insertProfile(profileName)
        else:
            messagebox.showinfo("Information", "Enter name to create a profile!")

        profiles = db.fetchProfiles()
        profileCombo.config(values=profiles)
        if len(profiles) == 1:
            profileCombo.current(0)

        profileWindow.destroy()
        refreshTaskList()

    def deleteProfile():
        profileName = profileCombo.get()
        db.removeProfile(profileName)
        db.removeTasks(profileName)

        profiles = db.fetchProfiles()
        if len(profiles) != 0:
            profileCombo.config(values=profiles)
            profileCombo.current(0)
        else:
            profileCombo.config(values=[""])
            profileCombo.current(0)

        profileWindow.destroy()
        refreshTaskList()

    profileWindow = tk.Toplevel()
    profileWindow.minsize(350,150)
    profileWindow.maxsize(350,150)
    profileWindow.title("Profile Details")

    input = tk.Entry(profileWindow)
    input.pack()

    createProfileButton = tk.Button(profileWindow, text="Create Profile", command=createProfile)
    createProfileButton.pack()

    deleteProfileButton = tk.Button(profileWindow, text="Delete Profile", command=deleteProfile)
    deleteProfileButton.pack()

def addTaskWindow():
    def addTask():
        if len(input.get()) > 0:
            taskText = input.get()
        else:
            messagebox.showinfo("Information", "Enter a task!")
            addTaskWindow.destroy()
            return
            
        currentNames = db.fetchProfiles()
        for x in currentNames:
            if str(x)[2:-3] == profileCombo.get(): 
                db.insertTask(profileCombo.get(), taskText)
                refreshTaskList()
                addTaskWindow.destroy()
                return

        addTaskWindow.destroy()
        messagebox.showinfo("Information", "Create/Select a valid profile first!")

    addTaskWindow = tk.Toplevel()
    addTaskWindow.minsize(350,150)
    addTaskWindow.maxsize(350,150)
    addTaskWindow.title("Add Task")

    input = tk.Entry(addTaskWindow)
    input.pack()

    addTaskButton = tk.Button(addTaskWindow, text="Add Task", command=addTask)
    addTaskButton.pack()

def removeTask():
    taskText = str(taskList.get("anchor"))
    db.removeTask(profileCombo.get(), taskText)
    refreshTaskList()

def selectedCombo(event):
    refreshTaskList()

def refreshTaskList():
    taskList.delete(0,"end")
    dbTaskList = db.fetchTasks(profileCombo.get())
    for item in dbTaskList:
        taskList.insert("end", str(item)[2:-3])
#---------END---------#


#------SETTINGS------#
root = tk.Tk()
root.minsize(windowHeight, windowWidth)
root.maxsize(int(windowHeight*maxWindowMultiplier), int(windowWidth*maxWindowMultiplier))
root.title("Family Organiser")
root.iconphoto(True, tk.PhotoImage(file="Images/Icon.png"))
root.geometry(str(windowHeight)+"x"+str(windowWidth))
#---------END---------#


#-----COMPONENTS-----#
# User profile section
userFrame = tk.Frame(root, bg="#cce6ff")
userFrame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.05)

# Combobox
if len(profiles) != 0:
    profileCombo = ttk.Combobox(userFrame, state="readonly", value=profiles)
    profileCombo.current(0)
else:
    profileCombo = ttk.Combobox(userFrame, state="readonly", value=[""])
    profileCombo.current(0)

profileCombo.place(relx=0, rely=0, relwidth=1, relheight=1)
profileCombo.bind("<<ComboboxSelected>>", selectedCombo)

# Task view section
taskFrame = tk.Frame(root, bg="#b3d9ff")
taskFrame.place(relx=0.05, rely=0.125, relwidth=0.9, relheight=0.825)

# Listbox for tasks
taskList = tk.Listbox(taskFrame)
taskList.place(relx=0, rely=0.05, relwidth=1, relheight=1)
refreshTaskList()

# Scrollbar for task list
scrollbar = tk.Scrollbar(taskList)
scrollbar.place(relx=0.975, rely=0, relwidth=0.025, relheight=0.95)
taskList.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=taskList.yview)

# Button: Add task
addTaskButton = tk.Button(taskFrame, text="Add Task", bg=taskButtonColour, command=addTaskWindow)
addTaskButton.place(relx=0, rely=0, relwidth=0.25, relheight=0.05)

# Button: Remove task
removeTaskButton = tk.Button(taskFrame, text="Remove Task", bg=taskButtonColour, command=removeTask)
removeTaskButton.place(relx=0.25, rely=0, relwidth=0.25, relheight=0.05)

# Button: Task details
taskDetailsButton = tk.Button(taskFrame, text="Task Details", bg=taskButtonColour)
taskDetailsButton.place(relx=0.50, rely=0, relwidth=0.25, relheight=0.05)

# Button: Profile Details
profileDetailsButton = tk.Button(taskFrame, text="Profile Details", bg=taskButtonColour, command=profileWindow)
profileDetailsButton.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.05)
#---------END---------#


tk.mainloop()
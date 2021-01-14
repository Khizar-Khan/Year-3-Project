#-------IMPORTS-------#
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database import Database

import re
#---------END---------#


#------VARIABLES------#
windowHeight = 600
windowWidth = 700
maxWindowMultiplier = 1.25

taskButtonColour = "yellow"

db = Database("profile.db")
profileIDs = db.fetchIDs()
profiles = []
#---------END---------#


#------FUNCTIONS------#
def profileWindow():
    def createProfile():
        profileName = re.sub('[\W_]+', '', inputCreate.get())
        if len(profileName) > 0:
            db.insertProfile(profileName)
        else:
            messagebox.showinfo("Information", "Enter name to create a profile!")

        refreshProfilesList()
        profileCombo.config(values=profiles)
        if len(profiles) == 1:
            profileCombo.current(0)

        profileWindow.destroy()
        refreshTaskList()

    def deleteProfile():
        if profileCombo.get() == "":
            messagebox.showinfo("Information", "There are no profiles to delete!")
            profileWindow.destroy()
            return
        profileIndex = profileCombo.current()
        profileIDs = db.fetchIDs()
        profileID = profileIDs[profileIndex]
        db.removeProfile(str(profileID)[2:-3])
        db.removeTasks(str(profileID)[2:-3])

        refreshProfilesList()
        if len(profiles) != 0:
            profileCombo.config(values=profiles)
            profileCombo.current(0)
        else:
            profileCombo.config(values=[""])
            profileCombo.current(0)

        profileWindow.destroy()
        refreshTaskList()

    def updateProfile():
        if profileCombo.get() == "":
            messagebox.showinfo("Information", "There are no profiles to change!")
            profileWindow.destroy()
            return
        profileName = re.sub('[\W_]+', '', inputUpdate.get())
        if len(profileName) > 0:
            profileIndex = profileCombo.current()
            profileIDs = db.fetchIDs()
            profileID = profileIDs[profileIndex]
            db.updateProfile(profileName, str(profileID)[2:-3])
        else:
            messagebox.showinfo("Information", "Enter name to update a profile!")

        refreshProfilesList()
        profileCombo.config(values=profiles)
        if len(profiles) == 1:
            profileCombo.current(0)
        else:
            profileCombo.current(profileIndex)

        profileWindow.destroy()
        refreshTaskList()

    profileWindow = tk.Toplevel()
    profileWindow.minsize(350,150)
    profileWindow.maxsize(350,150)
    profileWindow.title("Profile Details")
    profileWindow.grab_set()

    inputCreate = tk.Entry(profileWindow)
    inputCreate.pack()

    inputUpdate = tk.Entry(profileWindow)
    inputUpdate.pack()

    createProfileButton = tk.Button(profileWindow, text="Create Profile", command=createProfile)
    createProfileButton.pack()

    updateProfileButton = tk.Button(profileWindow, text="Change Profile Name", command=updateProfile)
    updateProfileButton.pack()

    deleteProfileButton = tk.Button(profileWindow, text="Delete Profile", command=deleteProfile)
    deleteProfileButton.pack()

def addTaskWindow():
    if profileCombo.get() == "":
        messagebox.showinfo("Information", "Create a valid profile first!")
        return

    def addTask():
        if len(input.get()) > 0:
            taskText = input.get()
        else:
            messagebox.showinfo("Information", "Enter a task!")
            addTaskWindow.destroy()
            return

        profileIndex = profileCombo.current()
        profileIDs = db.fetchIDs()
        profileID = profileIDs[profileIndex]

        db.insertTask(str(profileID)[2:-3], taskText)
        refreshTaskList()
        addTaskWindow.destroy()

    addTaskWindow = tk.Toplevel()
    addTaskWindow.minsize(350,150)
    addTaskWindow.maxsize(350,150)
    addTaskWindow.title("Add Task")
    addTaskWindow.grab_set()

    input = tk.Entry(addTaskWindow)
    input.pack()

    addTaskButton = tk.Button(addTaskWindow, text="Add Task", command=addTask)
    addTaskButton.pack()

def removeTask():
    if profileCombo.get() == "":
        return
    taskText = str(taskList.get("anchor"))
    profileIndex = profileCombo.current()
    profileIDs = db.fetchIDs()
    profileID = profileIDs[profileIndex]
    db.removeTask(str(profileID)[2:-3], taskText)
    refreshTaskList()

def taskDetailsWindow():
    if taskList.get("anchor") == "":
        messagebox.showinfo("Information", "You do not have a task selected!")
        return
    def setDetail(whichDetail, inputDetail):
        profileIndex = profileCombo.current()
        profileIDs = db.fetchIDs()
        profileID = profileIDs[profileIndex]
        selectedTask = taskList.get("anchor")

        db.setTaskDetail(str(profileID)[2:-3], selectedTask, whichDetail, inputDetail)

        taskDetailsWindow.destroy()
        refreshTaskList()

    taskDetailsWindow = tk.Toplevel()
    taskDetailsWindow.minsize(400,200)
    taskDetailsWindow.maxsize(400,200)
    taskDetailsWindow.title("Task Details")
    taskDetailsWindow.grab_set()

    inputDeadline = tk.Entry(taskDetailsWindow)
    inputDeadline.pack()

    inputReminder = tk.Entry(taskDetailsWindow)
    inputReminder.pack()

    inputRecurring = tk.Entry(taskDetailsWindow)
    inputRecurring.pack()

    inputImportant = tk.Entry(taskDetailsWindow)
    inputImportant.pack()

    setDeadlineButton = tk.Button(taskDetailsWindow, text="Set Deadline", command=lambda:setDetail(1,inputDeadline.get()))
    setDeadlineButton.pack()

    setReminderButton = tk.Button(taskDetailsWindow, text="Set Reminder", command=lambda:setDetail(2,inputReminder.get()))
    setReminderButton.pack()

    setRecurringButton = tk.Button(taskDetailsWindow, text="Set Recurring", command=lambda:setDetail(3,inputRecurring.get()))
    setRecurringButton.pack()

    setImportantButton = tk.Button(taskDetailsWindow, text="Set Important", command=lambda:setDetail(4,inputImportant.get()))
    setImportantButton.pack()

def selectedCombo(event):
    refreshTaskList()

def refreshTaskList():
    if profileCombo.get() == "":
        taskList.delete(0,"end")
        return
    taskList.delete(0,"end")
    profileIndex = profileCombo.current()
    profileIDs = db.fetchIDs()
    profileID = profileIDs[profileIndex]

    dbTaskList = db.fetchTasks(str(profileID)[2:-3])
    for item in dbTaskList:
        taskList.insert("end", str(item)[2:-3])

def refreshProfilesList():
    profiles.clear()
    profileIDs = db.fetchIDs()
    if len(profileIDs) > 0:
        for x in profileIDs:
            profiles.append(db.fetchProfileById(str(x)[2:-3]))
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
if len(profileIDs) != 0:
    refreshProfilesList()
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
taskDetailsButton = tk.Button(taskFrame, text="Task Details", bg=taskButtonColour, command=taskDetailsWindow)
taskDetailsButton.place(relx=0.50, rely=0, relwidth=0.25, relheight=0.05)

# Button: Profile Details
profileDetailsButton = tk.Button(taskFrame, text="Profile Details", bg=taskButtonColour, command=profileWindow)
profileDetailsButton.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.05)
#---------END---------#


tk.mainloop()
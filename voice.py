#-------IMPORTS-------#
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
#---------END---------#

class VoiceAssistant:
    def __init__(self):
        self.assistantIsActive = False

    def speak(self, text):
        tts = gTTS(text=text, lang="en")
        filename = "botVoice.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)

    def getAudio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print(said)
            except Exception as e:
                print("Exception: " + str(e))

        return said

    def interactWithUser(self):
        text = self.getAudio()

        if "new task" in text:
            self.speak("sure, who is this task for?")
            profileName = self.getAudio()

            self.speak("what task would you like to add?")
            taskName = self.getAudio()

            return profileName, taskName, "add task"

        elif "remove task" in text:
            self.speak("sure, who's task would you like to remove?")
            profileName = self.getAudio()

            self.speak("what task would you like to remove?")
            taskName = self.getAudio()

            return profileName, taskName, "remove task"

        elif "add profile" in text:
            self.speak("sure, what name should this profile have?")
            profileName = self.getAudio()

            return profileName, " ", "add profile"

        elif "remove profile" in text:
            self.speak("sure, what profile should I remove?")
            profileName = self.getAudio()

            return profileName, " ", "remove profile"

        elif "set deadline" in text:
            self.speak("sure, which profile is this task for?")
            profileName = self.getAudio()

            self.speak("which task should I set the deadline for?")
            taskName = self.getAudio()

            self.speak("Which year would you like the deadline to be.")
            deadlineYear = self.getAudio()

            self.speak("Which month would you like the deadline to be.")
            deadlineMonth = self.getAudio()

            self.speak("Which day would you like the deadline to be.")
            deadlineDay = self.getAudio()

            return profileName, taskName, "set deadline", deadlineYear, deadlineMonth, deadlineDay

        elif "set reminder" in text or "set a reminder" in text:
            self.speak("sure, which profile is this task for?")
            profileName = self.getAudio()

            self.speak("which task should I set the reminder for?")
            taskName = self.getAudio()

            self.speak("Which year would you like the reminder to be.")
            reminderYear = self.getAudio()

            self.speak("Which month would you like the reminder to be.")
            reminderMonth = self.getAudio()

            self.speak("Which day would you like the reminder to be.")
            reminderDay = self.getAudio()

            return profileName, taskName, "set reminder", reminderYear, reminderMonth, reminderDay

        elif "set important task" in text:
            self.speak("sure, which profile is this task for?")
            profileName = self.getAudio()

            self.speak("which task would you like to make important?")
            taskName = self.getAudio()

            return profileName, taskName, "set important task"

        elif "what tasks" in text or "what task" in text:
            self.speak("which profile are you asking for?")
            profileName = self.getAudio()

            return profileName, "", "what tasks"

        elif "robot exit" in text:
            self.speak("Goodbye")
            return "", "", "exit"
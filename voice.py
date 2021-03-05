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
                print("You said: " + said)
            except Exception as e:
                pass
                #print("Exception: " + str(e))

        return said

    def interactWithUser(self):
        text = self.getAudio()

        if "new task" in text or "add task" in text:
            self.speak("sure, who is this task for?")
            profileName = self.getAudio()

            self.speak("what task would you like to add?")
            taskName = self.getAudio()

            return profileName, taskName, "add task"

        elif "remove task" in text or "delete task" in text:
            self.speak("sure, who's task would you like to remove?")
            profileName = self.getAudio()

            self.speak("what task would you like to remove?")
            taskName = self.getAudio()

            return profileName, taskName, "remove task"

        elif "add profile" in text or "new profile" in text or "create profile" in text:
            self.speak("sure, what name should this profile have?")
            profileName = self.getAudio()

            return profileName, " ", "add profile"

        elif "remove profile" in text or "delete profile" in text:
            self.speak("sure, what profile should I remove?")
            profileName = self.getAudio()

            return profileName, " ", "remove profile"

        elif "set deadline" in text or "add deadline" in text:
            self.speak("sure, which profile is this deadline for?")
            profileName = self.getAudio()

            self.speak("which task should I set the deadline for?")
            taskName = self.getAudio()

            self.speak("Which date would you like the deadline to be.")
            deadlineDate = self.getAudio()

            return profileName, taskName, "set deadline", deadlineDate

        elif "set reminder" in text or "set a reminder" in text or "add reminder" in text:
            self.speak("sure, which profile is this reminder for?")
            profileName = self.getAudio()

            self.speak("which task should I set the reminder for?")
            taskName = self.getAudio()

            self.speak("Which date would you like the reminder to be.")
            deadlineDate = self.getAudio()

            return profileName, taskName, "set reminder", deadlineDate

        elif "set important task" in text or "set important" in text:
            self.speak("sure, which profile is this important task for?")
            profileName = self.getAudio()

            self.speak("which task would you like to make important?")
            taskName = self.getAudio()

            return profileName, taskName, "set important task"

        elif "what tasks" in text or "what task" in text:
            self.speak("which profile are you asking for?")
            profileName = self.getAudio()

            return profileName, "", "what tasks"

        elif "robot exit" in text or "exit robot" in text or "goodbye robot" in text:
            self.speak("Goodbye")
            return "", "", "exit"
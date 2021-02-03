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

        if "remove task" in text:
            self.speak("sure, who's task would you like to remove?")
            profileName = self.getAudio()

            self.speak("what task would you like to remove?")
            taskName = self.getAudio()

            return profileName, taskName, "remove task"

        if "add profile" in text:
            self.speak("sure, what name should this profile have?")
            profileName = self.getAudio()

            return profileName, " ", "add profile"

        if "remove profile" in text:
            self.speak("sure, what profile should I remove?")
            profileName = self.getAudio()

            return profileName, " ", "remove profile"
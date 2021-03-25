#-------IMPORTS-------#
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
#---------END---------#

class VoiceAssistant:
    def __init__(self):
        pass

    def speak(self, text):
        tts = gTTS(text=text, lang="en") # Turn text to speech and in english.
        filename = "botVoice.mp3" # Set location and name for the audio file.
        tts.save(filename) # Save the speech to a location as a specified name.
        playsound.playsound(filename) # Play the sound that is stored in this location
        os.remove(filename) # Remove the file at this location and specified name

    def getAudio(self):
        r = sr.Recognizer() # Set r to do recognition work
        with sr.Microphone() as source: # Get microphone input from source
            audio = r.listen(source) # Listen to the source and store it
            said = "" # Set said to empty if nothing can be recognised

            try:
                said = r.recognize_google(audio) # Use speech recognition and turn the audio into text
                print("You said: " + said) # Print for the user what they have said to the console
            except Exception as e:
                pass # If there was an error in recognising the audio then do nothing
                #print("Exception: " + str(e)) # Print the error

        return said

    def interactWithUser(self):
        text = self.getAudio() # Get user voice and store it

        if "new task" in text or "add task" in text: # If the text is found within
            self.speak("sure, who is this task for?")
            profileName = self.getAudio() # Get profile name from user and store

            self.speak("what task would you like to add?")
            taskName = self.getAudio() # Get task name and store

            return profileName, taskName, "add task" # Return name, task and what action to perform

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
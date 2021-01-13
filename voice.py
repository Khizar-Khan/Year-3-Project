#-------IMPORTS-------#
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
#---------END---------#


#------FUNCTIONS------#
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "botVoice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def getAudio():
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
#---------END---------#


text = getAudio()

if "hello" in text:
    speak("hello, how are you")

if "what is your name" in text:
    speak("my name is Cookie")
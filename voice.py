#Dependancies:
#oauth2client
#pyaudio
#speechrecognition
#google-cloud-speech
#pyttsx

import pyttsx3
import speech_recognition as sr
from apikey import *

# Obtain Audio From Microphone
def getaudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    return r,audio

def processaudio(r,audio):
    try:
        sound = str(r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        print("Google Cloud Speech thinks you said " + sound)
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
    engine = pyttsx3.init()
    engine.say("You said "+sound)
    engine.runAndWait()
    for item in sound.split():
        if item.lower() == 'awake':
            return("User is Awake")

def main():
    r, audio = getaudio()
    print(processaudio(r, audio))

if __name__ == '__main__':
    main()
    

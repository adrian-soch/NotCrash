#Imports
import win32com.client as wincl
import speech_recognition as sr
import pymongo
import datetime
from connections import *

#Obtain Audio Through Microphone
def getaudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    return r,audio

#Process Audio With Google Cloud Speech
def processaudio(r,audio):
    try:
        sound = str(r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        print("Google Cloud Speech Heard " + sound)
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return (str(sound))



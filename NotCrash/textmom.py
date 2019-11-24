#Imports
from lib import lib
from mongo import *
from connections import *
import win32com.client as wincl
import speech_recognition as sr
import pymongo
import datetime
from connections import *

lib = lib(token=stdlib)


#Obtain Audio Through Microphone
def getaudio2():
    r = sr.Recognizer()
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak("What Do You Want To Do?")


    with sr.Microphone() as source:
        print("Listening...")
        sounds = r.listen(source)

    sound = str(r.recognize_google_cloud(sounds, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
    counter = 0 
    print(sound)
    for item in sound.split():
        print(item)
        if item.lower() == 'text':
            counter = 1
            break
        else:
            pass
    if (counter == 1):
        pass
    else:
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak("Please Try Again")
        return 0,0,0


    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak("Who Do You Want To Text?")
    with sr.Microphone() as source:
        print("Who Do You Want To Text?")
        person = r.listen(source)
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak("What Do You Want To Tell This Person?")
    with sr.Microphone() as source:
        print("What Do You Want To Say?")
        audio = r.listen(source)
    return r,person, audio

#Process Audio With Google Cloud Speech
def processaudio2(r,person, audio):
    if (r == 0):
        return 0
    try:
        sound1 = str(r.recognize_google_cloud(person, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        sound2 = str(r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak("Now Texting "+sound1+" the message "+sound2)
        return (str(sound2))
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
    


#Send the text message
def sendSMS2(cell, sound2):
    sms = lib.utils.sms["@1.0.11"]
    message = sound2
    result = sms(to = cell, body = message)

#Main Function
def textmomplis():
    var1,var2,var3 = getaudio2()
    if (processaudio2(var1,var2,var3) == 0):
        pass
    else:
        sendSMS2("INSERT PHONE NUMBER", processaudio2(var1,var2,var3))

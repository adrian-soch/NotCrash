#Imports
from voice import *

#Insert Data Into MongoDB
def runmongo(sound):
    client = pymongo.MongoClient(mongourl)
    db = client.notcrash
    count = int(db.distractions.count()) + 1
    time = str(datetime.datetime.now())
    db.distractions.insert_one({"What Was Said": sound, "Incident": count, "Time": time}) 

#Get Audio and Run Above Function
def insertdata():
    r, audio = getaudio()
    runmongo(processaudio(r, audio))



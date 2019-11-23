from voice import *

def runmongo(sound):
    client = pymongo.MongoClient(mongourl)
    db = client.notcrash
    count = int(db.collection.count()) + 1
    time = datetime.datetime.now()
    db.distractions.insert_one({"Reason": sound, "Incident #": count, "Time": time}) 

def main():
    r, audio = getaudio()
    runmongo(processaudio(r, audio))

if __name__ == '__main__':
    main()
    
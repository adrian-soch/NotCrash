#Imports
from lib import lib
from mongo import *
from connections import *

#Generate Report
def report():
    client = pymongo.MongoClient(mongourl)
    db = client.notcrash
    cursor = db.distractions.find({}, { 'Reason': 1, 'Incident': 1, 'Time': 1, '_id': 0 })
    lis = []
    for items in cursor:
        lis.append(items)
    return lis

#Send the text message
def sendSMS(cell, lis):
    lib = lib(token=stdlib)
    sms = lib.utils.sms["@1.0.11"]
    message = 'Your Driving Details Are Below: \n \n'
    for items in lis:
        message = '\n'*2 + message + str(items) + '\n'*2
    result = sms(to = cell, body = message)

#Main Function
def ending():
    insertdata()
    if (len(report())%1 == 0):
        sendSMS("6478702797", report())


if __name__ == "__main__":
    ending()

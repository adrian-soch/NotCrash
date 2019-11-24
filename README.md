# NotCrash

Connected Vehicle Application that uses OpenCV to check drowsiness of user (while driving), and beeps in order to wake them up. In order to stop the beep the user must say a sentence. Each incident like this is recorded in a MongoDB collection, and if more than five occurances occur in one drive, an sms message is sent to the user that includes the timestammped incidents. Another feature is the user can use voice control to text someone a message. 

## Prerequisites 

- Anaconda (Python 3.7)


## Running 

1. run ```pip install requirements.txt``` 
2. run ```main.py```

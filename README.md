# NotCrash

A connected vehicle application that brings a new safety system which acts on the inside. Leveraging machine learning classifiers and speech recognition software from OpenCV, dlib, and google cloud api's to check and restore driver alertness while providing aditional hands-free functionalities. When a driver is determined to be inalert, an auditory cue is initiated and can only be disengaged by verbal confrimation by the driver. Each incident is recorded in a MongoDB collection, past a certain threshold an sms message is sent to the user that includes the timestammped incidents.

## Prerequisites 

- Anaconda (Python 3.7)


## Running 

1. run ```pip install requirements.txt``` 
2. run ```main.py```

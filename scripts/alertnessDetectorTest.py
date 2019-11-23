import numpy as np
import cv2 as cv
import dlib
import time
import imutils
import winsound
import win32com.client as wincl
import speech_recognition as sr
import pymongo
from lib import lib
import datetime
from connections import *
from scipy.spatial import distance
from imutils import face_utils
from threading import Thread
from multiprocessing import Process

EYE_AR_THRESH = 0.28
EYE_AR_CONSEC_FRAMES = 38

COUNTER = 0
ALARM_ON = False

frequency = 2600  # Set Frequency (Hz)
duration = 333  # Set Duration (ms)

# Obtain Audio From Microphone
def getaudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    return r,audio

# Use Google Cloud To Process Data
def processaudio(r,audio):
    try:
        sound = str(r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        print("Google Cloud Speech Heard " + sound)
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak("You said "+sound)
    return (str(sound))

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

#Generate Report
def report():
    client = pymongo.MongoClient(mongourl)
    db = client.notcrash
    cursor = db.distractions.find({}, { 'What Was Said': 1, 'Incident': 1, 'Time': 1, '_id': 0 })
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


def alarm():
    # Windows machine emits the specific frequency for the specified duration
    winsound.Beep(frequency, duration)

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    #Euclidean distance
    C = distance.euclidean(eye[0], eye[3]) 
	#Eye aspect ratio
    ear = (A + B) / (2.0 * C)
	
    return ear


def headPoseEst():

    # Start video stream
    vs = cv.VideoCapture(1)
    if not vs.isOpened():
        vs = cv.VideoCapture(0)
    time.sleep(0.3)

    # Initialize dlib face detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    image_points = np.array([
                            (359, 391),     # Nose tip 34
                            (399, 561),     # Chin 9
                            (337, 297),     # Left eye left corner 37
                            (513, 301),     # Right eye right corne 46
                            (345, 465),     # Left Mouth corner 49
                            (453, 469)      # Right mouth corner 55
                        ], dtype="double")

    # 3D model points.
    model_points = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip 34
                            (0.0, -330.0, -65.0),        # Chin 9
                            (-225.0, 170.0, -135.0),     # Left eye left corner 37
                            (225.0, 170.0, -135.0),      # Right eye right corne 46
                            (-150.0, -150.0, -125.0),    # Left Mouth corner 49
                            (150.0, -150.0, -125.0)      # Right mouth corner 55

                        ])

    while True:

        if not vs.isOpened():
            vs.release()
            print("Camera Error")
            break

        ret, frame = vs.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = imutils.resize(frame, width=1024, height=576)
        size = gray.shape

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # check to see if a face was detected, and if so, draw the total
        # number of faces on the frame
        if len(rects) > 0:
                text = "{} face(s) found".format(len(rects))
                cv.putText(frame, text, (10, 20), cv.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)

        # loop over the face detections
        for rect in rects:
                # compute the bounding box of the face and draw it on the
                # frame
                        (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
                        cv.rectangle(frame, (bX, bY), (bX + bW, bY + bH),(0, 255, 0), 1)
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                        shape = predictor(gray, rect)
                        shape = face_utils.shape_to_np(shape)
                # loop over the (x, y)-coordinates for the facial landmarks
                # and draw each of them
                        for (i, (x, y)) in enumerate(shape):
                                if i == 33:
                                        #something to our key landmarks
                    # save to our new key point list
                    # i.e. keypoints = [(i,(x,y))]
                                        image_points[0] = np.array([x,y],dtype='double')
                    # write on frame in Green
                                        cv.circle(frame, (x, y), 1, (0, 255, 0), -1)
                                        cv.putText(frame, str(i + 1), (x - 10, y - 10),cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                                elif i == 8:
                    #something to our key landmarks
                    # save to our new key point list
                    # i.e. keypoints = [(i,(x,y))]
                                        image_points[1] = np.array([x,y],dtype='double')
                    # write on frame in Green
                                        cv.circle(frame, (x, y), 1, (0, 255, 0), -1)
                                        cv.putText(frame, str(i + 1), (x - 10, y - 10),cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                                elif i == 36:
                                        #something to our key landmarks
                                        # save to our new key point list
                                        # i.e. keypoints = [(i,(x,y))]
                                        image_points[2] = np.array([x,y],dtype='double')
                                        # write on frame in Green
                                        cv.circle(frame, (x, y), 1, (0, 255, 0), -1)
                                        cv.putText(frame, str(i + 1), (x - 10, y - 10),cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                                elif i == 45:
                                        #something to our key landmarks
                    # save to our new key point list
                    # i.e. keypoints = [(i,(x,y))]
                                        image_points[3] = np.array([x,y],dtype='double')
                    # write on frame in Green
                                        cv.circle(frame, (x, y), 1, (0, 255, 0), -1)
                                        cv.putText(frame, str(i + 1), (x - 10, y - 10),cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                                elif i == 48:
                    #something to our key landmarks
                    # save to our new key point list
                    # i.e. keypoints = [(i,(x,y))]
                                        image_points[4] = np.array([x,y],dtype='double')
                    # write on frame in Green
                                        cv.circle(frame, (x, y), 1, (0, 255, 0), -1)
                                        cv.putText(frame, str(i + 1), (x - 10, y - 10),cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                                elif i == 54:
                    #something to our key landmarks
                    # save to our new key point list
                    # i.e. keypoints = [(i,(x,y))]
                                        image_points[5] = np.array([x,y],dtype='double')
                    # write on frame in Green
                                        cv.circle(frame, (x, y), 1, (0, 255, 0), -1)
                                        cv.putText(frame, str(i + 1), (x - 10, y - 10),cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
                                else:
                    #everything to all other landmarks
                    # write on frame in Red
                                        cv.circle(frame, (x, y), 1, (0, 0, 255), -1)
                                        cv.putText(frame, str(i + 1), (x - 10, y - 10),cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                        focal_length = size[1]
                        center = (size[1]/2, size[0]/2)
                        camera_matrix = np.array([[focal_length,0,center[0]],[0, focal_length, center[1]],[0,0,1]], dtype="double")

                        #print "Camera Matrix :\n {0}".format(camera_matrix)

                        dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
                        (success, rotation_vector, translation_vector) = cv.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv.SOLVEPNP_ITERATIVE)#flags=cv.CV_ITERATIVE)

                        #print "Rotation Vector:\n {0}".format(rotation_vector)
                        #print "Translation Vector:\n {0}".format(translation_vector)
                        # Project a 3D point (0, 0 , 1000.0) onto the image plane
                        # We use this to draw a line sticking out of the nose_end_point2D
                        (nose_end_point2D, jacobian) = cv.projectPoints(np.array([(0.0, 0.0, 1000.0)]),rotation_vector, translation_vector, camera_matrix, dist_coeffs)
                        for p in image_points:
                                cv.circle(frame, (int(p[0]), int(p[1])), 3, (0,0,255), -1)

                        p1 = ( int(image_points[0][0]), int(image_points[0][1]))
                        p2 = ( int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

                        cv.line(frame, p1, p2, (255,0,0), 2)
        # Opens window
        cv.imshow("Frame2", frame)
        #Any key breaks loop
        if cv.waitKey(1) >= 0:
            vs.release()
            break
    # Destroy any leftover windows
    cv.destroyAllWindows()

 
def closedEyeDetector():
    
    # Start video stream
    vs = cv.VideoCapture(1)
    if not vs.isOpened():
        vs = cv.VideoCapture(0)
    time.sleep(0.3)

    # Initialize dlib face detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    # loop over frames from the video stream
    while True:

        if not vs.isOpened():
            vs.release()
            print("Camera Error")
            break

        # Resize recolour captured frame
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Detect face(s)
        rects = detector(gray, 0)

        # loop through faces
        for rect in rects:
            
            # Get facial landmarks
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # Get aspect ratios
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # Average ear value
            ear = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv.convexHull(leftEye)
            rightEyeHull = cv.convexHull(rightEye)

            # Display outline of detected eyes
            cv.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)   
            cv.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # Checking ear ratio
            if ear < EYE_AR_THRESH:
                COUNTER += 1
                CHECKER = 0
                # Sounds alarm after specified counter overflow
                while(COUNTER >= EYE_AR_CONSEC_FRAMES and CHECKER == 0):
                    # Turns alarm on
                    ALARM_ON = True

                    #Plays winsound in background
                    t = Thread(target=alarm)
                    t.daemon = True
                    t.start()

                    
                    # Prints alert
                    cv.putText(frame, "ALERT", (10, 30),cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    sound = processaudio(getaudio())

                    for item in sound.split():
                        if item.lower() == 'awake':
                            CHECKER = 1
                            break
                        else:
                            continue
                        
            else:
                COUNTER = 0
                ALARM_ON = False

            # Prints current ear value
            cv.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
        # Opens window
        cv.imshow("Frame", frame)
        #Any key breaks loop
        if cv.waitKey(1) >= 0:
            vs.release()
            break
    # Destroy any leftover windows
    cv.destroyAllWindows()


def main():
    
    while(1):
        closedEyeDetector()
    #Process(target = closedEyeDetector).start()
    #Process(target = headPoseEst).start()
    
if __name__ == '__main__':
    main()
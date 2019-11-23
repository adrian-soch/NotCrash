import numpy as np
import cv2 as cv
import dlib
import time
import imutils
import winsound

from scipy.spatial import distance
from imutils import face_utils
#from imutils import VideoStream
from threading import Thread

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 48

COUNTER = 0
ALARM_ON = False

frequency = 3000  # Set Frequency (Hz)
duration = 1000  # Set Duration (ms)

def alarm():
    #Windows machine emits the specific frequency for the specified duration
    winsound.Beep(frequency, duration)

def eyeAspectRatio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    #Euclidean distance
    C = distance.euclidean(eye[0], eye[3]) 
	#Eye aspect ratio
    eyeAspect = (A + B) / (2.0 * C)
	
    return eyeAspect

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# 0 for device webcam default
# 1 for external webcam
vs = cv.VideoCapture(1)

if not vs.isOpened():
    vs.release()

while True:


        # Delay for camera to stabilize
        time.sleep(1.0)
        #Take a frame from the video
        ret, frame = vs.read()
        #resize
        frame = imutils.resize(frame,width=450)
        #
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        rects = detector(gray, 0)

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eyeAspectRatio(leftEye)
            rightEAR = eyeAspectRatio(rightEye)
            eyeAspect = (leftEAR + rightEAR)/2.0
            
            leftEyeHull = cv.convexHull(leftEye)
            rightEyeHull = cv.convexHull(rightEye)
            cv.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            
            if eyeAspect < EYE_AR_THRESH:
                COUNTER += 1
                
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    # if the alarm is not on, turn it on
                    if not ALARM_ON:
                        ALARM_ON = True

                        # sound played in the background
                        t = Thread(target=alarm)
                        t.start()
                    cv.putText(frame, "ALERT", (10, 30),cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                COUNTER = 0
                ALARM_ON = False
                cv.putText(frame, "EAR: {:.2f}".format(eyeAspect), (300, 30),cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
        # Display output
        cv.imshow("Frame", frame)
        if cv.waitKey(1) >= 0:
            vs.release()
            break
#Close remaining windows
cv.destroyAllWindows()
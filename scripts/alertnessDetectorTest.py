import numpy as np
import cv2 as cv
import dlib
import time
import imutils
import winsound

from scipy.spatial import distance
from imutils import face_utils
from threading import Thread

EYE_AR_THRESH = 0.28
EYE_AR_CONSEC_FRAMES = 40

COUNTER = 0
ALARM_ON = False

frequency = 2750  # Set Frequency (Hz)
duration = 333  # Set Duration (ms)

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

# Initialize dlib face detector

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Start video stream
vs = vs = cv.VideoCapture(1)
time.sleep(0.3)

# loop over frames from the video stream
while True:

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

            # Sounds alarm after specified counter overflow
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
				# Turns alarm on
                if not ALARM_ON:
                    ALARM_ON = True

                    #Plays winsound in background
                    t = Thread(target=alarm)
                    t.daemon = True
                    t.start()

			# Prints alert
            cv.putText(frame, "ALERT", (10, 30),cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

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
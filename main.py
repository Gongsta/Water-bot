"""
Script that detects when a mouth opens and sends a wireless command to the
gun. Heavily inspired from https://github.com/peterjpxie/detect_mouth_open/blob/master/facerec_from_webcam_mouth_open.py

"""

import face_recognition
import cv2
from datetime import datetime
import math
import time

#Optional Parameters
SHOW_FPS = False

def get_lip_height(lip):
    """Calculate the height of the lip"""
    sum=0
    for i in [2,3,4]:
        # distance between two near points up and down
        distance = math.sqrt( (lip[i][0] - lip[12-i][0])**2 +
                              (lip[i][1] - lip[12-i][1])**2   )
        sum += distance
    return sum / 3

def get_mouth_width(top_lip):
    """Calculate the width of the mouth (used to display the box)"""
    return top_lip[6][0] - top_lip[0][0]


def get_mouth_height(top_lip, bottom_lip):
    """Calculate the height of the mouth(calculated from the distance between the two lips)"""
    sum=0
    for i in [8,9,10]:
        # distance between two near points up and down
        distance = math.sqrt( (top_lip[i][0] - bottom_lip[18-i][0])**2 + 
                              (top_lip[i][1] - bottom_lip[18-i][1])**2   )
        sum += distance
    return sum / 3

def check_mouth_open(top_lip, bottom_lip, verbose=False):
    top_lip_height = get_lip_height(top_lip)
    bottom_lip_height = get_lip_height(bottom_lip)
    mouth_height = get_mouth_height(top_lip, bottom_lip)

    # if mouth is open more than lip height * ratio, return true.
    ratio = 0.5
    if verbose == True:
        print('top_lip_height: %.2f, bottom_lip_height: %.2f, mouth_height: %.2f, min*ratio: %.2f' 
          % (top_lip_height,bottom_lip_height,mouth_height, min(top_lip_height, bottom_lip_height) * ratio))
          
    if mouth_height > min(top_lip_height, bottom_lip_height) * ratio:
        return True
    else:
        return False

# def calculateSizeOfMouth(lip_width, lip_height):


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

while True:
    start_time = time.time()

    # Grab a single frame of video
    ret, frame = video_capture.read()
    face_landmarks_list = face_recognition.face_landmarks(frame)

    try:
        face_landmarks = face_landmarks_list[0]
        
        # Display text for mouth open / close
        top_lip = face_landmarks['top_lip']
        bottom_lip = face_landmarks['bottom_lip']
        ret_mouth_open = check_mouth_open(top_lip, bottom_lip)
        if ret_mouth_open is True:
            text = 'Open'
        else:
            text = 'Closed' 

        bottom_lip_x, bottom_lip_y = bottom_lip[3] #Point 57(center point of bottom lip) 
        top_lip_x, top_lip_y = top_lip[3] #Point 51(center point of top lip)    

        mouth_width = get_mouth_width(top_lip)
        left = top_lip_x - mouth_width//2 -2 #Move by 2 
        right = bottom_lip_x + mouth_width//2 + 2 #Move by 2
        cv2.rectangle(frame, (left, top_lip_y-5), (right, bottom_lip_y+5), (0, 0, 255), 2)
        cv2.putText(frame, text, (left-22, bottom_lip_y + 25), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
        

        cv2.putText(frame, text, (left-22, bottom_lip_y + 25), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
    



    except Exception as e:
        print("An exception occured", e)


    cv2.imshow('Video', frame)

    if SHOW_FPS: #Calculate the frame rate of the video
        time_elapsed = time.time() - start_time
        fps = 1/time_elapsed
        print("FPS:", fps)

    if cv2.waitKey(10) == 27: #Press the "Escape key" to terminate the program
        video_capture.release()
        cv2.destroyAllWindows()
        print("Program terminated, thank you for relieving me from my suffering.")
        break

import cv2
import numpy as np

"""
https://towardsdatascience.com/face-detection-with-haar-cascade-727f68dafd08
Haar cascade is really fast, but it's also really bad with mouth detection...
"""

mouth_cascade = cv2.CascadeClassifier('./haarcascade_mcs_mouth.xml') #Taken from https://github.com/opencv/opencv/blob/3.4/data/haarcascades/haarcascade_frontalface_alt.xm

capture = cv2.VideoCapture(0) #Capture video from webcam

def detectAndDisplay(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)

    #Detect the mouth
    mouth = mouth_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in mouth:
        print("Height", h)
        center = (x+w//2, y+h//2)
        frame = cv2.ellipse(frame, center, (w//2, h//2),0,0, 360, (255,0,255),4)
        break
    cv2.imshow("Mouth", frame)

if not capture.isOpened:
    print("Error opening video capture")
    exit(0)

while True:
    ret, frame = capture.read()
    detectAndDisplay(frame)

    if cv2.waitKey(10) == 27: #Escape key
        capture.release()
        cv2.destroyAllWindows()
        print("Program terminated")
        break








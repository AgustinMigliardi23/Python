import face_recognition
import os
import cv2
import json
import numpy as np

FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog"

def detect_face(frame):
    locations = face_recognition.face_locations(frame, model=MODEL)
    for face_location in locations:
        # face_location = [12, 34, 56, 78]
        # top_left = (282, 225)
        # bottom_right = (411, 354)
        top_left = (face_location[3], face_location[0]- 20)
        bottom_right = (face_location[1], face_location[2] + 20)

        color = [0, 0, 255] # ROJO
        # x_center = int(((face_location[1] - face_location[3]) / 2) + face_location[3])
        # y_center = int(((face_location[2] - face_location[0]) / 2) + face_location[0])

        # print(x_center, y_center)

        #define region of interest
        roi = frame[face_location[0] - 20:face_location[2] + 20, face_location[3]:face_location[1]] # ARRIBA Y: ABAJO Y, IZQ X: DER X

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # define range of skin color in HSV
        lower_colour = np.array([0,20,70], dtype=np.uint8) # azul, verde, rojo
        upper_colour = np.array([20,120,180], dtype=np.uint8)
        
        #extract skin colur imagw  
        mask = cv2.inRange(hsv, lower_colour, upper_colour)

        # cv2.imshow("hsv", hsv)
        cv2.imshow("mask", mask)

        # cv2.circle(frame, (x_center, y_center), 3, color, -1)
        cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)
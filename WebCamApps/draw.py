import  cv2
import numpy as np

def draw(canvas, Xy=None):
    if Xy != None:
        cv2.circle(canvas, Xy, 3, (0, 255, 0),-1)
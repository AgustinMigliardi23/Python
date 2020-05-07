import cv2
import my_own_face_recognition

vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
encodings = my_own_face_recognition.getJSON()
while rval:
    cv2.imshow("face recognition", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    my_own_face_recognition.recognize_face(frame, encodings)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")
import face_recognition
import os
import cv2
import json
import numpy as np

KNOWN_FACES_JSON_DIR = r"C:\Users\agust\Desktop\Toto\Face Recognition\encodings.json"
KNOWN_FACES_DIR = r"C:\Users\agust\Desktop\Toto\Face Recognition\known_faces"
TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog"

def getJSON():
    with open(KNOWN_FACES_JSON_DIR, 'r') as f:
        data = json.load(f)
    return data

known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        datastore = getJSON()
        found = False
        for file in datastore["Encodings"]["Faces"]:
            if file["Filename"] == filename:
                encoding = file["Encoding"]
                encoding = np.array(encoding)
                known_faces.append(encoding)
                known_names.append(file["Name"])
                found = True
        if not found:
            image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(name)
            data = {
                "Name": name,
                "Filename": filename,
                "Encoding": encoding.tolist()
            }
            datastore["Encodings"]["Faces"].append(data)
            with open(KNOWN_FACES_JSON_DIR, 'w') as f:
                json.dump(datastore, f)


def check_duplicates(listOfElems):
    index_of_True = []
    for index, element in enumerate(listOfElems):
        if element:
            index_of_True.append(index)
    return index_of_True

def get_better_match(true_array, face_to_compare):
    new_tolerance = TOLERANCE
    dilema = False
    while check_same_name(true_array, known_names):
        new_tolerance = new_tolerance - 0.0005
        results = face_recognition.compare_faces(known_faces, face_to_compare, new_tolerance)
        true_array = check_duplicates(results)
        if not True in results:
            dilema = True
        if dilema or len(true_array) == 1:
            break
    if dilema:
        new_tolerance = new_tolerance + 0.0005
        results = face_recognition.compare_faces(known_faces, face_to_compare, new_tolerance)
        no_rep_names = get_only_names(check_duplicates(results))
        match = ''
        for name in no_rep_names:
            match += name + " o "
        match = match[:-3]
        return match
    match = known_names[true_array[0]]
    return match

def get_only_names(array_of_trues):
    n = known_names[array_of_trues[0]]
    names = []
    names.append(n)
    for true in range(1, len(array_of_trues)):
        if n != known_names[array_of_trues[true]]:
            names.append(known_names[array_of_trues[true]])
    return names

def check_same_name(indexes_true, names):
    first_name = names[indexes_true[0]]
    for i in range(1, len(indexes_true)):
        if first_name != names[indexes_true[i]]:
            return True
    return False

def recognize_face(frame, encodings):
    locations = face_recognition.face_locations(frame, model=MODEL)
    encodings = face_recognition.face_encodings(frame, locations)
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        match = None
        if True in results:
            indexes_of_true = check_duplicates(results)
            if check_same_name(indexes_of_true, known_names):
                match = get_better_match(indexes_of_true, face_encoding)
            else:
                match = known_names[results.index(True)]

            # print(f"Match found!  {match}")
            # face_location = [12, 34, 56, 78]
            # top_left = (78, 12)
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            color = [0, 255, 0]
            cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2] + 22)
            cv2.rectangle(frame, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(
                frame,
                match,
                (face_location[3] + 10, face_location[2] + 15),
                cv2.FONT_HERSHEY_COMPLEX,
                0.5,
                (0, 0, 0),
                FONT_THICKNESS,
            )
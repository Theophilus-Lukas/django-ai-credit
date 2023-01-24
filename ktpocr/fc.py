import cv2
import json
import matplotlib.pyplot as plt
from ktpocr.form import KTPInformation
# from PIL import Image
import face_recognition
import math
import numpy as np
import dlib


class FACERECO(object):
    def __init__(self, img1, img2):
        self.img1 = dlib.load_rgb_image(img1)
        self.img2 = dlib.load_rgb_image(img2)
        self.result = KTPInformation()
        self.master_process()

    def crop_img2(self, image):
        # Load the dlib shape predictor
        predictor = dlib.shape_predictor(
            "shape_predictor_68_face_landmarks.dat")

        # Load the image
        # image = dlib.load_rgb_image("dataset/aryo_kaca.png")
        image1 = image
        image2 = image1
        # Detect faces in the image
        detector = dlib.get_frontal_face_detector()
        faces = detector(image)

        # Align the faces
        for face in faces:
            shape = predictor(image2, face)
            image2 = dlib.get_face_chip(image2, shape)
        return image2

    def Similar(self, img1, img2):
        rgb_img = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(rgb_img)[0]
        rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]
        result = face_recognition.compare_faces([img_encoding], img_encoding2)
        distance = face_recognition.face_distance(
            [img_encoding], img_encoding2)
        face_match_threshold = 0.6
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - distance) / (range*2.0)
        if distance > face_match_threshold:
            self.result.FaceScore = str(np.round(linear_val, 2))

        else:
            value = (linear_val + ((1.0 - linear_val) *
                     math.pow((linear_val - 0.5)*2, 0.2)))*100
            self.result.FaceScore = str(np.round(value, 2))

    def master_process(self):
        image1 = self.crop_img2(self.img1)
        image2 = self.crop_img2(self.img2)
        self.Similar(image1, image2)

    def to_json(self):
        return json.dumps(self.result.__dict__, indent=4)

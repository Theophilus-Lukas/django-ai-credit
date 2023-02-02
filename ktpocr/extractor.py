import cv2
import json
import re
import numpy as np
import pytesseract
from ktpocr.form import KTPInformation
# from PIL import Image
import dlib
import face_recognition
import math

from creditaidjango.functions import textparser


class KTPOCR(object):
    def __init__(self, image, image2):
        self.image = cv2.imread(image)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.th, self.threshed = cv2.threshold(
            self.gray, 150, 255, cv2.THRESH_TRUNC)
        self.result = KTPInformation()

        # perubahahan dan penambahan
        self.img1 = dlib.load_rgb_image(image)
        self.img2 = dlib.load_rgb_image(image2)

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
            self.result.SCORE_FR = str(np.round(linear_val[0]/100, 2))

        else:
            value = (linear_val + ((1.0 - linear_val) *
                     math.pow((linear_val - 0.5)*2, 0.2)))*100
            self.result.SCORE_FR = str(np.round(value[0]/100, 2))

    def process(self, image):
        raw_extracted_text = pytesseract.image_to_string(
            (self.threshed), lang="ind")
        return raw_extracted_text

    def word_to_number_converter(self, word):
        word_dict = {
            '|': "1"
        }
        res = ""
        for letter in word:
            if letter in word_dict:
                res += word_dict[letter]
            else:
                res += letter
        return res

    def nik_extract(self, word):
        word_dict = {
            'b': "6",
            'e': "2",
            'L': '1',
            '?': '7'
        }
        res = ""
        for letter in word:
            if letter in word_dict:
                res += word_dict[letter]
            else:
                res += letter
        return res

    def extract(self, extracted_result):
        # print(extracted_result.replace('\n', ' -- '))
        for word in extracted_result.split("\n"):
            if "NIK" in word:
                word = word.split(':')
                self.result.nik = self.nik_extract(word[-1].replace(" ", ""))
                if len(self.result.nik) > 16:
                    self.result.nik = self.result.nik[:16]
                self.result.nik = re.sub('\D', '', self.result.nik)
                continue

            if "Nama" in word:
                word = word.split(':')
                self.result.nama = word[-1].replace('Nama ', '')
                self.result.nama = re.sub(
                    r'[^\w]', ' ', self.result.nama).strip()
                continue

            if "Lahir" in word:
                word = word.split(':')
                try:
                    self.result.tanggal_lahir = re.search(
                        "([0-9]{2}\-[0-9]{2}\-[0-9]{4})", word[-1])[0]
                except:
                    self.result.tanggal_lahir = re.search(
                        "[0-9]+", word[-1])[0]
                self.result.tempat_lahir = word[-1].replace(self.result.tanggal_lahir, '').replace(
                    ",", '').replace(":", "").replace(".", "").strip()
                B = self.result.tempat_lahir.split(" ")
                if len(B) > 2:
                    self.result.tempat_lahir = B[-1]
                continue

            if 'Darah' in word:
                try:
                    self.result.jenis_kelamin = re.search(
                        "(LAKI-LAKI|LAKI|LELAKI|PEREMPUAN)", word)[0]
                    word = word.split(':')
                except:
                    self.result.jenis_kelamin = ''

                try:
                    self.result.golongan_darah = re.search(
                        "(O|A|B|AB)", word[-1])[0]
                except:
                    self.result.golongan_darah = '-'
            if 'Alamat' in word:
                self.result.alamat = self.word_to_number_converter(word).replace(
                    "Alamat ", "").replace(".", "").replace(":", "").replace("!", "I")
                # self.result.alamat = re.sub(r'[0-9]', '', self.result.alamat)
                # if "JL" not in self.result.alamat:
                # self.result.alamat = re.sub(r'^', 'JL ', self.result.alamat)
            if 'NO.' in word:
                self.result.alamat = self.result.alamat + ' '+word
            if "Kecamatan" in word:
                k = 0  # iterasi
                kecamatan = []
                for i in word.split(" "):
                    if k > 1 and len(i) >= 3:
                        kecamatan.append(i)
                    k += 1
                for i in kecamatan:
                    self.result.kecamatan += i + " "
                self.result.kecamatan = self.result.kecamatan.strip()
                # self.result.kecamatan = word.split(' ')[-1].strip()
            if "Desa" in word:
                k = 0  # iterasi
                desa = []
                for i in word.split(" "):
                    if k > 0 and len(i) >= 2:
                        desa.append(i)
                    k += 1
                for i in desa:
                    self.result.kelurahan_atau_desa += i + " "
                self.result.kelurahan_atau_desa = self.result.kelurahan_atau_desa.replace(
                    ":", "").replace("-", "").strip()
                # self.result.kelurahan_atau_desa = re.sub(r"[0 - 9]", "", self.result.kelurahan_atau_desa)
                # wrd = word.split()
                # desa = []
                # for wr in wrd:
                #    if not 'desa' in wr.lower():
                #        desa.append(wr)
                # self.result.kelurahan_atau_desa = ''.join(wr)
            if 'Kewarganegaraan' in word:
                # self.result.kewarganegaraan = word.split(' ')[1].strip()
                if "WNI" in word.split(' '):
                    self.result.kewarganegaraan = "WNI"
                else:
                    self.result.kewarganegaraan = "WNA"
            if 'jaan' in word:
                wrod = word.split()
                Pekerjaan = ["BELUM/TIDAK BEKERJA", "MENGURUS RUMAH TANGGA", "PELAJAR/MAHASISWA", "PENSIUNAN", "PEWAGAI NEGERI SIPIL", "TENTARA NASIONAL INDONESIA", "KEPOLISISAN RI", "PERDAGANGAN", "PETANI/ PEKEBUN", "PETERNAK", "NELAYAN/ PERIKANAN", "INDUSTRI", "KONSTRUKSI", "TRANSPORTASI", "KARYAWAN SWASTA", "KARYAWAN BUMN", "KARYAWAN BUMD", "KARYAWAN HONORER", "BURUH HARIAN LEPAS", "BURUH TANI/ PERKEBUNAN", "BURUH NELAYAN/ PERIKANAN", "BURUH PETERNAKAN", "PEMBANTU RUMAH TANGGA", "TUKANG CUKUR", "TUKANG LISTRIK", "TUKANG BATU", "TUKANG KAYU", "TUKANG SOL SEPATU", "TUKANG LAS/ PANDAI BESI", "TUKANG JAHIT", "TUKANG GIGI", "PENATA RIAS", "PENATA BUSANA", "PENATA RAMBUT", "MEKANIK", "SENIMAN", "TABIB", "PARAJI", "PERANCANG BUSANA",
                             "PENTERJEMAH", "IMAM MASJID", "PENDETA", "PASTOR", "WARTAWAN", "USTADZ/ MUBALIGH", "JURU MASAK", "PROMOTOR ACARA", "ANGGOTA DPR-RI", "ANGGOTA DPD", "ANGGOTA BPK", "PRESIDEN", "WAKIL PRESIDEN", "ANGGOTA MAHKAMAH KONSTITUSI", "ANGGOTA KABINET/ KEMENTERIAN", "DUTA BESAR", "GUBERNUR", "WAKIL GUBERNUR", "BUPATI", "WAKIL BUPATI", "WALIKOTA", "WAKIL WALIKOTA", "ANGGOTA DPRD PROVINSI", "ANGGOTA DPRD KABUPATEN/ KOTA", "DOSEN", "GURU", "PILOT", "PENGACARA", "NOTARIS", "ARSITEK", "AKUNTAN", "KONSULTAN", "DOKTER", "BIDAN", "PERAWAT", "APOTEKER", "PSIKIATER/ PSIKOLOG", "PENYIAR TELEVISI", "PENYIAR RADIO",  "PELAUT", "PENELITI", "SOPIR", "PIALANG", "PARANORMAL", "PEDAGANG", "PERANGKAT DESA", "KEPALA DESA", "BIARAWATI", "WIRASWASTA"]
                for i in word.replace(":", "").split(" "):
                    if i in Pekerjaan:
                        self.result.pekerjaan = i
                if self.result.pekerjaan == "":
                    pekerjaan = []
                    for wr in wrod:
                        if not '-' in wr:
                            pekerjaan.append(wr)
                    self.result.pekerjaan = ' '.join(
                        pekerjaan).replace('Pekerjaan :', '').strip()
            if 'Agama' in word:
                Agama = ['ISLAM', 'KRISTEN', 'KATHOLIK',
                         'BUDHA', 'HINDU', 'KONGHUCU']
                for i in word.replace(":", "").split(" "):
                    if i in Agama:
                        self.result.agama = i
                # self.result.agama = word.replace('Agama',"").strip()
            if 'Statu' in word:
                if "BELUM" in word.split(" "):
                    self.result.status_perkawinan = "BELUM KAWIN"
                else:
                    self.result.status_perkawinan = "KAWIN"
            if 'Perkawinan' in word:
                if "BELUM" in word.split(" "):
                    self.result.status_perkawinan = "BELUM KAWIN"
                else:
                    self.result.status_perkawinan = "KAWIN"
                # status = ["KAWIN", "BELUM KAWIN"]
                # for i in word.split(" "):
                #    if i in status:
                #        self.result.status_perkawinan = i
                #    if "BELUM" in word.split()
                # self.result.status_perkawinan = word.split(' ')[-1]
                # if "BELUM" in word.split(' '):
                #    self.result.status_perkawinan = "BELUM KAWIN"
            # if "RTRW" in word:
            #    word = word.replace("RTRW",'')
            #    self.result.rt = word.split('/')[0].strip()
            #    self.result.rw = word.split('/')[1].strip()

    def master_process(self):
        image1 = self.crop_img2(self.img1)
        image2 = self.crop_img2(self.img2)
        self.Similar(image1, image2)
        raw_text = self.process(self.image)

        test_extract = textparser.lukasextract(raw_text)
        print(test_extract)

        self.extract(raw_text)

    def to_dict(self):
        return self.result.__dict__

    def to_json(self):
        return json.dumps(self.result.__dict__, indent=4)

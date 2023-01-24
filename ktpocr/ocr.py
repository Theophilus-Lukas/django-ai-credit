# LEGACY VERSION

import numpy as np
from ktpocr import KTPOCR
import os
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
# from flask import Flask, render_template, request, jsonify
# from flask_restful import Resource, Api
# from flask_cors import CORS


def similar(text1, text2):
    # Create an instance of the TfidfVectorizer/
    vectorizer = TfidfVectorizer()
    # Transform the text strings into numerical vectors
    vectors = vectorizer.fit_transform([text1, text2])
    # Calculate the cosine similarity between the two vectors
    similarity = cosine_similarity(vectors[0], vectors[1])
    # Print the similarity score
    return similarity[0][0]


def score(data):
    try:
        # should check from api
        # response = requests.get(
        #     'https://rafflesia.cloud/nik/api.php?nik='+data['nik'])
        response = {
            'success': True,
            'data': {
                'NOMOR_NIK': '3329062801020001',
                'NOMOR_KK': '3329032803120010',
                'NAMA_LENGKAP': 'MUHAMMAD ANDRIANTO ABDILLAH',
                'JENIS_KELAMIN': 'Laki-Laki',
                'TEMPAT_LAHIR': 'BREBES',
                'TANGGAL_LAHIR': '2002-01-28',
                'GOLONGAN_DARAH': '-',
                'AGAMA': 'ISLAM',
                'STATUS_KAWIN': 'BELUM KAWIN',
                'STATUS_HUBUNGAN_KELUARGA': 'ANAK',
                'PENYANDANG_CACAT': None,
                'PENDIDIKAN_AKHIR': 'SLTP/SEDERAJAT',
                'JENIS_PEKERJAAN': 'PELAJAR/MAHASISWA',
                'NAMA_LENGKAP_IBU': 'SHOLAETUN',
                'NAMA_LENGKAP_AYAH': 'AHMAD LUAYIN',
                'NIK_AYAH': None,
                'NIK_IBU': '3329064105740002',
                'NOMOR_PROVINSI': '33',
                'NAMA_PROVINSI': 'JAWA TENGAH',
                'NOMOR_KABUPATEN': '29',
                'NAMA_KABUPATEN': 'BREBES',
                'NOMOR_KECAMATAN': '3',
                'NAMA_KECAMATAN': 'BUMIAYU',
                'NOMOR_KELURAHAN': '2003',
                'NAMA_KELURAHAN': 'DUKUHTURI',
                'ALAMAT': 'JL. EMPU KANANG',
                'NOMOR_RT': '7',
                'NOMOR_RW': '1',
                'NAMA_DUSUN': None,
                'KODE_POS': '52273',
                'NOMOR_AKTA_LAHIR': None,
                'NOMOR_AKTA_KAWIN': None,
                'TANGGAL_KAWIN': None,
                'NOMOR_AKTA_CERAI': None,
                'TANGGAL_CERAI': None,
                'UPDATE_TERAKHIR': '07-AUG-18'
            }
        }
    except:
        print("Ada yang salah")

    if (response['success']):
        json_response = response
        # print(json_response)
    else:
        print('An error occurred:', response.status_code)

    try:
        disduk_data = json_response['data']
        keys_factor_disduk = ['NOMOR_NIK', 'NAMA_LENGKAP', 'TEMPAT_LAHIR',
                              'TANGGAL_LAHIR', 'ALAMAT', "NAMA_KELURAHAN", 'NAMA_KECAMATAN']
        keys_factor_ocr = ['nik', 'nama', 'tempat_lahir',
                           'tanggal_lahir', 'alamat', "kelurahan_atau_desa", 'kecamatan']

        score = []
        for i in range(1, len(keys_factor_disduk)):
            if keys_factor_disduk[i] == 'NAMA_KECAMATAN':
                score.append(similar(disduk_data[keys_factor_disduk[i]].replace(
                    " ", ""), data[keys_factor_ocr[i]].replace(" ", "")))
                continue
            score.append(
                similar(disduk_data[keys_factor_disduk[i]], data[keys_factor_ocr[i]]))
        return round(np.mean(score), 2)
    except:
        return print("data tidak bisa dieksekusi karena NIK salah")

# # build API
# app = Flask(__name__)
# @app.route("/")
# def home():
#     return "Welcome to the API!"

# # GET request to retrieve data
# @app.route("/data", methods=['GET'])
# def get_data():
#     data = {"name": "John", "age": 30}
#     return jsonify(data)

# # POST request to add data
# @app.route("/data", methods=['POST'])
# def add_data():
#     json_data = request.get_json()
#     name = json_data.get('name')
#     age = json_data.get('age')
#     data = {"name": name, "age": str(score(int(age)+1))}
#     return jsonify(data)


def asid(filename):
    selfie_folder = "ktpocr/dataset/Selfie/"
    ktppath = "ktpocr/dataset/KTP/"

    ktppath = os.path.join(ktppath, filename)
    head, tail = os.path.split(ktppath)
    selfiepath = os.path.join(selfie_folder, tail)

    ocr = KTPOCR(ktppath, selfiepath)
    ocr_dict = ocr.to_dict()

    OcrScore = score(ocr_dict)
    ASIDScore = ((0.7*float(ocr_dict['SCORE_FR']))+0.3*(OcrScore))

    if ASIDScore >= 0.85 and ASIDScore <= 1:
        SCORE_CAT = "Verifikasi Sangat Baik & Fraud Sangat Rendah"
    elif ASIDScore >= 0.75 and ASIDScore < 0.85:
        SCORE_CAT = "Verifikasi Baik & Fraud Rendah"
    elif ASIDScore >= 0.50 and ASIDScore < 0.75:
        SCORE_CAT = "Verifikasi Buruk & Fraud Tinggi"
    elif ASIDScore < 0.50:
        SCORE_CAT = "Verifikasi Sangat Buruk & Fraud Sangat Tinggi"

    # python object to be appended
    SCORE = {"SCORE_OCR": str((OcrScore)), "SCORE_ASID": str(
        round(ASIDScore, 2)), "SCORE_CAT": SCORE_CAT}
    ocr_dict.update(SCORE)

    return ocr_dict

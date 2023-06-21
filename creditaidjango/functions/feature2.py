from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse
# from .models import Predictor
# from .serializers import PredictorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import pytesseract
import re
import cv2
import numpy as np
import json


def ocrnib(image_path):

    # Check if file is an image
    if True:
        custome_oef_config = r'--oem 3 --psm 6 outputbase digits'
        dict = {}
        pattern_nib = r'\d{13}'
        pattern_npwp = r'\d{2}\.\d{3}\.\d{3}\.\d{1}-\d{3}\.\d{3}'
        pattern_kbli = r'\d{5}'
        pattern_telephone = r'\d{10}'
        pattern_company = r"(cv\s.*)"
        pattern_company_2 = r"(pt\s.*)"
        pattern_company_3 = r"(?<=:\s)(.*)"
        pattern_investment = r"(?<=:\s)(.*)"
        pattern_api = r"(?<=:\s)(.*)"

        # read image
        image = cv2.imread(image_path)

        # increase resolution of image
        image = cv2.resize(image, None, fx=2, fy=2,
                           interpolation=cv2.INTER_CUBIC)

        # binarising image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Set a threshold value
        threshold_value = 189

        # Apply the threshold to convert to pure black and white
        ret, gray = cv2.threshold(
            gray, threshold_value, 255, cv2.THRESH_BINARY)

        # denoise gray image
        gaussian = cv2.GaussianBlur(gray, (5, 5), 0)
        unsharp = cv2.addWeighted(gray, 2, gaussian, -0.5, 0)

        # perform text detection using Tesseract OCR
        text = pytesseract.image_to_string(unsharp, config=custome_oef_config)

        # turn text into list
        list = text.split('\n')

        # remove any empty strings from the list and replace them with a space character
        list = [text for text in list if text.strip()]

        # lowercase Semua list
        list = [text.lower() for text in list]

        # pembuatan logika untuk menstore nib
        for text in list:
            try:
                if re.search(pattern_nib, text):
                    dict['nib_number'] = re.search(pattern_nib, text).group()

                if 'nib_number' not in dict:
                    dict['nib_number'] = ''
            except:
                dict['nib_number'] = ''

        # pembuatan logika untuk menstore company name
        for text in list:
            try:
                if 'nama usaha' in text:
                    if re.search(pattern_company, text):
                        dict['company_name'] = re.search(
                            pattern_company, text).group(1)
                    elif re.search(pattern_company_2, text):
                        dict['company_name'] = re.search(
                            pattern_company_2, text).group(1)
                    elif re.search(pattern_company_3, text):
                        dict['company_name'] = re.search(
                            pattern_company_3, text).group(1)

                elif 'nama perusahaan' in text:
                    if re.search(pattern_company, text):
                        dict['company_name'] = re.search(
                            pattern_company, text).group(1)
                    elif re.search(pattern_company_2, text):
                        dict['company_name'] = re.search(
                            pattern_company_2, text).group(1)
                    elif re.search(pattern_company_3, text):
                        dict['company_name'] = re.search(
                            pattern_company_3, text).group(1)

                if 'company_name' not in dict:
                    dict['company_name'] = ''
            except:
                dict['company_name'] = ''

        # pembuatan logika untuk menstore npwp
        for text in list:
            try:
                if re.search(pattern_npwp, text):
                    dict['npwp_number'] = re.search(pattern_npwp, text).group()

                elif 'npwp' in text:
                    text = text.replace(',', '.')
                    dict['npwp_number'] = re.search(pattern_npwp, text).group()

                if 'npwp_number' not in dict:
                    dict['npwp_number'] = ''
            except:
                dict['npwp_number'] = ''

        # pembuatan logika untuk menstore telephone number
        for text in list:
            try:
                if 'telepon' in text:
                    if re.search(pattern_telephone, text):
                        dict['telephone_number'] = re.search(
                            pattern_telephone, text).group()

                if 'telephone_number' not in dict:
                    dict['telephone_number'] = ''

            except:
                dict['telephone_number'] = ''

        # pembuatan logika untuk menstore kode kbli
        for text in list:
            try:
                if 'kbli' in text:
                    if re.search(pattern_kbli, text):
                        dict['kbli_number'] = re.search(
                            pattern_kbli, text).group()

                if 'kbli_number' not in dict:
                    dict['kbli_number'] = ''
            except:
                dict['kbli_number'] = ''

        # pembuatan logika untuk menstore jenis api
        for text in list:
            try:
                if 'jenis api' in text:
                    dict['api_classification'] = re.search(
                        pattern_api, text).group(1)

                if 'api_classification' not in dict:
                    dict['api_classification'] = ''
            except:
                dict['api_classification'] = ''

        # pembuatan logika untuk menstore investment status
        for text in list:
            try:
                if 'status penanaman modal' in text:
                    dict['investment_status'] = re.search(
                        pattern_investment, text).group(1)

                if 'investment_status' not in dict:
                    dict['investment_status'] = ''
            except:
                dict['investment_status'] = ''

        return JsonResponse(dict)

    return {"error": "Invalid file type"}


def ocrsiup(image_path):

    # Check if file is an image
    if True:
        dict = {}
        new_dict = {}
        hasil = []
        pattern_year = r"\b(19|20)\d{2}\b"
        # Menambahkan configurasi untuk pytesseract
        custome_oef_config = r'--oem 3 --psm 6 outputbase digits'
        # Import SIUP Image
        img_siup = cv2.imread(image_path)
        # Convert image to grayscale
        img_siup_gray = cv2.cvtColor(img_siup, cv2.COLOR_BGR2GRAY)
        # Perform text detection using Tesseract OCR
        text_siup = pytesseract.image_to_string(
            img_siup_gray, config=custome_oef_config)
        # Split the text into a list of strings
        lines_siup = text_siup.split('\n')
        # Remove any empty strings from the list and replace them with a space character
        lines_siup = [line for line in lines_siup if line.strip()]
        # Remove any empty strings from the list and replace them with a space character
        lines_siup = [line for line in lines_siup if line.strip()]
        for line in lines_siup:
            if 'Nama KBLI' in line:
                index_Nama_KBLI = lines_siup.index(line)
            elif line.startswith('Kode KBLI') or line.startswith('Nama KEL'):
                index_Kode_KBLI = lines_siup.index(line)
            elif 'Desa/Kelurahan' in line:
                index_desa = lines_siup.index(line)

        # Menambahkan list
        hasil = []
        for line in lines_siup:
            if 'Nama Perusahaan' in line:
                hasil.append(line)
            if 'Nomor Induk Berusaha' in line:
                hasil.append(line)
            try:
                if 'Alamat Perusahaan' in line:
                    index = lines_siup.index(line)
                    alamat_perusahaan = ' '.join(
                        lines_siup[index:index_Nama_KBLI])
                    hasil.append(alamat_perusahaan)
            except:
                hasil.append(line)

            if 'Nama KBLI' in line:
                index = lines_siup.index(line)
                Nama_KBLI = ' '.join(lines_siup[index:index_Kode_KBLI])
                hasil.append(Nama_KBLI)

            if 'Nama KEL' in line:
                index = lines_siup.index(line)
                Nama_KBLI = ' '.join(lines_siup[index:index_Kode_KBLI])
                hasil.append(Nama_KBLI)

            if 'Kode KBLI' in line:
                hasil.append(line)

            if '- Alam' in line:
                index = lines_siup.index(line)
                alamat = ' '.join(lines_siup[index:index_desa])
                hasil.append(alamat)

            if 'Desa/Kelurahan' in line:
                hasil.append(line)

            if 'Kecamatan' in line:
                hasil.append(line)

            if 'Kabupaten/Kota' in line:
                hasil.append(line)

            if 'Provinsi' in line:
                hasil.append(line)

            if 'Dikeluarkan tanggal' in line:
                hasil.append(line)

        # Turn List of string into dictionary (key and value)
        for line in hasil:
            year_match = re.search(pattern_year, line)
            # make filter for year section
            if year_match:
                line = line.replace('|', '1').strip()
                year = int(year_match.group())
                index_year = line.index(str(year)) + len(str(year))
                line = line[:index_year]
            try:
                line = line.replace(':', '').replace('>', '').replace('|', '').replace(
                    '-', '').replace('_', '').replace('—', '').replace('$', '8').strip()
                if '  ' in line:
                    key, value = line.split('  ', 1)
                    dict[key] = value
                elif '   ' in line:
                    key, value = line.split('   ', 1)
                    dict[key] = value
                elif "Dikeluarkan tanggal" in line:
                    key = line[:19].strip()
                    value = line[19:].strip()
                    dict[key] = value
            except:
                return {}

        # Filter Check if the dictionary have all the components
        try:
            for key, value in dict.items():
                if 'Nama Perusahaan' in key:
                    new_key = 'Company Name'
                    new_dict[new_key] = value
                elif 'Nomor Induk' in key:
                    new_key = 'Business Registration Number (NIB)'
                    new_dict[new_key] = value
                elif 'Alamat Perusahaan' in key:
                    new_key = 'Company Address'
                    new_dict[new_key] = value
                elif 'Nama K' in key:
                    new_key = 'KBLI Name'
                    new_dict[new_key] = value
                elif 'Kode K' in key:
                    new_key = 'KBLI Code'
                    new_dict[new_key] = value
                elif 'Barang / Jasa Dagangan' in key:
                    new_key = 'Goods/Services Trade'
                    new_dict[new_key] = value
                elif 'Alam' in key:
                    new_key = 'Address'
                    new_dict[new_key] = value
                elif 'Desa' in key:
                    new_key = 'Sub-district'
                    new_dict[new_key] = value
                elif 'Kecamatan' in key:
                    new_key = 'District'
                    new_dict[new_key] = value
                elif 'Kabupaten' in key:
                    new_key = 'Regency'
                    new_dict[new_key] = value
                elif 'Provinsi' in key:
                    new_key = 'Province'
                    new_dict[new_key] = value
                else:
                    new_key = 'Issued Date'
                    new_dict[new_key] = value
        except:
            return {}
        return JsonResponse(dict)

    return {"error": "Invalid file type"}


def ocrtdp(image_path):

    # Check if file is an image
    if True:
        ocr_results = []
        custome_oef_config = r'--oem 3 --psm 6 outputbase digits'
        dict = {}
        pattern_tdp_number = r'\d{2}\.\d{2}\.\d{1}\.\d{2}\.\d{5}'
        pattern_tdp_number_2 = r'\d{12}'
        pattern_tdp_number_3 = r'\d{2}\.\d{2}\. \d{1}\.\d{2}\.\d{5}'
        pattern_npwp_number = r'\d{2}\.\d{3}\.\d{3}\.\d{1}-\d{3}\.\d{3}'
        pattern_npwp_number_2 = r'r\d\.\d{4}\.\d{4}\.\d{2}\.\d{3}'
        pattern_npwp_number_3 = r'\d{2} \d{3} \d{3} \d-\d{3} \d{3}'
        pattern_kbli_number = r'\d{5}'
        pattern_kbli_number_2 = r'\d{4}'

        image = cv2.imread(image_path)
        # binarising image
        gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        th1, img_bin = cv2.threshold(gray_scale, 150, 225, cv2.THRESH_BINARY)

        # Defining vertical and horizontal kernels
        lineWidth = 3
        lineMinWidth = 20
        kernal1 = np.ones((lineWidth, lineWidth), np.uint8)
        kernal1h = np.ones((1, lineWidth), np.uint8)
        kernal1v = np.ones((lineWidth, 1), np.uint8)

        kernal6 = np.ones((lineMinWidth, lineMinWidth), np.uint8)
        kernal6h = np.ones((1, lineMinWidth), np.uint8)
        kernal6v = np.ones((lineMinWidth, 1), np.uint8)

        # Detect horizontal lines
        # bridge small gap in horizonntal lines
        img_bin_h = cv2.morphologyEx(~img_bin, cv2.MORPH_CLOSE, kernal1h)
        # kep ony horiz lines by eroding everything else in hor direction
        img_bin_h = cv2.morphologyEx(img_bin_h, cv2.MORPH_OPEN, kernal6h)

        # Finding vertical lines
        # bridge small gap in vert lines
        img_bin_v = cv2.morphologyEx(~img_bin, cv2.MORPH_CLOSE, kernal1v)
        # keep only vert lines by encoding everything else in vert direction
        img_bin_v = cv2.morphologyEx(img_bin_v, cv2.MORPH_OPEN, kernal6v)

        # merging vertical and horizontal lines to get blocks. Adding a layer of dilation to remove small gaps
        def fix(img):
            img[img > 127] = 255
            img[img < 127] = 0
            return img

        img_bin_final = fix(fix(img_bin_h) | fix(img_bin_v))

        finalKernel = np.ones((5, 5), np.uint8)
        img_bin_final = cv2.dilate(img_bin_final, finalKernel, iterations=1)

        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(
            ~img_bin_final, connectivity=8, ltype=cv2.CV_32S)

        # Define maximum size of bounding box
        max_size = 200000
        min_size = 1300

        # skipping first two stats as background
        for x, y, w, h, area in stats[2:]:
            if min_size < w*h < max_size:
                # Draw bounding box
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Crop the bounding box from the original image
                box = image[y:y+h, x:x+w]

                # Increase the resolution
                img = cv2.resize(box, None, fx=1.5, fy=1.5,
                                 interpolation=cv2.INTER_CUBIC)

                # Convert image to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Denoise the image
                gray = cv2.medianBlur(gray, 3)

                # Smooth the image
                gaussian = cv2.GaussianBlur(gray, (5, 5), 0)
                unsharp = cv2.addWeighted(gray, 1.9, gaussian, -0.5, 0)

                # Perform OCR on the cropped box
                text = pytesseract.image_to_string(
                    unsharp, config=custome_oef_config)
                ocr_results.append(text)

                # Remove any empty strings from the list and replace them with a space character
                ocr_results = [line for line in ocr_results if line.strip()]

        ocr_results = [s.replace('\n', ' ').strip() for s in ocr_results]
        ocr_results = [line.lower() for line in ocr_results]

        # Pembuatan logika untuk menstore nomor tdp
        for line in ocr_results:
            try:
                if 'tdp' in line:
                    if re.search(pattern_tdp_number, line):
                        line = re.search(pattern_tdp_number, line).group()
                        dict['tdp_number'] = line
                    elif re.search(pattern_tdp_number_2, line):
                        line = re.search(pattern_tdp_number_2, line).group()
                        dict['tdp_number'] = line
                    elif re.search(pattern_tdp_number_3, line):
                        line = re.search(pattern_tdp_number_3, line).group()
                        dict['tdp_number'] = line
                    elif re.search(pattern_tdp_number_3, line):
                        line = re.search(pattern_tdp_number_3, line).group()
                        line = line.replace('. ', '.')
                        dict['tdp_number'] = line
                    elif 'tanggal' in ocr_results[ocr_results.index(line) + 1]:
                        line = ocr_results[ocr_results.index(
                            line) + 2].replace('. ', '.')
                        dict['tdp_number'] = line

                elif 'top' in line:
                    if re.search(pattern_tdp_number, line):
                        line = re.search(pattern_tdp_number, line).group()
                        dict['tdp_number'] = line
                    elif re.search(pattern_tdp_number_2, line):
                        line = re.search(pattern_tdp_number_2, line).group()
                        dict['tdp_number'] = line
                    elif re.search(pattern_tdp_number_3, line):
                        line = re.search(pattern_tdp_number_3, line).group()
                        line = line.replace('. ', '.')
                        dict['tdp_number'] = line
                    elif 'tanggal' in ocr_results[ocr_results.index(line) + 1]:
                        line = ocr_results[ocr_results.index(
                            line) + 2].replace('. ', '.')
                        dict['tdp_number'] = line

                if 'tdp_number' not in dict:
                    dict['tdp_number'] = ''
            except:
                dict['tdp_number'] = ''

        # Pembuatan logika untuk menstore nomor NPWP
        for line in ocr_results:
            try:
                if 'npwp' in line:
                    line = line.replace(',', '.')
                    if re.search(pattern_npwp_number, line):
                        line = re.search(pattern_npwp_number, line).group()
                        dict['npwp_number'] = line
                    elif re.search(pattern_npwp_number_2, line):
                        line = re.search(pattern_npwp_number_2, line).group()
                        dict['npwp_number'] = line

                elif 'npwwp' in line:
                    line = line.replace(',', '.')
                    if re.search(pattern_npwp_number, line):
                        line = re.search(pattern_npwp_number, line).group()
                        dict['npwp_number'] = line
                    elif re.search(pattern_npwp_number_2, line):
                        line = re.search(pattern_npwp_number_2, line).group()
                        dict['npwp_number'] = line

                elif 'pwp' in line:
                    line = line.replace(',', '.')
                    if re.search(pattern_npwp_number, line):
                        line = re.search(pattern_npwp_number, line).group()
                        dict['npwp_number'] = line
                    elif re.search(pattern_npwp_number_2, line):
                        line = re.search(pattern_npwp_number_2, line).group()
                        dict['npwp_number'] = line

                elif 'npwr' in line:
                    line = line.replace(',', '.')
                    if re.search(pattern_npwp_number, line):
                        line = re.search(pattern_npwp_number, line).group()
                        dict['npwp_number'] = line
                    elif re.search(pattern_npwp_number_2, line):
                        line = re.search(pattern_npwp_number_2, line).group()
                        dict['npwp_number'] = line

                elif line.startswith('pw'):
                    line = line.replace(',', '.')
                    if re.search(pattern_npwp_number, line):
                        line = re.search(pattern_npwp_number, line).group()
                        dict['npwp_number'] = line
                    elif re.search(pattern_npwp_number_2, line):
                        line = re.search(pattern_npwp_number_2, line).group()
                        dict['npwp_number'] = line

                elif 'np wp' in line:
                    line = line.replace(',', '.')
                    if re.search(pattern_npwp_number, line):
                        line = re.search(pattern_npwp_number, line).group()
                        dict['npwp_number'] = line
                    elif re.search(pattern_npwp_number_2, line):
                        line = re.search(pattern_npwp_number_2, line).group()
                        dict['npwp_number'] = line

                elif re.search(pattern_npwp_number_3, line):
                    line = re.search(pattern_npwp_number_3, line).group()
                    line = line.replace(' ', '.')
                    dict['npwp_number'] = line

                if 'npwp_number' not in dict:
                    dict['npwp_number'] = ''
            except:
                dict['npwp_number'] = ''

        # Pembuatan logika untuk menstore nomor KBLI
        for line in ocr_results:
            try:
                if 'kbli' in line:
                    if re.search(pattern_kbli_number, line):
                        line = re.search(pattern_kbli_number, line).group()
                        dict['kbli'] = line
                    elif re.search(pattern_kbli_number_2, line):
                        line = re.search(pattern_kbli_number_2, line).group()
                        dict['kbli'] = line

                elif 'kblu' in line:
                    if re.search(pattern_kbli_number, line):
                        line = re.search(pattern_kbli_number, line).group()
                        dict['kbli'] = line
                    elif re.search(pattern_kbli_number_2, line):
                        line = re.search(pattern_kbli_number_2, line).group()
                        dict['kbli'] = line

                elif '«bl' in line:
                    if re.search(pattern_kbli_number, line):
                        line = re.search(pattern_kbli_number, line).group()
                        dict['kbli'] = line
                    elif re.search(pattern_kbli_number_2, line):
                        line = re.search(pattern_kbli_number_2, line).group()
                        dict['kbli'] = line

                elif 'kbu' in line:
                    if re.search(pattern_kbli_number, line):
                        line = re.search(pattern_kbli_number, line).group()
                        dict['kbli'] = line
                    elif re.search(pattern_kbli_number_2, line):
                        line = re.search(pattern_kbli_number_2, line).group()
                        dict['kbli'] = line

                elif 'kbl' in line:
                    if re.search(pattern_kbli_number, line):
                        line = re.search(pattern_kbli_number, line).group()
                        dict['kbli'] = line
                    elif re.search(pattern_kbli_number_2, line):
                        line = re.search(pattern_kbli_number_2, line).group()
                        dict['kbli'] = line

                elif 'lainnya' in line:
                    if re.search(pattern_kbli_number, line):
                        line = re.search(pattern_kbli_number, line).group()
                        dict['kbli'] = line
                    elif re.search(pattern_kbli_number_2, line):
                        line = re.search(pattern_kbli_number_2, line).group()
                        dict['kbli'] = line

                elif 'pokok' in line:
                    if re.search(pattern_kbli_number, line):
                        line = re.search(pattern_kbli_number, line).group()
                        dict['kbli'] = line
                    elif re.search(pattern_kbli_number_2, line):
                        line = re.search(pattern_kbli_number_2, line).group()
                        dict['kbli'] = line

                if 'kbli' not in dict:
                    dict['kbli'] = ''
            except:
                if 'kbli' not in dict:
                    dict['kbli'] = ''

        return JsonResponse(dict)

    return {"error": "Invalid file type"}


def ocrskdp(image_path):

    # Check if file is an image
    if True:
        dict = {}
        new_dict = {}
        hasil = []
        # Menambahkan configurasi untuk pytesseract
        custome_oef_config = r'--oem 3 --psm 6 outputbase digits'
        # Import SIUP Image
        img_siup = cv2.imread(image_path)
        # Convert image to grayscale
        img_siup_gray = cv2.cvtColor(img_siup, cv2.COLOR_BGR2GRAY)
        # Perform text detection using Tesseract OCR
        text_siup = pytesseract.image_to_string(
            img_siup_gray, config=custome_oef_config)
        # Split the text into a list of strings
        lines_siup = text_siup.split('\n')
        # Remove any empty strings from the list and replace them with a space character
        lines_siup = [line for line in lines_siup if line.strip()]
        # Lowercase Semua list
        lines_siup = [line.lower() for line in lines_siup]

        # Mendapatkan index alamat usaha
        for line in lines_siup:
            if 'alamat usaha' in line:
                index_alamat_perusahaan = lines_siup.index(line)
            elif 'alamat perusahaan' in line:
                index_alamat_perusahaan = lines_siup.index(line)
            elif 'tempat usaha' in line:
                index_alamat_perusahaan = lines_siup.index(line)
            elif line.startswith('domisili perusahaan'):
                index_alamat_perusahaan = lines_siup.index(line)

        # Preprocessing data hasil ocr untuk menstore nomor SKDP
        for line in lines_siup:
            try:
                if line.startswith('no.:'):
                    skdp_number = line.split(':')[1].strip()
                    dict['skdp_number'] = skdp_number
                elif line.startswith('nomor'):
                    skdp_number = line.split(':')[1].strip()
                    dict['skdp_number'] = skdp_number
                elif line.startswith('no. :'):
                    skdp_number = line.split(':')[1].strip()
                    dict['skdp_number'] = skdp_number
            except:
                dict['skdp_number'] = ''
        if 'skdp_number' not in dict:
            dict['skdp_number'] = ''

        # Preprocessing data hasil ocr untuk menstore nama di skdp
        for line in lines_siup:
            try:
                if 'nama' in line:
                    if 'nama' in line and 'perusahaan' not in line and 'usaha' not in line and 'perusahan' not in line:
                        nama = line.split('nama')[1].replace(':', '').strip()
                        dict['name'] = nama
            except:
                dict['name'] = ''
        if 'name' not in dict:
            dict['name'] = ''

        # Preprocessing data hasil ocr untuk menstore Tempat/Tanggal Lahir di skdp
        for line in lines_siup:
            try:
                if 'tanggal lahir' in line:
                    place_date_of_birth = line.split('lahir')[1].replace(
                        '+', '').replace(':', '').strip()
                    if ',' in place_date_of_birth:
                        dict['place_date_of_birth'] = place_date_of_birth.split(
                            ',')
                        dict['place_date_of_birth'][1] = dict['place_date_of_birth'][1].strip()
                    else:
                        dict['place_date_of_birth'] = place_date_of_birth
                elif 'lahir' in line:
                    place_date_of_birth = line.split('lahir')[1].replace(
                        '+', '').replace(':', '').strip()
                    if ',' in place_date_of_birth:
                        dict['place_date_of_birth'] = place_date_of_birth.split(
                            ',')
                        dict['place_date_of_birth'][1] = dict['place_date_of_birth'][1].strip()
                    else:
                        dict['place_date_of_birth'] = place_date_of_birth

            except:
                dict['place_date_of_birth'] = ''
        if 'place_date_of_birth' not in dict:
            dict['place_date_of_birth'] = ''

        # Preprocessing data hasil ocr untuk menstore Jenis Kelamin di skdp
        for line in lines_siup:
            try:
                if 'kelamin' in line:
                    gender = line.split('kelamin')[1].replace('.', '').replace(
                        '+', '').replace(':', '').replace('t', 'l').strip()
                    dict['gender'] = gender
            except:
                dict['gender'] = ''
        if 'gender' not in dict:
            dict['gender'] = ''

        # Preprocessing data hasil ocr untuk menstore agama di skdp
        for line in lines_siup:
            try:
                if 'agama' in line:
                    if 'kewarganegaraan' in line:
                        religion = line.split('kewarganegaraan')[1].replace(
                            ':', '').replace('isiam', 'islam').strip()
                        if '/' in religion:
                            dict['religion'] = religion.split('/')[0].strip()
                        else:
                            dict['religion'] = religion
                    elif 'agama' in line:
                        religion = line.split('agama')[1].replace(
                            ':', '').replace('isiam', 'islam').strip()
                        dict['religion'] = religion
            except:
                dict['religion'] = ''
        if 'religion' not in dict:
            dict['religion'] = ''

        # Preprocessing data hasil ocr untuk menstore kewarganegaraan di skdp
        for line in lines_siup:
            if 'kewarganegaraan' in line:
                citizenship = line.split('kewarganegaraan')[
                    1].replace('+', '').strip()
                if '/' in citizenship:
                    dict['citizenship'] = citizenship.split('/')[1].strip()
                else:
                    dict['citizenship'] = citizenship

        # Preprocessing data hasil ocr untuk menstore nomor KTP di skdp
        for line in lines_siup:
            pattern_nik = r"\bnik\b"
            pattern_ktp = r"\bktp\b"
            try:
                if re.search(pattern_ktp, line, re.IGNORECASE):
                    id_card_number = line.split('ktp')[1].replace(
                        '+', '').replace(':', '').replace('nomor', '').strip()
                    dict['id_card_number'] = id_card_number
                elif re.search(pattern_nik, line, re.IGNORECASE):
                    id_card_number = line.split('nik')[1].replace(
                        '+', '').replace(':', '').replace('nomor', '').strip()
                    dict['id_card_number'] = id_card_number
            except:
                dict['id_card_number'] = ''
        if 'id_card_number' not in dict:
            dict['id_card_number'] = ''

        # Preprocessing data hasil ocr untuk menstore occupation di skdp
        for line in lines_siup:
            try:
                if 'pekerjaan' in line:
                    occupation = line.split('pekerjaan')[
                        1].replace('+', '').strip()
                    dict['occupation'] = occupation
            except:
                dict['occupation'] = ''
        if 'occupation' not in dict:
            dict['occupation'] = ''

        # Preprocessing data hasil ocr untuk menstore nama perusahaan di skdp
        for line in lines_siup:
            try:
                if 'nama perusahaan' in line:
                    company_name = line.split('perusahaan')[1].replace(
                        ':', '').replace(',', '').strip()
                    dict['company_name'] = company_name
                elif 'nama usaha' in line:
                    company_name = line.split('usaha')[1].replace(
                        ':', '').replace(',', '').strip()
                    dict['company_name'] = company_name
                elif 'nama perusahan' in line:
                    company_name = line.split('perusahan')[1].replace(
                        ':', '').replace(',', '').strip()
                    dict['company_name'] = company_name
            except:
                dict['company_name'] = ''
        if 'company_name' not in dict:
            dict['company_name'] = ''

        # Preprocessing data hasil ocr untuk menstore jenis usaha di skdp
        for line in lines_siup:
            try:
                if 'jenis usaha' in line:
                    business_category = ', '.join(lines_siup[lines_siup.index(line):index_alamat_perusahaan]).split('usaha')[1].replace('!', 'i').replace(
                        '2.', '').replace('1.', '').replace('klasifikasi', '').replace('-', '').replace('/', '').replace(':', '').replace('—', '').strip()
                    if ',' in business_category:
                        dict['business_category'] = business_category.split(
                            ',  ')
                    else:
                        dict['business_category'] = business_category
            except:
                dict['business_category'] = ''
        if 'business_category' not in dict:
            dict['business_category'] = ''

        # Preprocessing data hasil ocr untuk menstore alamat usaha di skdp
        for line in lines_siup:
            try:
                if 'alamat usaha' in line:
                    business_address = line.split('usaha')[1].replace(
                        '=', '').replace('|', '1').strip()
                    dict['business_address'] = business_address
                elif 'alamat perusahaan' in line:
                    business_address = line.split('perusahaan')[1].replace(
                        '=', '').replace('|', '1').strip()
                    dict['business_address'] = business_address
                elif 'tempat usaha' in line:
                    business_address = line.split('usaha')[1].replace(
                        '=', '').replace('|', '1').strip()
                    dict['business_address'] = business_address
                elif line.startswith('domisili perusahaan'):
                    dict['business_address'] = line.split(
                        'perusahaan')[1].replace('=', '').replace('|', '1').strip()
            except:
                dict['business_address'] = ''
        if 'business_address' not in dict:
            dict['business_address'] = ''

        # Preprocessing data hasil ocr untuk menstore no telepon perusahaan di skdp
        for line in lines_siup:
            try:
                if 'telepon' in line:
                    contact_number = line.split('perusahaan')[1].strip()
                    if '/' in contact_number:
                        dict['contact_number'] = contact_number.split('/ ')
                    else:
                        dict['contact_number'] = contact_number
            except:
                dict['contact_number'] = ''
        if 'contact_number' not in dict:
            dict['contact_number'] = ''

        # Preprocessing data hasil ocr untuk menstore status bangunan di skdp
        for line in lines_siup:
            try:
                if 'status' in line:
                    building_status = line.split('bangunan')[1].replace(
                        'milk', 'milik').replace('sendin', 'sendiri').strip()
                    dict['building_status'] = building_status
            except:
                dict['building_status'] = ''
        if 'building_status' not in dict:
            dict['building_status'] = ''

        # Preprocessing data hasil ocr untuk menstore no akte pendirian perusahaan di skdp
        for line in lines_siup:
            try:
                if 'akte' in line:
                    establishment_deed_number = line.split('perusahaan')[
                        1].strip()
                    if 'nomor' in establishment_deed_number:
                        dict['establishment_deed_number'] = establishment_deed_number.split('nomor')[
                            1].replace(':', '').strip()
                    else:
                        dict['establishment_deed_number'] = establishment_deed_number
                elif line.startswith('akta pendirian perusahaan'):
                    establishment_deed_number = ''.join(
                        lines_siup[lines_siup.index(line):lines_siup.index(line)+3])
                    dict['establishment_deed_number'] = establishment_deed_number.split('perusahaan')[1].replace(':', '').replace(
                        'notaris', '').replace('tanggal', '').replace('=', '').replace('nomor', '').replace('‘', '').strip()
            except:
                dict['establishment_deed_number'] = ''
        if 'establishment_deed_number' not in dict:
            dict['establishment_deed_number'] = ''

        # Preprocessing data hasil ocr untuk menstore SK Pengesahaan Kehakiman di skdp
        for line in lines_siup:
            try:
                if 'kehakiman' in line:
                    judicial_approval_letter = line.split(
                        'kehakiman')[1].replace('=', '').replace('-', '').strip()
                    dict['judicial_approval_letter'] = judicial_approval_letter
            except:
                dict['judicial_approval_letter'] = ''
        if 'judicial_approval_letter' not in dict:
            dict['judicial_approval_letter'] = ''

        # Preprocessing data hasil ocr untuk menstore jumlah karyawan di skdp
        for line in lines_siup:
            try:
                if 'karyawan' in line:
                    staff_number = line.split('karyawan')[1].strip()
                    dict['staff_number'] = staff_number
            except:
                dict['staff_number'] = ''
        if 'staff_number' not in dict:
            dict['staff_number'] = ''

        # Preprocessing data hasil ocr untuk menstore penanggung jawab di skdp
        for line in lines_siup:
            try:
                if 'jawab' in line:
                    if '/' in line:
                        person_in_charge = lines_siup[lines_siup.index(
                            line)+1].split('perusahaan')[1].replace(':', '').strip()
                        dict['person_in_charge'] = person_in_charge
                    else:
                        person_in_charge = line.split('jawab')[1].strip()
                        dict['person_in_charge'] = person_in_charge
                elif 'pimpinan' in line:
                    person_in_charge = line.split('perusahaan')[1].strip()
                    if 'person_in_charge' not in dict:
                        dict['person_in_charge'] = person_in_charge
            except:
                dict['person_in_charge'] = ''
        if 'person_in_charge' not in dict:
            try:
                dict['person_in_charge'] = dict['name']
            except:
                dict['person_in_charge'] = ''
        return JsonResponse(dict)

    return {"error": "Invalid file type"}


def ocrnpwp(image_path):
    # Check if file is an image
    if allowed_file(image_path):
        # Buat komponen
        dict = {}
        new_dict = {}
        hasil = []
        index_npwp = 0
        index_terdaftar = None
        pattern = r'\d{2}-\d{2}-\d{4}'

        # Menambahkan configurasi untuk pytesseract
        custome_oef_config = r'--oem 3 --psm 6'

        # Import SIUP Image
        img_siup = cv2.imread(image_path)

        # Convert image to grayscale
        img_siup_gray = cv2.cvtColor(img_siup, cv2.COLOR_BGR2GRAY)

        # Perform text detection using Tesseract OCR
        text_siup = pytesseract.image_to_string(
            img_siup_gray, config=custome_oef_config)

        # Split the text into a list of strings
        lines_siup = text_siup.split('\n')

        # Remove any empty strings from the list and replace them with a space character
        lines_siup = [line for line in lines_siup if line.strip()]

        # Lowercase Semua list
        lines_siup = [line.lower() for line in lines_siup]

        # Pembuatan logika pyhton jika dokumen npwp
        try:
            for line in lines_siup:
                if 'npwp' in line:
                    index_npwp = lines_siup.index(line)
                    kode_npwp = line.split(':')[1].strip()
                    dict["Code NPWP"] = kode_npwp
                if 'terdaftar' in line:
                    index_terdaftar = lines_siup.index(line)

            # Store dictionary nama
            dict['Name'] = lines_siup[index_npwp+1]

            # Store dictionary alamat
            if index_terdaftar is not None:
                dict['Adress'] = ' '.join(
                    lines_siup[index_npwp+2:index_terdaftar]).strip()
            elif index_terdaftar is None:
                dict['Adress'] = ' '.join(lines_siup[index_npwp+2:]).strip()

            # Store dictionary Terdaftar
            if 'terdaftar' in line:
                terdaftar_line = line[line.find('terdaftar'):]
                dict['registered'] = terdaftar_line.split(
                    ':')[1].replace('/', '-').strip()

            # match the dictionary of date and edit
            match = re.search(pattern, dict['registered'])
            if match:
                date = match.group()
                dict['registered'] = date

        except:
            if 'Code NPWP' not in dict:
                dict['Code NPWP'] = ''
            if 'Name' not in dict:
                dict['Name'] = ''
            if 'Adress' not in dict:
                dict['Adress'] = ''
            if 'registered' not in dict:
                dict['registered'] = ''

        return JsonResponse(dict)

    return {"error": "Invalid file type"}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

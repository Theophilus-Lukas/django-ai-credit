# this is the prediction function
from ktpocr import ocr


def id_score_filename(filename):
    result = ocr.asid(filename)
    return result

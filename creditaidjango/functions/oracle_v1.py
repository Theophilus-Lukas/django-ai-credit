# this is the prediction function
from ktpocr import ocr


def id_score(data_id):
    result = ocr.asid(data_id)
    return result

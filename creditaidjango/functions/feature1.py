# this is the prediction function
from ktpocr import ocr


def id_score(selfiepath, ktppath):
    result = ocr.asid(selfiepath, ktppath)
    return result

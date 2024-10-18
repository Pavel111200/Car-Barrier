import cv2
import pytesseract
import numpy as np
import easyocr
from cv2.typing import MatLike

class ANPR():
    def __init__(self):
        # self.reader = easyocr.Reader(['en'])
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    def read_text_from_image_easyocr(self, image: MatLike) -> str:
        """
            Read the text from the given image using easyocr

            Parameters:
                image (MatLike): the image from which text needs to be read
        
        """
        text = self.reader.readtext(image, detail=0, allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        if len(text) > 0:
            return text[0]
        return None
    
    def read_text_from_image_tesseract(self, image: MatLike) -> str:
        """
            Read the text from the given image using tesseract

            Parameters:
                image (MatLike): the image from which text needs to be read
        
        """
        if image is not None:
            alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            options = "-c tessedit_char_whitelist={}".format(alphanumeric)
            options += " --psm {}".format(7)
            text = pytesseract.image_to_string(image, config=options)  
            return text
        return None

    def get_license_plate(self, image):
        contours = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        
        square_contours = []
        cropped_plate = None

        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            
            if cv2.contourArea(c) > 4000 and cv2.contourArea(c) < 7000:
                square_contours.append(c)

        square_contours = sorted(square_contours, key=cv2.contourArea, reverse=True)

        for c in square_contours:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            if ar >= 3.5 and ar <= 5.1:
                cropped_plate = image[y:y + h, x:x + w]
        return cropped_plate
        
        
        
import cv2
import numpy as np
from PIL import Image

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (5, 5), 0)        # reduce noise
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  # binarize
    temp_path = "preprocessed.png"
    cv2.imwrite(temp_path, img)
    return temp_path

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe "
file = 'numbers/21.png'
img = cv2.imread(file)
num = pytesseract.image_to_string(img)
print(num)

# cv2.imshow('21', img)
# cv2.waitKey(0)

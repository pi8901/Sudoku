import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import pytesseract

# Bild laden
image_path = "./Images/sudoku.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Adaptive Thresholding für bessere Konturerkennung
processed = cv2.GaussianBlur(image, (5, 5), 0)
processed = cv2.adaptiveThreshold(processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Kernel für Morphologische Operationen
kernel = np.ones((2, 2), np.uint8)

kernel2 = np.ones((1,1), np.uint8)

# Öffnen: Entfernt kleine Punkte (Rauschen)
processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel, iterations=1)

# Schließen: Schließt Lücken in den Gitterlinien
processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel2, iterations=2)


width = image.shape[0]
height = image.shape[1]

dim = math.floor(width/9)

sudoku = [[0 for i in range(9)] for j in range(9)]

for i in range(9):
    for j in range(9):
        cropped_image = processed[i*dim:(i+1)*dim, j*dim:(j+1)*dim]
        cc = cropped_image[5:dim-5, 5:dim-5]
        cv2.imshow("Sudoku Grid", cc)
        letter = pytesseract.image_to_string(cc, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        if letter == "":
            sudoku[i][j] = 0
        else:
            sudoku[i][j] = int(letter)
        print(letter)

print(sudoku)






# Anzeigen des verbesserten Bilds
plt.imshow(processed, cmap='gray')
plt.title("Nach Morphologischen Operationen")
plt.show()

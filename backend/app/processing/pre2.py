import cv2
import pytesseract
import numpy as np

# Bild laden
image = cv2.imread("./Images/sudoku.png", cv2.IMREAD_GRAYSCALE)

# Bildgröße anpassen (optional, falls das Bild zu groß ist)
image = cv2.resize(image, (450, 450))

# Rauschreduzierung
image = cv2.GaussianBlur(image, (5, 5), 0)

# Adaptive Thresholding anwenden, um das Bild zu binarisieren
binary = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Konturen finden, um das Sudoku-Raster zu lokalisieren
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_contour = max(contours, key=cv2.contourArea)

# Maske für das Sudoku-Raster erstellen
mask = np.zeros_like(image)
cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

# Nur den Bereich innerhalb des Sudoku-Rasters behalten
cropped = cv2.bitwise_and(binary, binary, mask=mask)

# Tesseract konfigurieren
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=123456789'

# Sudoku-Feld initialisieren
sudoku = [[0 for _ in range(9)] for _ in range(9)]

# Zellen des Sudoku-Rasters verarbeiten
cell_height = cropped.shape[0] // 9
cell_width = cropped.shape[1] // 9

for row in range(9):
    for col in range(9):
        # Zelle ausschneiden
        y_start = row * cell_height
        y_end = (row + 1) * cell_height
        x_start = col * cell_width
        x_end = (col + 1) * cell_width
        cell = cropped[y_start:y_end, x_start:x_end]

        # Texterkennung in der Zelle durchführen
        text = pytesseract.image_to_string(cell, config=custom_config).strip()
        if text.isdigit():
            sudoku[row][col] = int(text)

# Sudoku-Feld ausgeben
for row in sudoku:
    print(row)
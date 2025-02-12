import cv2
import math  # Importiere math, um Pi zu verwenden
import pytesseract



# Bild laden
image = cv2.imread("./Images/img1_digital.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Graustufenbild

# Schwellenwert setzen, um das Bild zu binarisieren
_, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Gitter erkennen (Optional: Kanten finden und Linien erkennen)
edges = cv2.Canny(binary_image, 100, 200)

# Linien im Bild erkennen
# Beispielcode für HoughLinesP
lines = cv2.HoughLinesP(edges, 1, math.pi / 180, 100, minLineLength=50, maxLineGap=10)

# Linien zeichnen
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

print(image.shape)
# Bereich um das Sudoku-Feld extrahieren (Abhängig vom erkannten Gitter)
x, y, w, h = 0, 0, 75, 75  # Beispielkoordinaten
cropped_image = image[y:y+h, x:x+w]
cv2.imshow("Sudoku Grid", cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# OCR anwenden
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
extracted_text = pytesseract.image_to_string(cropped_image, config=custom_config)

print("Erkannte Zahlen:", extracted_text)



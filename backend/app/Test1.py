from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np
import pytesseract

class CameraApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.img = Image()
        self.sudoku_label = Label(text="Erkanntes Sudoku", font_size=20)
        self.reset_button = Button(text="Neues Sudoku erfassen", size_hint=(1, 0.1))
        self.reset_button.bind(on_press=self.reset_sudoku)

        self.layout.add_widget(self.img)
        self.layout.add_widget(self.sudoku_label)
        self.layout.add_widget(self.reset_button)

        self.cap = cv2.VideoCapture(0)
        self.sudoku_fixed = None  # Speichert das erkannte Sudoku
        Clock.schedule_interval(self.update, 1.0 / 10.0)  # 10 FPS

        return self.layout

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        if self.sudoku_fixed is None:
            processed, sudoku_numbers = self.detect_sudoku_grid(frame)
            if sudoku_numbers is not None:
                self.sudoku_fixed = sudoku_numbers
                self.sudoku_label.text = self.format_sudoku(sudoku_numbers)
        else:
            processed = frame  # Nur das aktuelle Kamerabild anzeigen
        
        # OpenCV Bild -> Kivy Texture
        buf1 = cv2.flip(processed, 0).tobytes()
        texture = Texture.create(size=(processed.shape[1], processed.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf1, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

    def detect_sudoku_grid(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        # Finden der größten Kontur (das Sudoku-Gitter)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        sudoku_grid = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                sudoku_grid = approx
                break

        if sudoku_grid is not None:
            cv2.drawContours(frame, [sudoku_grid], -1, (0, 255, 0), 2)

            # Perspektivische Transformation
            pts = sudoku_grid.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")

            # Sortiere Punkte: oben-links, oben-rechts, unten-rechts, unten-links
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            dst = np.array([[0, 0], [450, 0], [450, 450], [0, 450]], dtype="float32")
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(frame, M, (450, 450))

            # Sudoku-Zahlen extrahieren
            sudoku_numbers = self.extract_sudoku_numbers(warped)

            return warped, sudoku_numbers

        return frame, None  # Falls kein Sudoku erkannt wird

    def extract_sudoku_numbers(self, image):
        height, width = image.shape[:2]
        dim = height // 9  # Kachelgröße

        sudoku = [[0 for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                cropped_image = image[i * dim:(i + 1) * dim, j * dim:(j + 1) * dim]
                cc = cropped_image[5:dim-5, 5:dim-5]  # Rand entfernen

                gray = cv2.cvtColor(cc, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (3, 3), 0)

                # Adaptive Thresholding
                thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY_INV, 11, 2)

                # Rauschen reduzieren
                kernel = np.ones((2,2), np.uint8)
                thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

                # Konturen finden
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if contours:
                    largest_contour = max(contours, key=cv2.contourArea)
                    x, y, w, h = cv2.boundingRect(largest_contour)

                    # Prüfen, ob die erkannte Form groß genug für eine Zahl ist
                    if w * h > 100:
                        number_roi = thresh[y:y + h, x:x + w]

                        # Tesseract OCR zur Erkennung der Zahl
                        letter = pytesseract.image_to_string(
                            number_roi, config='--psm 10 -c tessedit_char_whitelist=0123456789'
                        ).strip()

                        if letter.isdigit():
                            sudoku[i][j] = int(letter)

        return sudoku

    def format_sudoku(self, sudoku):
        return "\n".join([" ".join(str(num) if num != 0 else "." for num in row) for row in sudoku])

    def reset_sudoku(self, instance):
        self.sudoku_fixed = None
        self.sudoku_label.text = "Erkanntes Sudoku"

    def on_stop(self):
        self.cap.release()

if __name__ == '__main__':
    CameraApp().run()

from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class CameraApp(App):
    def build(self):
        self.img = Image()
        self.cap = cv2.VideoCapture(0)  # Kamera dauerhaft geöffnet halten
        self.sudoku_saved = False  # Flag, um mehrfaches Speichern zu verhindern
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS
        return self.img

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        processed = self.detect_sudoku_grid(frame)

        # OpenCV Bild -> Kivy Texture
        buf1 = cv2.flip(processed, 0).tobytes()
        texture = Texture.create(size=(processed.shape[1], processed.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf1, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

    def detect_sudoku_grid(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        # Finden der größten Kontur
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        sudoku_grid = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:  # Ein Rechteck (möglicherweise das Sudoku)
                sudoku_grid = approx
                break

        if sudoku_grid is not None:
            # Zeichne das erkannte Sudoku
            cv2.drawContours(frame, [sudoku_grid], -1, (0, 255, 0), 2)

            # Perspektivische Transformation für ein gerades Sudoku-Gitter
            pts = sudoku_grid.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")

            # Sortiere Punkte: oben-links, oben-rechts, unten-rechts, unten-links
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            # Zielpunkte für die Transformierte (ein 450x450 px großes Sudoku)
            dst = np.array([[0, 0], [450, 0], [450, 450], [0, 450]], dtype="float32")

            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(frame, M, (450, 450))

            # **Speichere das Sudoku-Bild nur einmal**
            if not self.sudoku_saved:
                cv2.imwrite("sudoku.png", warped)
                print("Sudoku-Bild gespeichert als 'sudoku.png'")
                self.sudoku_saved = True  # Verhindert mehrfaches Speichern

            return warped

        return frame  # Falls kein Sudoku erkannt wurde, das Originalbild zurückgeben

    def on_stop(self):
        self.cap.release()  # Kamera schließen, wenn die App beendet wird

if __name__ == '__main__':
    CameraApp().run()

from flask import Flask, request, jsonify
import pytesseract
import cv2
import numpy as np
import math
import json

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve_sudoku():
    # Empfange Bild aus der Anfrage
    img_file = request.files['image']
    img_data = img_file.read()
    
    # Lade das Bild und konvertiere es in ein numpy Array
    nparr = np.frombuffer(img_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Bildgröße berechnen und Sudoku-Raster extrahieren
    width = image.shape[0]
    height = image.shape[1]
    dim = math.floor(width / 9)
    sudoku = [[0 for i in range(9)] for j in range(9)]
    
    for i in range(9):
        for j in range(9):
            cropped_image = image[i*dim:(i+1)*dim, j*dim:(j+1)*dim]
            cc = cropped_image[10:dim-10, 10:dim-10]
            letter = pytesseract.image_to_string(cc, config='--psm 6 -c tessedit_char_whitelist=0123456789')
            if letter == "":
                sudoku[i][j] = 0
            else:
                sudoku[i][j] = int(letter)

    # Lösung des Sudokus
    def is_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num:
                return False
        for i in range(9):
            if board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    solve(sudoku)

    # Antwort mit der gelösten Sudoku-Matrix zurückgeben
    return jsonify(sudoku)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

import sys
import cv2
import pytesseract
import math
import json

def process_sudoku(image_path):
    # Bild laden
    image = cv2.imread(image_path)
    width, height = image.shape[0], image.shape[1]
    dim = math.floor(width / 9)

    sudoku = [[0 for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            cropped_image = image[i*dim:(i+1)*dim, j*dim:(j+1)*dim]
            cc = cropped_image[10:dim-10, 10:dim-10]

            letter = pytesseract.image_to_string(cc, config='--psm 6 -c tessedit_char_whitelist=0123456789').strip()
            sudoku[i][j] = int(letter) if letter.isdigit() else 0

    return sudoku

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

if __name__ == "__main__":
    image_path = sys.argv[1]
    sudoku = process_sudoku(image_path)

    if solve_sudoku(sudoku):
        print(json.dumps(sudoku))
    else:
        print(json.dumps({"error": "Sudoku konnte nicht gelöst werden"}))

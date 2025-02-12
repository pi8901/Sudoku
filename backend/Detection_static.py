import cv2
import pytesseract
import math



# Bild laden
image = cv2.imread("./Images/img1_digital.png")

print(image.shape)

width = image.shape[0]
height = image.shape[1]

dim = math.floor(width/9)

sudoku = [[0 for i in range(9)] for j in range(9)]

for i in range(9):
    for j in range(9):
        cropped_image = image[i*dim:(i+1)*dim, j*dim:(j+1)*dim]
        cc = cropped_image[10:dim-10, 10:dim-10]
        cv2.imshow("Sudoku Grid", cc)
        cv2.waitKey(50)
        cv2.destroyAllWindows()
        letter = pytesseract.image_to_string(cc, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        if letter == "":
            sudoku[i][j] = 0
        else:
            sudoku[i][j] = int(letter)



def is_valid(board, row, col, num):
    # Prüfe, ob die Zahl bereits in der Zeile vorhanden ist
    for i in range(9):
        if board[row][i] == num:
            return False
    
    # Prüfe, ob die Zahl bereits in der Spalte vorhanden ist
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # Prüfe, ob die Zahl bereits im 3x3 Block vorhanden ist
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    
    return True

def solve_sudoku(board):
    # Finde eine leere Zelle
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                # Versuche jede Zahl von 1 bis 9
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        # Setze die Zahl ein
                        board[row][col] = num
                        
                        # Rekursiver Schritt
                        if solve_sudoku(board):
                            return True
                        
                        # Backtracking: Setze die Zahl zurück
                        board[row][col] = 0
                
                # Wenn keine Zahl gültig ist, gehe zurück
                return False
    return True


# Löse das Sudoku
solve_sudoku(sudoku)

# Ausgabe der Lösung
for row in sudoku:
    print(row)



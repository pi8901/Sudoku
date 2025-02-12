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

# Beispiel-Sudoku
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Löse das Sudoku
solve_sudoku(board)

# Ausgabe der Lösung
for row in board:
    print(row)

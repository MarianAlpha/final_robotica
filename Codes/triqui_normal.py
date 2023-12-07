import random

def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def minimax(board, depth, maximizing_player):
    scores = {'X': 1, 'O': -1, 'tie': 0}

    if check_winner(board, 'X'):
        return scores['X'] - depth

    if check_winner(board, 'O'):
        return scores['O'] + depth

    if is_board_full(board):
        return scores['tie']

    if maximizing_player:
        max_eval = float('-inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'X'
            eval = minimax(board, depth + 1, False)
            board[i][j] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'O'
            eval = minimax(board, depth + 1, True)
            board[i][j] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(board):
    best_move = None
    best_eval = float('-inf')
    for i, j in get_empty_cells(board):
        board[i][j] = 'X'
        eval = minimax(board, 0, False)
        board[i][j] = ' '
        if eval > best_eval:
            best_eval = eval
            best_move = (i, j)
    return best_move

def play():
    board = [[' ' for _ in range(3)] for _ in range(3)]

    while True:
        print_board(board)
        player_row = int(input("Ingrese el número de fila (0, 1, 2): "))
        player_col = int(input("Ingrese el número de columna (0, 1, 2): "))

        if board[player_row][player_col] == ' ':
            board[player_row][player_col] = 'O'
        else:
            print("¡Celda ocupada! Intenta de nuevo.")
            continue

        if check_winner(board, 'O'):
            print_board(board)
            print("¡Ganaste!")
            break

        if is_board_full(board):
            print_board(board)
            print("¡Empate!")
            break

        print("Turno de la máquina...")
        machine_row, machine_col = get_best_move(board)
        board[machine_row][machine_col] = 'X'

        if check_winner(board, 'X'):
            print_board(board)
            print("¡La máquina gana!")
            break

        if is_board_full(board):
            print_board(board)
            print("¡Empate!")
            break

if __name__ == "__main__":
    play()

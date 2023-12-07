import cv2
import numpy as np
import keyboard
from pydobot import Dobot
import time
import DobotControl as dc
import DobotDllType as dType



dc.HOME()
time.sleep(21)

# Conectar al Dobot
dobot = Dobot(port="COM11")  # Reemplaza "COMX" con el puerto COM correcto


def dividir_en_9_segmentos(frame):
    height, width, _ = frame.shape

    segmentos = [
        (0, 0, width // 3, height // 3),
        (width // 3, 0, 2 * width // 3, height // 3),
        (2 * width // 3, 0, width, height // 3),
        (0, height // 3, width // 3, 2 * height // 3),
        (width // 3, height // 3, 2 * width // 3, 2 * height // 3),
        (2 * width // 3, height // 3, width, 2 * height // 3),
        (0, 2 * height // 3, width // 3, height),
        (width // 3, 2 * height // 3, 2 * width // 3, height),
        (2 * width // 3, 2 * height // 3, width, height)
    ]

    matriz_segmentos = []

    for segmento in segmentos:
        x1, y1, x2, y2 = segmento
        segmento_actual = frame[y1:y2, x1:x2].copy()
        matriz_segmentos.append(segmento_actual)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return matriz_segmentos

def detectar_fichas(frame):
    # Convertir el frame a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir el rango de azul
    rango_bajo1 = np.array([h_bajo1, s_bajo1, v_bajo1])
    rango_alto1 = np.array([h_alto1, s_alto1, v_alto1])

    rango_bajo2 = np.array([h_bajo2, s_bajo2, v_bajo2])
    rango_alto2 = np.array([h_alto2, s_alto2, v_alto2])

    # Crear una máscara para las fichas en el rango definido
    mascara = cv2.inRange(hsv, rango_bajo1, rango_alto1)
    mascara2 = cv2.inRange(hsv, rango_bajo2, rango_alto2)

    # Encontrar contornos en la máscara
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos2, _ = cv2.findContours(mascara2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    fichas = []
    fichas_r = []

    for contorno in contornos:
        # Calcular el área del contorno
        area = cv2.contourArea(contorno)
        
        # Filtrar contornos pequeños para eliminar ruido
        if area > area_minima:
            # Obtener las coordenadas del rectángulo que rodea el contorno
            x, y, w, h = cv2.boundingRect(contorno)
            centro_x = x + w // 2
            centro_y = y + h // 2

            # Agregar las coordenadas al conjunto de fichas detectadas
            fichas.append((centro_x, centro_y))

    for contorno in contornos2:
        # Calcular el área del contorno
        area = cv2.contourArea(contorno)
        
        # Filtrar contornos pequeños para eliminar ruido
        if area > area_minima:
            # Obtener las coordenadas del rectángulo que rodea el contorno
            x, y, w, h = cv2.boundingRect(contorno)
            centro_x = x + w // 2
            centro_y = y + h // 2

            # Agregar las coordenadas al conjunto de fichas detectadas
            fichas_r.append((centro_x, centro_y))
            
    return fichas, fichas_r

def hay_objeto_rojo(segmento):
    # Convertir el segmento a espacio de color HSV
    hsv = cv2.cvtColor(segmento, cv2.COLOR_BGR2HSV)

    # Definir el rango de colores rojos en HSV
    bajo_rojo = np.array([h_bajo2, s_bajo2, v_bajo2])
    alto_rojo = np.array([h_alto2, s_alto2, v_alto2])

    # Crear una máscara para los colores rojos
    mascara_roja = cv2.inRange(hsv, bajo_rojo, alto_rojo)

    # Contar los píxeles blancos en la máscara
    cantidad_pixeles_blancos = np.sum(mascara_roja == 255)

    # Determinar si hay un objeto rojo basado en el número de píxeles blancos
    return cantidad_pixeles_blancos > 100  # Ajusta el umbral según sea necesario

def hay_objeto_azul(segmento):
    # Convertir el segmento a espacio de color HSV
    hsv = cv2.cvtColor(segmento, cv2.COLOR_BGR2HSV)

    # Definir el rango de colores rojos en HSV
    bajo_azul = np.array([h_bajo1, s_bajo1, v_bajo1])
    alto_azul = np.array([h_alto1, s_alto1, v_alto1])

    # Crear una máscara para los colores rojos
    mascara_azul = cv2.inRange(hsv, bajo_azul, alto_azul)

    # Contar los píxeles blancos en la máscara
    cantidad_pixeles_blancos = np.sum(mascara_azul == 255)

    # Determinar si hay un objeto rojo basado en el número de píxeles blancos
    return cantidad_pixeles_blancos > 100  # Ajusta el umbral según sea necesario

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
    return all(cell != '0' for row in board for cell in row)

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == '0']

def minimax(board, depth, maximizing_player):
    scores = {'R': 1, 'A': -1, 'tie': 0}

    if check_winner(board, 'R'):
        return scores['R'] - depth

    if check_winner(board, 'A'):
        return scores['A'] + depth

    if is_board_full(board):
        return scores['tie']

    if maximizing_player:
        max_eval = float('-inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'R'
            eval = minimax(board, depth + 1, False)
            board[i][j] = '0'
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i, j in get_empty_cells(board):
            board[i][j] = 'A'
            eval = minimax(board, depth + 1, True)
            board[i][j] = '0'
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(board):
    best_move = None
    best_eval = float('-inf')
    for i, j in get_empty_cells(board):
        board[i][j] = 'R'
        eval = minimax(board, 0, False)
        board[i][j] = '0'
        if eval > best_eval:
            best_eval = eval
            best_move = (i, j)
    return best_move

def mov_segmentos(fil, colm):
    
    if fil == 0 and colm == 0: # Segmento 1
        new_pos = [164.4917,-65.0625,-50.5086,0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
        dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)
        

    elif fil == 0 and colm == 1: # Segmento 2
        new_pos = [207.6942,-66.983,-50.508,0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
        dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)
        

    elif fil == 0 and colm == 2: # Segmento 3
        new_pos = [245.0884,-66.9834,-50.5073,0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
        dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)
        

    elif fil == 1 and colm == 0: # Segmento 4
        new_pos = [160.7999,-111.4318,-53.9401,0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
        dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)
        

    elif fil == 1 and colm == 1: # Segmento 5
        new_pos = [204.0949,-110.856,-54.876,0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
        dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)
        

    elif fil == 1 and colm == 2: # Segmento 6
        new_pos = [247.0313,-109.1287,-55.8116,0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
        dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)
        

    elif fil == 2 and colm == 0: # Segmento 7
        new_pos = [169.1271,-157.9933,-54.6118,0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
        dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)
        

    elif fil == 2 and colm == 1: # Segmento 8
        new_pos = [209.5198,-153.4577,-54.6111,0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
        dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)
        

    elif fil == 2 and colm == 2: # Segmento 9
        new_pos = [247.0313,-153.458,-54.6112,0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
        dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)


def pos_prin():
    #Movimeintos del robot
    dobot.suck(True)
    # Posición HOME
    new_pos = [232.82,2.47,52.83, 0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
    dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)  

    # Agarra ficha
    new_pos = [177.5763,20.7143,-60.1826,0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
    dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)     

    # Posición HOME
    new_pos = [232.82,2.47,52.83, 0.6799]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
    dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)  

 
h_bajo1, s_bajo1, v_bajo1 = 100, 50, 100
h_alto1, s_alto1, v_alto1 = 130, 255, 255

h_bajo2, s_bajo2, v_bajo2 = 0, 100, 100
h_alto2, s_alto2, v_alto2 = 10, 255, 255

area_minima = 100

# Capturar el video de la cámara
cap = cv2.VideoCapture(1)

fichas_board = np.array(['0', '0', '0', '0', '0', '0', '0', '0', '0'])

# Para definir los movimientos
flag1 = True
flag2 = True
flag3 = True
flag4 = True
flag5 = True
conteo_r = 0

#Para el mesaje

message = "El Ganador "
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
text_size = cv2.getTextSize(message, font, font_scale, font_thickness)[0]

while True:
    ret, frame = cap.read()

    # Detección de fichas en el frame actual
    fichas_detectadas, fichas_rojas = detectar_fichas(frame)
    
    # Mostrar el frame con las fichas resaltadas
    for ficha in fichas_detectadas:
        cv2.circle(frame, ficha, 10, (0, 255, 0), -1)
    
    for ficha in fichas_rojas:
        cv2.circle(frame, ficha, 10, (0, 255, 255), -1)

    matriz_segmentos = dividir_en_9_segmentos(frame)
    
    height, width, _ = frame.shape
    x = (width - text_size[0]) // 2
    y = (height + text_size[1]) // 2
    
    for i, segmento in enumerate(matriz_segmentos):
        if hay_objeto_rojo(segmento):
            print(f'Rojo: {i}')
            fichas_board[i] = 'R'

            
    for i, segmento in enumerate(matriz_segmentos):
        if hay_objeto_azul(segmento):
            print(f'Azul: {i}')
            fichas_board[i] = 'A'
            conteo_r = np.count_nonzero(fichas_board == 'A')
    
    board = fichas_board.reshape((3,3))

    print(f'tablero: {board}')
    
    if check_winner(board, 'A'):
        cv2.putText(frame, 'Ganaste!', (x, y), font, font_scale, (0, 0, 255), font_thickness, cv2.LINE_AA)
        print("¡Ganaste!")
        

    if is_board_full(board):
        cv2.putText(frame, 'Empate!', (x, y), font, font_scale, (0, 0, 255), font_thickness, cv2.LINE_AA)
        print("¡Empate!")
    


    cv2.imshow('Deteccion de Fichas', frame)


    if conteo_r == 1 and flag1:
        print("Turno de la maquina...")
        pos_prin()
        machine_row, machine_col = get_best_move(board)
        board[machine_row][machine_col] = 'R'
        mov_segmentos(machine_row, machine_col)
        flag1 = False
        dobot.suck(False)
    

    elif conteo_r == 2 and flag2:
        print("Turno de la maquina...")
        pos_prin()
        machine_row, machine_col = get_best_move(board)
        board[machine_row][machine_col] = 'R'
        mov_segmentos(machine_row, machine_col)
        flag2 = False
        dobot.suck(False)

    elif conteo_r == 3 and flag3:
        print("Turno de la maquina...")
        pos_prin()
        machine_row, machine_col = get_best_move(board)
        board[machine_row][machine_col] = 'R'
        mov_segmentos(machine_row, machine_col)
        flag3 = False
        dobot.suck(False)

    elif conteo_r == 4 and flag4:
        print("Turno de la maquina...")
        pos_prin()
        machine_row, machine_col = get_best_move(board)
        board[machine_row][machine_col] = 'R'
        mov_segmentos(machine_row, machine_col)
        flag4 = False
        dobot.suck(False)

    elif conteo_r == 5 and flag5:
        print("Turno de la maquina...")
        pos_prin()
        machine_row, machine_col = get_best_move(board)
        board[machine_row][machine_col] = 'R'
        mov_segmentos(machine_row, machine_col)
        flag5 = False
        dobot.suck(False)
        
    # Posición HOME
    new_pos = [232.82,2.47,52.83, 0]  # Reemplaza con las coordenadas deseadas (x, y, z, r)
    dobot.move_to(new_pos[0], new_pos[1], new_pos[2], new_pos[3], wait=True)  
     


    if check_winner(board, 'R'):
        print_board(board)
        cv2.putText(frame, 'La maquina gana!', (x, y), font, font_scale, (0, 0, 255), font_thickness, cv2.LINE_AA)
        print("¡La maquina gana!")

    if is_board_full(board):
        cv2.putText(frame, 'Empate!', (x, y), font, font_scale, (0, 0, 255), font_thickness, cv2.LINE_AA)

        
    cv2.imshow('Deteccion de Fichas', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


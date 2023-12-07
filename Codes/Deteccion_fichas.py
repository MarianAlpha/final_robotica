import cv2
import numpy as np

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



h_bajo1, s_bajo1, v_bajo1 = 100, 50, 100
h_alto1, s_alto1, v_alto1 = 130, 255, 255

h_bajo2, s_bajo2, v_bajo2 = 0, 100, 100
h_alto2, s_alto2, v_alto2 = 10, 255, 255

area_minima = 100

# Capturar el video de la cámara
cap = cv2.VideoCapture(0)

fichas_board = np.array(['0', '0', '0', '0', '0', '0', '0', '0', '0'])

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
    
    for i, segmento in enumerate(matriz_segmentos):
            if hay_objeto_rojo(segmento):
                print(f'Rojo: {i}')
                fichas_board[i] = 'R'

            
    for i, segmento in enumerate(matriz_segmentos):
        if hay_objeto_azul(segmento):
            print(f'Azul: {i}')
            fichas_board[i] = 'A'
    
    board = fichas_board.reshape((3,3))
    

    print(f'tablero: {board}')

        
    cv2.imshow('Detección de Fichas', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()

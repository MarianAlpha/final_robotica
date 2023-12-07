# Proyecto Final Robótica Industrial

# Manual de usuario

## Introducción

Este manual proporciona instrucciones sobre cómo utilizar el proyecto donde un Dobot Magician jugará triqui por medio de visón artificial.

## Instalación

Para instalar este proyecto, sigue estos pasos:

1. Descarga el proyecto desde [Repositorio](https://github.com/MarianAlpha/final_robotica)
2. Descomprime el proyecto en una carpeta de tu elección.
3. Instala las librerias necesarias.

## Librerias

```python
pip install opencv-python
```
```python
pip install numpy
```
```python
pip install pydobot
```
```python
pip install keyboard
```

Programa externo: DobotDIIType.py ----> API del dobot

Este proyecto implementa un juego de triqui (o tres en raya) utilizando un robot Dobot junto con la detección de colores a través de una cámara para ubicar las fichas en el tablero. Antes de iniciar el juego, es crucial seguir estos pasos de configuración:

## Configuración Inicial

1. Área de trabajo

   Este juego se debe realizar preferiblemente sobre un tablero de color uniforme que contraste con el color de las fichas, en este caso rojo y azul. Además, se debe tener cuidado de que no haya ningún otro objeto de color que pueda interferir en la identificación de las fichas.
   
2. Mapeo del Área de Trabajo
 
   Para asegurar la precisión en la ubicación de las fichas, ejecuta el script de mapeo proporcionado. Esto permitirá al robot tener una referencia exacta de la disposición   de las fichas en el área de trabajo.

3. Posicionamiento de la Cámara

   Asegúrate de colocar la cámara de manera que los 9 segmentos del tablero queden perfectamente visibles dentro del área de trabajo del robot. Esto asegurará que la detección de colores funcione correctamente y permitirá al Dobot ubicar las fichas con precisión.

### Ejecución del Juego

Una vez que la configuración inicial esté completa, sigue estos pasos para iniciar el juego:

**Ejecutar el Script Principal:** Ejecuta el script principal del juego. Este iniciará la detección de colores, controlará el Dobot para ubicar las fichas en el tablero y permitirá jugar el triqui.

**Interacción Durante el Juego:** Durante la ejecución siempre inicia el usuario, sigue las instrucciones proporcionadas en la consola para jugar. Las fichas serán ubicadas por el Dobot, y podrás hacer tus movimientos cuando sea tu turno.

#### A tener en cuenta:

Se debe ser muy preciso al momento de ubicar las fichas en el tablero, teniendo especial cuidado que en ningún momento la ubicación de la ficha quede entre dos cuadrantes.

### Finalización del Juego

**Para finalizar el juego:**

Determinación de un Ganador o Empate: Cuando haya un ganador o un empate, se mostrará en la consola y se cerrará la ventana de la cámara automáticamente.

Interrumpir Manualmente: Si deseas salir del juego antes de que haya un resultado, presiona la tecla "q" en la consola para cerrar la ventana de la cámara y liberar los recursos.

## Experimentos

En este repositorio se encuentran otros archivos con los cuales se realizaron los experimentos:

1. Archivo con el programa que detecta los colores azul y rojo, divide la cámara en 9 segmentos y detecta e imprime la posición del objeto de color en el segmento en el que se encuentre. [Identificación y segmentación](https://github.com/MarianAlpha/final_robotica/blob/main/Codes/Deteccion_fichas.py) 

2. Archivo en el cuál se encuentra el programa en el cuál nos basabamos para realizar el proyecto [Triqui](https://github.com/MarianAlpha/final_robotica/blob/main/Codes/triqui_normal.py) 

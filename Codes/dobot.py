from pydobot import Dobot

# Conectar al Dobot
dobot = Dobot(port="COM11")  # Reemplaza "COMX" con el puerto COM correcto

# Activar la succión (asumiendo que la ventosa está conectada y lista)
#dobot.suck(True)
pos = dobot.pose()

# Imprimir la posición actual
print(f"Posición actual: {pos}")


dobot.home(True)

"""
# Mover el Dobot a una posición específica con coordenadas cartesianas (x, y, z, r)
pos1 = (230, 20, -20, 0)  # Reemplaza con las coordenadas cartesianas deseadas (x, y, z, r)
dobot.move_to(pos1[0], pos1[1], pos1[2], pos1[3], wait=True)

# Desactivar la succión después de un tiempo (puedes ajustar el tiempo según sea necesario)
# Esto simula recoger un objeto y luego soltarlo después de un tiempo
import time
time.sleep(5)  # Esperar 3 segundos
# Mover el Dobot a una posición específica con coordenadas cartesianas (x, y, z, r)
# pos1 = (200, 0, 50, 0)  # Reemplaza con las coordenadas cartesianas deseadas (x, y, z, r)
dobot.move_to(pos[0], pos[1], pos[2], pos[3], wait=True)
dobot.suck(False)  # Liberar la succión

pos2 = dobot.pose()

# Imprimir la posición actual
print(f"Posición actual: {pos2}")"""

# Desconectar el Dobot
dobot.close()

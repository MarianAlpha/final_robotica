import DobotDllType as dType



def HOME():

    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
    }

    # Cargar la DLL y obtener el objeto CDLL correspondiente
    api = dType.load()

    # Conectar con Dobot
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Estado de conexión:", CON_STR[state])

    if state == dType.DobotConnect.DobotConnect_NoError:
        # Limpiar comandos en cola
        dType.SetQueuedCmdClear(api)
        
        # Configurar parámetros de home
        dType.SetHOMEParams(api, 232.82, 2.47, 52.83, 0.6799, isQueued=1)

        # Ir a home
        dType.SetHOMECmd(api, temp=0, isQueued=1)

        # Iniciar la ejecución de comandos en cola
        dType.SetQueuedCmdStartExec(api)

        # Esperar a que se complete el comando de ir a home
        while dType.GetQueuedCmdCurrentIndex(api)[0] != 0:
            dType.dSleep(100)
            break

        # Detener la ejecución de comandos en cola
        dType.SetQueuedCmdStopExec(api)

    # Desconectar de Dobot
    dType.DisconnectDobot(api)




HOME()

print("HOLA")

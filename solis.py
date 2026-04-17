def solicitar_nombre_validado(mensaje):
    """
    Solicita un nombre que solo tenga letras y espacios
    """
    nombre = input(mensaje).strip()
    while len(nombre) == 0 or not solo_letras_y_espacios(nombre):
        if len(nombre) == 0:
            print("ERROR: el nombre no puede estar vacio.")
        else:
            print("ERROR: solo puede contener letras y espacios. Sin numeros ni simbolos.")
        nombre = input(mensaje).strip()
    return nombre

def solicitar_horario_validado(mensaje):
    """
    Solicita un horario con formato HH:MM
    """
    horario = input(mensaje).strip()
    while not validar_horario(horario):
        print("ERROR: el horario debe tener el formato HH:MM (ej: 14:00).")
        horario = input(mensaje).strip()
    return horario

def solicitar_asiento_validado():
    """
    Solicita un asiento con formato valido (A1 a J10)
    """
    asiento = input("Ingrese el asiento deseado (ej: A5): ").strip().upper()
    while not validar_asiento(asiento):
        print("ERROR: formato invalido. Use letra A-J seguida de numero 1-10 (ej: A5, J10).")
        asiento = input("Ingrese el asiento: ").strip().upper()
    return asiento


# ==============================================
#    MATRIZ DE ASIENTOS - FUNCIONES
# ==============================================

def asiento_a_indices(asiento):
    """
    Convierte 'A5' en (fila=0, col=4) para indexar la matriz
    """
    fila    = FILAS_ASIENTOS.index(asiento[0].upper())
    columna = int(asiento[1:]) - 1
    return fila, columna

def marcar_asiento_ocupado(asiento):
    """
    Pone 1 en la celda correspondiente de la matriz
    """
    fila, columna = asiento_a_indices(asiento)
    matrizAsientos[fila][columna] = 1

def esta_asiento_ocupado(asiento):
    """
    Retorna True si la celda de la matriz vale 1
    """
    fila, columna = asiento_a_indices(asiento)
    return matrizAsientos[fila][columna] == 1

def contar_asientos_disponibles():
    """
    Usa filter + lambda sobre la matriz aplanada para contar los libres
    """
    todosLosAsientos = [estado for fila in matrizAsientos for estado in fila]
    libres = list(filter(lambda estado: estado == 0, todosLosAsientos))
    return len(libres)

def mostrarMapaAsientos():
    """
    Muestra el mapa visual recorriendo la matriz bidimensional
    """
    imprimir_separador("       MAPA DE ASIENTOS")
    print("\n              PANTALLA\n     ========================\n")
    print("      1  2  3  4  5  6  7  8  9 10 \n")
    i = 0
    while i < len(FILAS_ASIENTOS):
        print("  " + FILAS_ASIENTOS[i] + "  ", end="")
        j = 0
        while j < COLUMNAS_ASIENTOS:
            print("[X]" if matrizAsientos[i][j] == 1 else "[ ]", end="")
            j = j + 1
        print()
        i = i + 1
    disponibles = contar_asientos_disponibles()
    ocupados    = len(FILAS_ASIENTOS) * COLUMNAS_ASIENTOS - disponibles
    print("\n==========================================")
    print("  [ ] = Disponible  |  [X] = Ocupado")
    print("  Disponibles: " + str(disponibles) + "  |  Ocupados: " + str(ocupados))
    print("==========================================")

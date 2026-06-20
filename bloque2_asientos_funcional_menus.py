#    MATRIZ DE ASIENTOS - FUNCIONES
def asiento_a_indices(asiento):
    """
    Convierte 'A5' en (fila=0, col=4) para indexar la matriz
    """
    try:
        fila    = FILAS_ASIENTOS.index(asiento[0].upper())
        columna = int(asiento[1:]) - 1
        return fila, columna
    except ValueError:
        print("ERROR: asiento invalido: " + asiento)
        return 0, 0

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


#    PROGRAMACION FUNCIONAL: map / filter / reduce
def obtenerRecaudacionPorPelicula():
    """
    map + lambda: recaudacion de cada pelicula (entradas x precio)
    """
    if len(dictPeliculas) == 0:
        return []
    indices = list(range(len(dictPeliculas)))
    return list(map(lambda i: entradasVendidas[i] * precios[i], indices))

def obtenerPeliculasConVentas():
    """
    filter + lambda: indices de peliculas con al menos 1 venta
    """
    if len(dictPeliculas) == 0:
        return []
    indices = list(range(len(dictPeliculas)))
    return list(filter(lambda i: entradasVendidas[i] > 0, indices))

def calcularRecaudacionTotalReduce():
    """
    reduce + lambda: suma total de todas las recaudaciones
    """
    recaudaciones = obtenerRecaudacionPorPelicula()
    if len(recaudaciones) == 0:
        return 0
    try:
        return reduce(lambda acum, valor: acum + valor, recaudaciones)
    except TypeError:
        print("ERROR: no se pudo calcular la recaudacion total.")
        return 0

def obtenerComprasSuperioresAPromedio():
    """
    filter + lambda: numeros de compra que superan el promedio
    """
    if len(dictCompras) == 0:
        return []
    numeros  = list(dictCompras.keys())
    totales  = list(map(lambda k: dictCompras[k]["total"], numeros))
    promedio = sum(totales) / len(totales)
    return list(filter(lambda k: dictCompras[k]["total"] > promedio, numeros))

def obtenerNombresEnMayuscula():
    """
    map + lambda: todos los nombres de compradores en mayuscula
    """
    return list(map(lambda k: dictCompras[k]["nombreComprador"].upper(), dictCompras.keys()))

def calcularTotalVentasReduce():
    """
    reduce + lambda: suma total de todas las compras de espectadores
    """
    if len(dictCompras) == 0:
        return 0
    totales = list(map(lambda k: dictCompras[k]["total"], dictCompras.keys()))
    try:
        return reduce(lambda acum, x: acum + x, totales)
    except TypeError:
        print("ERROR: no se pudo calcular el total de ventas.")
        return 0

def reporteFuncional():
    """
    Reporte que muestra en pantalla los resultados de map, filter y reduce
    """
    imprimir_separador("   REPORTE FUNCIONAL (map / filter / reduce)")

    # MAP: recaudacion por pelicula
    recaudaciones = obtenerRecaudacionPorPelicula()
    nombres_lista = list(dictPeliculas.values())
    print("\n[MAP] Recaudacion calculada por pelicula:")
    if len(recaudaciones) == 0:
        print("  Sin peliculas cargadas.")
    else:
        i = 0
        while i < len(nombres_lista):
            print("  " + nombres_lista[i] + ": $" + str(recaudaciones[i]))
            i = i + 1

    # FILTER: peliculas con ventas
    indicesConVentas = obtenerPeliculasConVentas()
    print("\n[FILTER] Peliculas con entradas vendidas: " + str(len(indicesConVentas)))
    i = 0
    while i < len(indicesConVentas):
        idx = indicesConVentas[i]
        print("  - " + nombres_lista[idx] + " (" + str(entradasVendidas[idx]) + " vendidas)")
        i = i + 1

    # REDUCE: total recaudado
    print("\n[REDUCE] Recaudacion total del cine: $" + str(calcularRecaudacionTotalReduce()))

    if len(dictCompras) > 0:
        numeros  = list(dictCompras.keys())
        totales  = list(map(lambda k: dictCompras[k]["total"], numeros))
        promedio = sum(totales) / len(totales)

        superiores = obtenerComprasSuperioresAPromedio()
        print("\n[FILTER] Compras superiores al promedio ($" + str(round(promedio, 2)) + "):")
        if len(superiores) == 0:
            print("  Ninguna compra supera el promedio.")
        else:
            i = 0
            while i < len(superiores):
                k = superiores[i]
                print("  - " + dictCompras[k]["nombreComprador"] + ": $" + str(dictCompras[k]["total"]))
                i = i + 1

        print("\n[REDUCE] Total recaudado en ventas al espectador: $" + str(calcularTotalVentasReduce()))

        nombresMayus = obtenerNombresEnMayuscula()
        print("\n[MAP] Compradores transformados a mayuscula:")
        i = 0
        while i < len(nombresMayus):
            print("  " + str(i + 1) + ". " + nombresMayus[i])
            i = i + 1

    print("\n==========================================")


#    CONJUNTOS - DIFERENCIA DE ASIENTOS
def asientosDisponibles():
    """
    Usa diferencia de conjuntos para obtener los asientos libres:
    todosLosAsientos - asientosOcupados = asientosLibres
    """
    todosLosAsientos = set()
    i = 0
    while i < len(FILAS_ASIENTOS):
        j = 1
        while j <= COLUMNAS_ASIENTOS:
            todosLosAsientos.add(FILAS_ASIENTOS[i] + str(j))
            j = j + 1
        i = i + 1

    asientosOcupados = set()
    i = 0
    while i < len(FILAS_ASIENTOS):
        j = 0
        while j < COLUMNAS_ASIENTOS:
            if matrizAsientos[i][j] == 1:
                asientosOcupados.add(FILAS_ASIENTOS[i] + str(j + 1))
            j = j + 1
        i = i + 1

    return todosLosAsientos - asientosOcupados

def mostrarAsientosDisponibles():
    """
    Muestra los asientos libres usando diferencia de conjuntos
    """
    imprimir_separador("  ASIENTOS DISPONIBLES (conjuntos)")
    disponibles = asientosDisponibles()
    ocupados    = len(FILAS_ASIENTOS) * COLUMNAS_ASIENTOS - len(disponibles)
    print(" Total disponibles: " + str(len(disponibles)))
    print(" Total ocupados:    " + str(ocupados))
    print("\n Asientos libres: " + str(sorted(disponibles)))
    print("==========================================")



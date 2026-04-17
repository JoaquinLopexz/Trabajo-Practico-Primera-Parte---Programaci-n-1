# ==============================================
#    PROGRAMACION FUNCIONAL: map / filter / reduce
# ==============================================

def obtenerRecaudacionPorPelicula():
    """
    map + lambda: recaudacion de cada pelicula (entradas x precio)
    """
    if len(peliculas) == 0:
        return []
    indices = list(range(len(peliculas)))
    return list(map(lambda i: entradasVendidas[i] * precios[i], indices))

def obtenerPeliculasConVentas():
    """
    filter + lambda: indices de peliculas con al menos 1 venta
    """
    if len(peliculas) == 0:
        return []
    indices = list(range(len(peliculas)))
    return list(filter(lambda i: entradasVendidas[i] > 0, indices))

def calcularRecaudacionTotalReduce():
    """
    reduce + lambda: suma total de todas las recaudaciones
    """
    recaudaciones = obtenerRecaudacionPorPelicula()
    if len(recaudaciones) == 0:
        return 0
    return reduce(lambda acum, valor: acum + valor, recaudaciones)

def obtenerComprasSuperioresAPromedio():
    """
    filter + lambda: indices de compras que superan el promedio
    """
    if len(listaTotalCompra) == 0:
        return []
    promedio = sum(listaTotalCompra) / len(listaTotalCompra)
    indices  = list(range(len(listaTotalCompra)))
    return list(filter(lambda i: listaTotalCompra[i] > promedio, indices))

def obtenerNombresEnMayuscula():
    """
    map + lambda: todos los nombres de compradores en mayuscula
    """
    return list(map(lambda nombre: nombre.upper(), listaNombreComprador))

def calcularTotalVentasReduce():
    """
    reduce + lambda: suma total de todas las compras de espectadores
    """
    if len(listaTotalCompra) == 0:
        return 0
    return reduce(lambda acum, x: acum + x, listaTotalCompra)

def reporteFuncional():
    """
    Reporte que muestra en pantalla los resultados de map, filter y reduce
    """
    imprimir_separador("   REPORTE FUNCIONAL (map / filter / reduce)")

    # MAP: recaudacion por pelicula
    recaudaciones = obtenerRecaudacionPorPelicula()
    print("\n[MAP] Recaudacion calculada por pelicula:")
    if len(recaudaciones) == 0:
        print("  Sin peliculas cargadas.")
    else:
        i = 0
        while i < len(peliculas):
            print("  " + peliculas[i] + ": $" + str(recaudaciones[i]))
            i = i + 1

    # FILTER: peliculas con ventas
    indicesConVentas = obtenerPeliculasConVentas()
    print("\n[FILTER] Peliculas con entradas vendidas: " + str(len(indicesConVentas)))
    i = 0
    while i < len(indicesConVentas):
        idx = indicesConVentas[i]
        print("  - " + peliculas[idx] + " (" + str(entradasVendidas[idx]) + " vendidas)")
        i = i + 1

    # REDUCE: total recaudado
    print("\n[REDUCE] Recaudacion total del cine: $" + str(calcularRecaudacionTotalReduce()))

    if len(listaTotalCompra) > 0:
        promedio   = sum(listaTotalCompra) / len(listaTotalCompra)
        superiores = obtenerComprasSuperioresAPromedio()
        print("\n[FILTER] Compras superiores al promedio ($" + str(round(promedio, 2)) + "):")
        if len(superiores) == 0:
            print("  Ninguna compra supera el promedio.")
        else:
            i = 0
            while i < len(superiores):
                idx = superiores[i]
                print("  - " + listaNombreComprador[idx] + ": $" + str(listaTotalCompra[idx]))
                i = i + 1
        print("\n[REDUCE] Total recaudado en ventas al espectador: $" + str(calcularTotalVentasReduce()))

        # MAP: nombres en mayuscula
        nombresMayus = obtenerNombresEnMayuscula()
        print("\n[MAP] Compradores transformados a mayuscula:")
        i = 0
        while i < len(nombresMayus):
            print("  " + str(i + 1) + ". " + nombresMayus[i])
            i = i + 1

    print("\n==========================================")
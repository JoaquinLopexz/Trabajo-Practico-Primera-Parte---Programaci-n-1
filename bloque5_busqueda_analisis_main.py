#    BUSQUEDA Y ANALISIS
def buscarPorNombre(nombre_buscar):
    imprimir_separador("       BUSQUEDA POR NOMBRE")
    if len(dictCompras) == 0:
        print(" No hay registros para buscar.\n==========================================")
        return []
    numeros       = list(dictCompras.keys())
    coincidencias = [k for k in numeros if nombre_buscar.upper() in dictCompras[k]["nombreComprador"].upper()]
    if len(coincidencias) == 0:
        print(" No se encontraron resultados para: '" + nombre_buscar + "'")
    else:
        print(" Se encontraron " + str(len(coincidencias)) + " resultado(s):\n")
        j = 0
        while j < len(coincidencias):
            k = coincidencias[j]
            print("--- Resultado #" + str(j + 1) + " ---")
            print("  Comprador: " + dictCompras[k]["nombreComprador"] + " | Funcion: " + dictCompras[k]["cartelera"])
            print("  Asiento: "   + dictCompras[k]["asiento"] + " | Total: $" + str(dictCompras[k]["total"]) + "\n")
            j = j + 1
    print("==========================================")
    return coincidencias

def buscarPorCodigo(codigo_buscar):
    imprimir_separador("       BUSQUEDA POR CODIGO")
    if len(codigos) == 0:
        print(" No hay peliculas cargadas.\n==========================================")
        return -1
    codigoBuscado  = codigo_buscar.upper()
    horarios_lista = list(dictPeliculas.keys())
    nombres_lista  = list(dictPeliculas.values())
    indice = codigos.index(codigoBuscado) if codigoBuscado in codigos else -1
    if indice == -1:
        print(" No se encontro pelicula con codigo: '" + codigoBuscado + "'")
    else:
        print(" Pelicula encontrada!\n")
        print("  Codigo: "  + codigoBuscado + " | Nombre: " + nombres_lista[indice])
        print("  Sala: "    + str(salas[indice]) + " | Horario: " + horarios_lista[indice])
        print("  Precio: $" + str(precios[indice]) + " | Entradas: " + str(entradasVendidas[indice]))
    print("==========================================")
    return indice

def menuBusqueda():
    imprimir_separador("         SISTEMA DE BUSQUEDA")
    print("1. Buscar compra por nombre de cliente\n2. Buscar pelicula por codigo\n0. Volver")
    print("==========================================")
    opcion = solicitar_numero("Seleccione una opcion: ", 0, 2)
    if opcion == 1:
        buscarPorNombre(solicitar_texto("Ingrese el nombre a buscar: "))
    elif opcion == 2:
        buscarPorCodigo(solicitar_texto("Ingrese el codigo (ej: PELI001): "))

def analisisCompras():
    imprimir_separador("     ANALISIS DE COMPRAS")
    if len(dictCompras) == 0:
        print(" No hay compras registradas.\n==========================================")
        return
    numeros    = list(dictCompras.keys())
    totales    = list(map(lambda k: dictCompras[k]["total"], numeros))
    maximo     = max(totales)
    minimo     = min(totales)
    promedio   = sum(totales) / len(totales)
    suma_total = calcularTotalVentasReduce()
    idx_max    = totales.index(maximo)
    idx_min    = totales.index(minimo)
    k_max      = numeros[idx_max]
    k_min      = numeros[idx_min]

    print(" ESTADISTICAS DE VENTAS:\n")
    print("  Total de compras: "            + str(len(dictCompras)))
    print("  Recaudacion total (reduce): $" + str(suma_total))
    print("  Compra maxima: $"  + str(maximo) + " | Compra minima: $" + str(minimo))
    print("  Promedio por compra: $"        + str(round(promedio, 2)))
    print("\n  COMPRA MAS ALTA: " + dictCompras[k_max]["nombreComprador"] + " ($" + str(maximo) + ")")
    print("  COMPRA MAS BAJA: " + dictCompras[k_min]["nombreComprador"] + " ($" + str(minimo) + ")")
    print("\n==========================================")

def analisisPeliculas():
    imprimir_separador("     ANALISIS DE PELICULAS")
    if len(dictPeliculas) == 0:
        print(" No hay peliculas cargadas.\n==========================================")
        return
    nombres_lista  = list(dictPeliculas.values())
    max_entradas   = max(entradasVendidas)
    min_entradas   = min(entradasVendidas)
    promedio       = sum(entradasVendidas) / len(entradasVendidas)
    total_entradas = reduce(lambda a, b: a + b, entradasVendidas)
    idx_max        = entradasVendidas.index(max_entradas)
    idx_min        = entradasVendidas.index(min_entradas)

    print(" ESTADISTICAS DE PELICULAS:\n")
    print("  Total peliculas: " + str(len(dictPeliculas)) +
          " | Entradas totales (reduce): " + str(total_entradas))
    print("  Maximo: " + str(max_entradas) +
          " | Minimo: " + str(min_entradas) +
          " | Promedio: " + str(round(promedio, 2)))
    print("\n  MAS VENDIDA:   " + nombres_lista[idx_max] + " (" + str(max_entradas) + " entradas)")
    print("  MENOS VENDIDA: " + nombres_lista[idx_min] + " (" + str(min_entradas) + " entradas)")
    print("\n==========================================")

def menuAnalisis():
    imprimir_separador("       SISTEMA DE ANALISIS")
    print("1. Analisis de compras\n2. Analisis de peliculas\n3. Analisis completo\n0. Volver")
    print("==========================================")
    opcion = solicitar_numero("Seleccione una opcion: ", 0, 3)
    if opcion == 1:
        analisisCompras()
    elif opcion == 2:
        analisisPeliculas()
    elif opcion == 3:
        analisisCompras()
        print()
        analisisPeliculas()


#    FUNCION PRINCIPAL
def main():
    print("==========================================")
    print("   BIENVENIDOS A CINE DIGITAL")
    print("==========================================")

    # Cargo todos los datos guardados (si existen)
    cargarCatalogosJSON()    # combos, descuentos, metodos de pago
    cargarCarteleraCSV()     # peliculas
    cargarAsientosCSV()      # asientos ocupados
    cargarComprasJSON()      # compras registradas

    salir = 0
    while salir == 0:
        opcion = menuPrincipal()
        if opcion == 1:
            salirAdmin = 0
            while salirAdmin == 0:
                opcionAdmin = menuAdministrador()
                if opcionAdmin == 1:
                    cargarPeliculas()
                elif opcionAdmin == 2:
                    mostrarCarteleraAdmin()
                elif opcionAdmin == 3:
                    venderEntradasAdmin()
                elif opcionAdmin == 4:
                    verRecaudacion()
                elif opcionAdmin == 5:
                    modificarPelicula()
                elif opcionAdmin == 6:
                    calcularTotales()
                elif opcionAdmin == 7:
                    estadisticasVentas()
                elif opcionAdmin == 8:
                    menuBusqueda()
                elif opcionAdmin == 9:
                    menuAnalisis()
                elif opcionAdmin == 10:
                    reporteFuncional()
                elif opcionAdmin == 11:
                    mostrarAsientosDisponibles()
                elif opcionAdmin == 0:
                    salirAdmin = 1
        elif opcion == 2:
            salirEspectador = 0
            while salirEspectador == 0:
                opcionEspectador = menuEspectador()
                if opcionEspectador == 1:
                    mostrarCarteleraEspectador()
                elif opcionEspectador == 2:
                    continuarComprando = "S"
                    while continuarComprando == "S":
                        resultado = procesarCompra()
                        if resultado == 1:
                            continuarComprando = input("Desea comprar otra entrada? (S/N): ").upper()
                            while continuarComprando != "S" and continuarComprando != "N":
                                continuarComprando = input("Ingrese S o N: ").upper()
                        else:
                            continuarComprando = "N"
                elif opcionEspectador == 3:
                    verHistorialCompras()
                elif opcionEspectador == 4:
                    verHistorialOrdenado()
                elif opcionEspectador == 0:
                    salirEspectador = 1
        elif opcion == 0:
            imprimir_separador("  Gracias por usar Cine Digital!")
            print("          Hasta pronto!")
            print("==========================================")
            salir = 1

main()

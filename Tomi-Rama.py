# ==============================================
#    MENUS PRINCIPALES
# ==============================================

def menuPrincipal():
    imprimir_separador("       SISTEMA INTEGRADO DE CINE")
    print("1. MODO ADMINISTRADOR\n2. MODO ESPECTADOR\n0. Salir")
    print("==========================================")
    return solicitar_numero("Seleccione una opcion: ", 0, 2)

def menuAdministrador():
    imprimir_separador("        MODO ADMINISTRADOR")
    opciones = [
        "Cargar salas y peliculas", "Mostrar cartelera", "Vender entradas",
        "Ver recaudacion por sala y total", "Modificar pelicula", "Calcular totales generales",
        "Estadisticas de ventas", "Busqueda de registros", "Analisis y estadisticas",
        "Reporte funcional (map/filter/reduce)"
    ]
    i = 0
    while i < len(opciones):
        print(str(i + 1) + ". " + opciones[i])
        i = i + 1
    print("0. Volver al menu principal\n==========================================")
    return solicitar_numero("Seleccione una opcion: ", 0, 10)

def menuEspectador():
    imprimir_separador("         MODO ESPECTADOR")
    print("1. Ver Cartelera\n2. Comprar Entrada\n3. Ver Historial de Compras\n4. Ver Historial Ordenado")
    print("0. Volver al menu principal\n==========================================")
    return solicitar_numero("Seleccione una opcion: ", 0, 4)


# ==============================================
#    FUNCIONES ADMINISTRATIVAS
# ==============================================

def generar_codigo_pelicula():
    """
    Genera un codigo unico automatico: PELI001, PELI002, etc.
    """
    numero = len(codigos) + 1
    codigo = "PELI" + str(numero).zfill(3)
    while codigo in codigos:
        numero = numero + 1
        codigo = "PELI" + str(numero).zfill(3)
    return codigo

def cargarPeliculas():
    continuar = "S"
    while continuar == "S":
        imprimir_separador("      CARGANDO NUEVA PELICULA")
        codigo = generar_codigo_pelicula()
        print(" Codigo asignado automaticamente: " + codigo + "\n")

        nombre  = solicitar_nombre_validado("Ingrese el nombre de la pelicula: ")
        sala    = solicitar_numero("Ingrese el numero de sala (1-100): ", 1, 100)
        print(" Precio de entrada (entre $5,000 y $50,000):")
        precio  = solicitar_numero("Ingrese el precio: ", 5000, 50000)
        horario = solicitar_horario_validado("Ingrese el horario (ej: 14:00): ")

        peliculas.append(nombre)
        salas.append(sala)
        precios.append(precio)
        entradasVendidas.append(0)
        codigos.append(codigo)
        horarios.append(horario)

        imprimir_separador("PELICULA CARGADA CORRECTAMENTE")
        print("   Codigo: " + codigo + " | Pelicula: " + nombre)
        print("   Sala: " + str(sala) + " | Horario: " + horario)
        print("   Precio entrada: $" + str(precio))
        print("==========================================")

        continuar = input("Desea agregar otra pelicula? (S/N): ").upper()
        while continuar != "S" and continuar != "N":
            print("ERROR: Opcion invalida. Ingrese S o N.")
            continuar = input("Desea agregar otra pelicula? (S/N): ").upper()

def mostrarCarteleraAdmin():
    imprimir_separador("          CARTELERA - CINE DIGITAL")
    if len(peliculas) == 0:
        print("No hay peliculas cargadas.")
    else:
        print(" PELICULAS CARGADAS:\n")
        i = 0
        while i < len(peliculas):
            print(str(i + 1) + ". " + peliculas[i])
            print("   Codigo: " + codigos[i] + " | Sala: " + str(salas[i]) + " | Horario: " + horarios[i])
            print("   PRECIO: $" + str(precios[i]) + " | Vendidas: " + str(entradasVendidas[i]) + "\n")
            i = i + 1
        print(" Total de peliculas: " + str(len(peliculas)))
    print("==========================================")

def venderEntradasAdmin():
    if len(peliculas) == 0:
        print("No hay peliculas cargadas.")
        return
    mostrarCarteleraAdmin()
    indice   = solicitar_numero("Seleccione el numero de pelicula: ", 1, len(peliculas)) - 1
    cantidad = solicitar_numero("Ingrese la cantidad de entradas a vender: ", 1, 1000)
    entradasVendidas[indice] = entradasVendidas[indice] + cantidad
    print("Se vendieron " + str(cantidad) + " entradas para " + peliculas[indice])

def verRecaudacion():
    imprimir_separador("   RECAUDACION POR SALA Y TOTAL")
    if len(peliculas) == 0:
        print("No hay peliculas cargadas.\n==========================================")
        return

    listaSalas        = []
    listaRecaudacion  = []
    i = 0
    while i < len(peliculas):
        sala        = salas[i]
        recaudacion = entradasVendidas[i] * precios[i]
        if sala in listaSalas:
            indSala = listaSalas.index(sala)
            listaRecaudacion[indSala] = listaRecaudacion[indSala] + recaudacion
        else:
            listaSalas.append(sala)
            listaRecaudacion.append(recaudacion)
        i = i + 1

    indicesOrdenados = sorted(range(len(listaSalas)), key=lambda k: listaSalas[k])
    j = 0
    while j < len(indicesOrdenados):
        idx = indicesOrdenados[j]
        print(" Sala " + str(listaSalas[idx]) + ": $" + str(listaRecaudacion[idx]))
        j = j + 1

    totalGeneral = reduce(lambda acum, x: acum + x, listaRecaudacion)
    print("==========================================")
    print(" TOTAL GENERAL: $" + str(totalGeneral))
    print("==========================================")

def modificarPelicula():
    if len(peliculas) == 0:
        print("No hay peliculas cargadas.")
        return
    mostrarCarteleraAdmin()
    indice = solicitar_numero("Seleccione el numero de pelicula a modificar: ", 1, len(peliculas)) - 1
    print("\nQue desea modificar?\n1. Nombre\n2. Sala\n3. Precio\n4. Horario")
    opcion = solicitar_numero("Seleccione opcion: ", 1, 4)
    if opcion == 1:
        peliculas[indice] = solicitar_nombre_validado("Nuevo nombre: ")
    elif opcion == 2:
        salas[indice] = solicitar_numero("Nueva sala: ", 1, 100)
    elif opcion == 3:
        precios[indice] = solicitar_numero("Nuevo precio: ", 0, 1000000)
    elif opcion == 4:
        horarios[indice] = solicitar_horario_validado("Nuevo horario: ")
    print("Pelicula modificada exitosamente.")

def calcularTotales():
    imprimir_separador("   TOTALES GENERALES DEL SISTEMA")
    if len(peliculas) == 0:
        print("No hay datos para calcular.\n==========================================")
        return
    total_entradas    = sum(entradasVendidas)
    total_recaudacion = calcularRecaudacionTotalReduce()
    print(" Total de peliculas: " + str(len(peliculas)))
    print(" Total de entradas vendidas: " + str(total_entradas))
    print(" Recaudacion total (reduce): $" + str(total_recaudacion))
    print(" Promedio por pelicula: $" + str(round(total_recaudacion / len(peliculas), 2)))
    print("==========================================")

def estadisticasVentas():
    imprimir_separador("   ESTADISTICAS DE VENTAS")
    if len(peliculas) == 0:
        print("No hay datos para analizar.\n==========================================")
        return
    max_ventas = max(entradasVendidas)
    min_ventas = min(entradasVendidas)
    promedio   = sum(entradasVendidas) / len(entradasVendidas)
    idx_max    = entradasVendidas.index(max_ventas)
    idx_min    = entradasVendidas.index(min_ventas)
    print(" Pelicula mas vendida: " + peliculas[idx_max] + " (" + str(max_ventas) + " entradas)")
    print(" Pelicula menos vendida: " + peliculas[idx_min] + " (" + str(min_ventas) + " entradas)")
    print(" Promedio de ventas: " + str(round(promedio, 2)) + " entradas")
    print("==========================================")
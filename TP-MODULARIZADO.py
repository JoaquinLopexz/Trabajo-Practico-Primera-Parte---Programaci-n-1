# ==============================================
#    SISTEMA INTEGRADO DE GESTION DE CINE
#    VERSION FINAL - TRABAJO PRACTICO
# ==============================================

from functools import reduce       # Programacion funcional

# --- DATOS GLOBALES ---
peliculas        = []
salas            = []
precios          = []
entradasVendidas = []
codigos          = []
horarios         = []

listaCartelera         = []
listaAsiento           = []
listaComboCliente      = []
listaDescuentoAplicado = []
listaMetodoPago        = []
listaTotalCompra       = []
listaNombreComprador   = []

# ==============================================
#    MATRIZ DE ASIENTOS (lista bidimensional)
#    10 filas (A-J) x 10 columnas (1-10)
#    0 = disponible | 1 = ocupado
# ==============================================
FILAS_ASIENTOS    = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
COLUMNAS_ASIENTOS = 10

# Inicializar matriz 10x10 en 0
matrizAsientos = []
i = 0
while i < len(FILAS_ASIENTOS):
    fila = []
    j = 0
    while j < COLUMNAS_ASIENTOS:
        fila.append(0)
        j = j + 1
    matrizAsientos.append(fila)
    i = i + 1

# Combos disponibles
listaNombreCombo = [
    "Sin combo", "COMBO MEGA FIESTA DEL CINE", "COMBO FIESTA",
    "COMBOS NACOS FIESTA DEL CINE", "COMBO SUPERMAN", "COMBO LOS 4 FANTASTICOS",
    "BALDE POCHOCLOS", "POP MEDIANO", "BEBIDA GRANDE", "BEBIDA MEDIANA",
    "AGUA", "AGUA SABORIZADA", "MOGUL", "CHOCO-PAUSE",
    "M&M GRANDE", "M&M CHICO", "SKITTLES GRANDE", "SKITTLES MEDIANOS"
]
listaPrecioCombo = [0, 20000, 12000, 12000, 24900, 24900, 9800, 8000, 7800,
                    7000, 4000, 4800, 5000, 3500, 10000, 5900, 9800, 5800]

listaTipoDescuento = [
    "Sin descuento", "Primer Lunes del Mes", "Segundo Lunes del Mes",
    "Miercoles de Cine", "Tarjeta Visa", "Tarjeta Mastercard",
    "Tarjeta American Express", "Tarjeta Naranja"
]
listaPorcentajeDescuento = [0.0, 0.30, 0.30, 0.25, 0.15, 0.15, 0.20, 0.10]
listaMetodosPago = ["Billeteras virtuales", "Efectivo", "Visa", "Mastercard", "Credito", "Debito"]
PRECIO_ENTRADA = 10000


# ==============================================
#    FUNCIONES AUXILIARES
# ==============================================

def solicitar_numero(mensaje, minimo, maximo):
    """
    Solicita un numero validado entre minimo y maximo
    """
    while True:
        entrada = input(mensaje).strip()
        if len(entrada) == 0:
            print("ERROR: no puede estar vacio.")
        elif entrada.isdigit():
            numero = int(entrada)
            if minimo <= numero <= maximo:
                return numero
            print("ERROR: debe estar entre " + str(minimo) + " y " + str(maximo))
        else:
            print("ERROR: debe ingresar un numero.")

def solicitar_texto(mensaje):
    """
    Solicita un texto no vacio
    """
    texto = input(mensaje).strip()
    while len(texto) == 0:
        print("ERROR: no puede estar vacio.")
        texto = input(mensaje).strip()
    return texto

def solicitar_opcion_lista(mensaje, lista):
    """
    Solicita seleccionar un elemento de una lista
    """
    return solicitar_numero(mensaje, 1, len(lista)) - 1

def imprimir_separador(titulo):
    """
    Imprime un separador con titulo
    """
    print("==========================================")
    print(titulo)
    print("==========================================")

def buscar_en_lista(lista, valor):
    """
    Retorna el indice del valor en la lista, o -1 si no existe
    """
    return lista.index(valor) if valor in lista else -1

def solo_letras_y_espacios(texto):
    """
    Valida que el texto tenga solo letras y espacios, sin numeros ni simbolos
    """
    i = 0
    while i < len(texto):
        caracter = texto[i]
        esLetra = (caracter >= "a" and caracter <= "z") or (caracter >= "A" and caracter <= "Z")
        esEspacio = caracter == " "
        if not esLetra and not esEspacio:
            return False
        i = i + 1
    return True

def validar_horario(horario):
    """
    Valida que el horario tenga formato HH:MM
    """
    if len(horario) != 5:
        return False
    if horario[2] != ":":
        return False
    horas   = horario[0:2]
    minutos = horario[3:5]
    if not horas.isdigit() or not minutos.isdigit():
        return False
    if int(horas) < 0 or int(horas) > 23:
        return False
    if int(minutos) < 0 or int(minutos) > 59:
        return False
    return True

def validar_asiento(asiento):
    """
    Valida que el asiento tenga formato correcto: letra A-J + numero 1-10
    """
    if len(asiento) < 2 or len(asiento) > 3:
        return False
    letra  = asiento[0]
    numero = asiento[1:]
    if letra not in FILAS_ASIENTOS:
        return False
    if not numero.isdigit():
        return False
    if int(numero) < 1 or int(numero) > 10:
        return False
    return True

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


# ==============================================
#    FUNCIONES DEL ESPECTADOR
# ==============================================

def mostrarCarteleraEspectador():
    imprimir_separador("        CARTELERA DISPONIBLE")
    if len(peliculas) == 0:
        print("No hay peliculas disponibles. El administrador debe cargarlas primero.")
    else:
        i = 0
        while i < len(peliculas):
            print(str(i + 1) + ". " + peliculas[i] +
                  " | Sala " + str(salas[i]) +
                  " | Horario: " + horarios[i] +
                  " | Precio: $" + str(precios[i]))
            i = i + 1
        print(" Total de funciones: " + str(len(peliculas)))
    print("==========================================")

def elegirFuncion():
    """
    Muestra cartelera al espectador y retorna la funcion elegida
    """
    imprimir_separador('        CARTELERA DISPONIBLE')
    if len(peliculas) == 0:
        print('No hay peliculas disponibles.\n==========================================')
        return '', 0, '', ''
    i = 0
    while i < len(peliculas):
        print(str(i + 1) + '. ' + peliculas[i] +
              ' | Sala ' + str(salas[i]) +
              ' | Horario: ' + horarios[i] +
              ' | Precio: $' + str(precios[i]))
        i = i + 1
    print('==========================================')
    indice = solicitar_numero('Seleccione el numero de pelicula: ', 1, len(peliculas)) - 1
    funcionElegida = peliculas[indice] + ' | Sala ' + str(salas[indice]) + ' | ' + horarios[indice]
    print(' Funcion seleccionada: ' + funcionElegida)
    return funcionElegida, salas[indice], peliculas[indice], horarios[indice]

def seleccionarAsiento(numeroSala, nombrePelicula, horario):
    imprimir_separador("       SELECCION DE ASIENTO")
    print(" Sala " + str(numeroSala) + " - Asientos: A1 a J10\n")
    mostrarMapaAsientos()
    print()
    asiento = solicitar_asiento_validado()
    while esta_asiento_ocupado(asiento):
        print(" El asiento " + asiento + " ya esta ocupado.")
        asiento = solicitar_asiento_validado()
    print("\n Asiento " + asiento + " seleccionado")
    return asiento

def elegirCombo():
    imprimir_separador("       SELECCION DE COMBO")
    i = 0
    while i < len(listaNombreCombo):
        print(str(i + 1) + ". " + listaNombreCombo[i] + " - $" + str(listaPrecioCombo[i]))
        i = i + 1
    print("==========================================")
    indice = solicitar_opcion_lista("Seleccione el numero de combo: ", listaNombreCombo)
    print(" Combo seleccionado: " + listaNombreCombo[indice])
    return listaNombreCombo[indice], listaPrecioCombo[indice]

def aplicarDescuento():
    imprimir_separador("       APLICAR DESCUENTO")
    i = 0
    while i < len(listaTipoDescuento):
        print(str(i + 1) + ". " + listaTipoDescuento[i] +
              " (" + str(int(listaPorcentajeDescuento[i] * 100)) + "%)")
        i = i + 1
    print("==========================================")
    indice = solicitar_opcion_lista("Seleccione el descuento: ", listaTipoDescuento)
    print(" Descuento aplicado: " + listaTipoDescuento[indice])
    return listaTipoDescuento[indice], listaPorcentajeDescuento[indice]

def seleccionarMetodoPago():
    imprimir_separador("       METODO DE PAGO")
    i = 0
    while i < len(listaMetodosPago):
        print(str(i + 1) + ". " + listaMetodosPago[i])
        i = i + 1
    print("==========================================")
    indice = solicitar_opcion_lista("Seleccione el metodo de pago: ", listaMetodosPago)
    return listaMetodosPago[indice]

def calcularTotal(precioCombo, porcentajeDescuento, metodoPago):
    subtotal  = PRECIO_ENTRADA + precioCombo
    descuento = subtotal * porcentajeDescuento
    recargo   = subtotal * 0.10 if metodoPago == "Credito" else 0
    total     = subtotal - descuento + recargo
    return subtotal, descuento, recargo, total

def confirmarCompra(funcionElegida, asiento, comboElegido, descuentoElegido, metodoPago,
                    subtotal, descuento, recargo, total, nombreComprador,
                    nombrePelicula, numeroSala, horario):
    imprimir_separador(" RESUMEN DE TU COMPRA")
    print("  Pelicula: " + funcionElegida)
    print("  Asiento: " + asiento)
    print("  Combo: " + comboElegido)
    print("  Descuento: " + descuentoElegido)
    print("  Metodo de pago: " + metodoPago)
    print("\n  Subtotal: $" + str(subtotal))
    print("  Descuento: -$" + str(round(descuento, 2)))
    if recargo > 0:
        print("  Recargo credito: +$" + str(round(recargo, 2)))
    print("  TOTAL: $" + str(round(total, 2)))
    print("==========================================")

    confirmacion = input("Confirmar compra? (S/N): ").upper()
    while confirmacion != "S" and confirmacion != "N":
        confirmacion = input("Ingrese S o N: ").upper()

    if confirmacion == "S":
        listaCartelera.append(funcionElegida)
        listaAsiento.append(asiento)
        listaComboCliente.append(comboElegido)
        listaDescuentoAplicado.append(descuentoElegido)
        listaMetodoPago.append(metodoPago)
        listaTotalCompra.append(round(total, 2))
        listaNombreComprador.append(nombreComprador)
        marcar_asiento_ocupado(asiento)

        imprimir_separador(" COMPRA REALIZADA CON EXITO!")
        print("   Ticket registrado | Asiento " + asiento + " reservado")
        print("   Disfruta tu pelicula, " + nombreComprador + "!")
        print("==========================================")
        return 1
    else:
        imprimir_separador(" COMPRA CANCELADA")
        print("   No se realizo ningun cargo\n==========================================")
        return 0

def procesarCompra():
    if len(peliculas) == 0:
        print("No hay peliculas disponibles.")
        return 0
    nombreComprador = solicitar_nombre_validado("Ingrese su nombre completo: ")
    funcionElegida, numeroSala, nombrePelicula, horario = elegirFuncion()
    if funcionElegida == '':
        return 0
    asiento                             = seleccionarAsiento(numeroSala, nombrePelicula, horario)
    comboElegido, precioCombo           = elegirCombo()
    descuentoElegido, pctDescuento      = aplicarDescuento()
    metodoPago                          = seleccionarMetodoPago()
    subtotal, descuento, recargo, total = calcularTotal(precioCombo, pctDescuento, metodoPago)
    return confirmarCompra(funcionElegida, asiento, comboElegido, descuentoElegido, metodoPago,
                           subtotal, descuento, recargo, total, nombreComprador,
                           nombrePelicula, numeroSala, horario)

def verHistorialCompras():
    imprimir_separador("       HISTORIAL DE COMPRAS")
    if len(listaCartelera) == 0:
        print(" No hay compras registradas.")
    else:
        i = 0
        while i < len(listaCartelera):
            print("--- Compra #" + str(i + 1) + " ---")
            print("  Comprador: " + listaNombreComprador[i] + " | Funcion: " + listaCartelera[i])
            print("  Asiento: " + listaAsiento[i] + " | Combo: " + listaComboCliente[i])
            print("  Descuento: " + listaDescuentoAplicado[i] +
                  " | Pago: " + listaMetodoPago[i] +
                  " | Total: $" + str(listaTotalCompra[i]) + "\n")
            i = i + 1
        print(" Total de compras: " + str(len(listaCartelera)))
    print("==========================================")

def verHistorialOrdenado():
    """
    Ordena el historial por nombre usando sorted() con lambda
    """
    imprimir_separador("   HISTORIAL ORDENADO POR COMPRADOR")
    if len(listaCartelera) == 0:
        print(" No hay compras registradas.\n==========================================")
        return
    indicesOrdenados = sorted(range(len(listaNombreComprador)),
                              key=lambda i: listaNombreComprador[i].upper())
    i = 0
    while i < len(indicesOrdenados):
        idx = indicesOrdenados[i]
        print("--- Compra #" + str(i + 1) + " ---")
        print("  Comprador: " + listaNombreComprador[idx] + " | Funcion: " + listaCartelera[idx])
        print("  Asiento: " + listaAsiento[idx] + " | Combo: " + listaComboCliente[idx])
        print("  Descuento: " + listaDescuentoAplicado[idx] +
              " | Pago: " + listaMetodoPago[idx] +
              " | Total: $" + str(listaTotalCompra[idx]) + "\n")
        i = i + 1
    print(" Total de compras: " + str(len(listaCartelera)))
    print("==========================================")


# ==============================================
#    BUSQUEDA Y ANALISIS
# ==============================================

def buscarPorNombre(nombre_buscar):
    imprimir_separador("       BUSQUEDA POR NOMBRE")
    if len(listaNombreComprador) == 0:
        print(" No hay registros para buscar.\n==========================================")
        return []
    coincidencias = [i for i in range(len(listaNombreComprador))
                     if nombre_buscar.upper() in listaNombreComprador[i].upper()]
    if len(coincidencias) == 0:
        print(" No se encontraron resultados para: '" + nombre_buscar + "'")
    else:
        print(" Se encontraron " + str(len(coincidencias)) + " resultado(s):\n")
        j = 0
        while j < len(coincidencias):
            idx = coincidencias[j]
            print("--- Resultado #" + str(j + 1) + " ---")
            print("  Comprador: " + listaNombreComprador[idx] + " | Funcion: " + listaCartelera[idx])
            print("  Asiento: " + listaAsiento[idx] + " | Total: $" + str(listaTotalCompra[idx]) + "\n")
            j = j + 1
    print("==========================================")
    return coincidencias

def buscarPorCodigo(codigo_buscar):
    imprimir_separador("       BUSQUEDA POR CODIGO")
    if len(codigos) == 0:
        print(" No hay peliculas cargadas.\n==========================================")
        return -1
    codigoBuscado = codigo_buscar.upper()
    indice = codigos.index(codigoBuscado) if codigoBuscado in codigos else -1
    if indice == -1:
        print(" No se encontro pelicula con codigo: '" + codigoBuscado + "'")
    else:
        print(" Pelicula encontrada!\n")
        print("  Codigo: " + codigos[indice] + " | Nombre: " + peliculas[indice])
        print("  Sala: " + str(salas[indice]) + " | Horario: " + horarios[indice])
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
    if len(listaTotalCompra) == 0:
        print(" No hay compras registradas.\n==========================================")
        return
    maximo     = max(listaTotalCompra)
    minimo     = min(listaTotalCompra)
    promedio   = sum(listaTotalCompra) / len(listaTotalCompra)
    suma_total = calcularTotalVentasReduce()
    idx_max    = listaTotalCompra.index(maximo)
    idx_min    = listaTotalCompra.index(minimo)

    print(" ESTADISTICAS DE VENTAS:\n")
    print("  Total de compras: " + str(len(listaTotalCompra)))
    print("  Recaudacion total (reduce): $" + str(suma_total))
    print("  Compra maxima: $" + str(maximo) + " | Compra minima: $" + str(minimo))
    print("  Promedio por compra: $" + str(round(promedio, 2)))
    print("\n  COMPRA MAS ALTA: " + listaNombreComprador[idx_max] + " ($" + str(maximo) + ")")
    print("  COMPRA MAS BAJA: " + listaNombreComprador[idx_min] + " ($" + str(minimo) + ")")
    print("\n==========================================")

def analisisPeliculas():
    imprimir_separador("     ANALISIS DE PELICULAS")
    if len(peliculas) == 0:
        print(" No hay peliculas cargadas.\n==========================================")
        return
    max_entradas   = max(entradasVendidas)
    min_entradas   = min(entradasVendidas)
    promedio       = sum(entradasVendidas) / len(entradasVendidas)
    total_entradas = reduce(lambda a, b: a + b, entradasVendidas)
    idx_max        = entradasVendidas.index(max_entradas)
    idx_min        = entradasVendidas.index(min_entradas)

    print(" ESTADISTICAS DE PELICULAS:\n")
    print("  Total peliculas: " + str(len(peliculas)) +
          " | Entradas totales (reduce): " + str(total_entradas))
    print("  Maximo: " + str(max_entradas) +
          " | Minimo: " + str(min_entradas) +
          " | Promedio: " + str(round(promedio, 2)))
    print("\n  MAS VENDIDA: " + peliculas[idx_max] + " (" + str(max_entradas) + " entradas)")
    print("  MENOS VENDIDA: " + peliculas[idx_min] + " (" + str(min_entradas) + " entradas)")
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


# ==============================================
#    FUNCION PRINCIPAL
# ==============================================

def main():
    print("==========================================")
    print("   BIENVENIDOS A CINE DIGITAL")
    print("==========================================")
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

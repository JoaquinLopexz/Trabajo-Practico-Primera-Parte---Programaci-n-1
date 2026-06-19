from functools import reduce   
import csv                      
import json                       

#    BLOQUE 1 - CARTELERA 
# key: horario (str, ej: "14:00") | value: nombre de la pelicula (str)
dictPeliculas    = {}

# Listas paralelas a dictPeliculas (mismo indice = misma pelicula)
salas            = []
precios          = []
entradasVendidas = []
codigos          = []


#    BLOQUE 2 - ASIENTOS 
FILAS_ASIENTOS    = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
COLUMNAS_ASIENTOS = 10

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

#    BLOQUE 3 - COMPRAS 
dictCompras = {}

#    BLOQUE 4 - CATALOGOS / CONFIGURACION
# key: nombre del combo | value: precio
dictCombos = {
    "Sin combo"                    : 0,
    "COMBO MEGA FIESTA DEL CINE"   : 20000,
    "COMBO FIESTA"                 : 12000,
    "COMBOS NACOS FIESTA DEL CINE" : 12000,
    "COMBO SUPERMAN"               : 24900,
    "COMBO LOS 4 FANTASTICOS"      : 24900,
    "BALDE POCHOCLOS"              : 9800,
    "POP MEDIANO"                  : 8000,
    "BEBIDA GRANDE"                : 7800,
    "BEBIDA MEDIANA"               : 7000,
    "AGUA"                         : 4000,
    "AGUA SABORIZADA"              : 4800,
    "MOGUL"                        : 5000,
    "CHOCO-PAUSE"                  : 3500,
    "M&M GRANDE"                   : 10000,
    "M&M CHICO"                    : 5900,
    "SKITTLES GRANDE"              : 9800,
    "SKITTLES MEDIANOS"            : 5800
}

# key: tipo de descuento | value: porcentaje (float)
dictDescuentos = {
    "Sin descuento"            : 0.0,
    "Primer Lunes del Mes"     : 0.30,
    "Segundo Lunes del Mes"    : 0.30,
    "Miercoles de Cine"        : 0.25,
    "Tarjeta Visa"             : 0.15,
    "Tarjeta Mastercard"       : 0.15,
    "Tarjeta American Express" : 0.20,
    "Tarjeta Naranja"          : 0.10
}

# metodos de pago disponibles
listaMetodosPago = ["Billeteras virtuales", "Efectivo", "Visa", "Mastercard", "Credito", "Debito"]

# precio fijo de la entrada
PRECIO_ENTRADA   = 10000


#    FUNCIONES AUXILIARES
def solicitar_numero(mensaje, minimo, maximo):
    """
    Solicita un numero validado entre minimo y maximo
    """
    while True:
        entrada = input(mensaje).strip()
        if len(entrada) == 0:
            print("ERROR: no puede estar vacio.")
        else:
            try:
                numero = int(entrada)
                if minimo <= numero <= maximo:
                    return numero
                print("ERROR: debe estar entre " + str(minimo) + " y " + str(maximo))
            except ValueError:
                print("ERROR: debe ingresar un numero entero valido.")

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

def solo_letras_y_espacios(texto):
    """
    Valida que el texto tenga solo letras y espacios, sin numeros ni simbolos
    """
    i = 0
    while i < len(texto):
        caracter  = texto[i]
        esLetra   = (caracter >= "a" and caracter <= "z") or (caracter >= "A" and caracter <= "Z")
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


#    MENUS PRINCIPALES
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
        "Reporte funcional (map/filter/reduce)", "Asientos disponibles (conjuntos)"
    ]
    i = 0
    while i < len(opciones):
        print(str(i + 1) + ". " + opciones[i])
        i = i + 1
    print("0. Volver al menu principal\n==========================================")
    return solicitar_numero("Seleccione una opcion: ", 0, 11)

def menuEspectador():
    imprimir_separador("         MODO ESPECTADOR")
    print("1. Ver Cartelera\n2. Comprar Entrada\n3. Ver Historial de Compras\n4. Ver Historial Ordenado")
    print("0. Volver al menu principal\n==========================================")
    return solicitar_numero("Seleccione una opcion: ", 0, 4)


#    CARTELERA
#    Lo escribe el ADMINISTRADOR, lo lee el ESPECTADOR.

def guardarCarteleraCSV():
    """
    Guarda toda la cartelera en cartelera.csv (modo "w" -> pisa todo).
    Cada fila: horario, nombre, sala, precio, entradas, codigo
    """
    archivo  = open("cartelera.csv", "w", newline="", encoding="utf-8")
    escritor = csv.writer(archivo)
    escritor.writerow(["horario", "nombre", "sala", "precio", "entradas", "codigo"])

    horarios = list(dictPeliculas.keys())
    i = 0
    while i < len(horarios):
        horario = horarios[i]
        nombre  = dictPeliculas[horario]
        escritor.writerow([horario, nombre, salas[i], precios[i], entradasVendidas[i], codigos[i]])
        i = i + 1

    archivo.close()

def cargarCarteleraCSV():
    """
    Lee cartelera.csv y carga los datos en memoria.
    Si el archivo todavia no existe (primera ejecucion), no hace nada.
    """
    try:
        archivo = open("cartelera.csv", "r", newline="", encoding="utf-8")
        lector  = csv.reader(archivo)

        # vacio las estructuras para no duplicar al cargar
        dictPeliculas.clear()
        salas.clear()
        precios.clear()
        entradasVendidas.clear()
        codigos.clear()

        primera = True
        for fila in lector:
            if primera == True:
                primera = False            # salteo la linea de encabezado
            elif len(fila) == 6:
                horario  = fila[0]
                nombre   = fila[1]
                sala     = int(fila[2])
                precio   = int(fila[3])
                entradas = int(fila[4])
                codigo   = fila[5]

                dictPeliculas[horario] = nombre
                salas.append(sala)
                precios.append(precio)
                entradasVendidas.append(entradas)
                codigos.append(codigo)

        archivo.close()
    except FileNotFoundError:
        print(" (No hay cartelera guardada todavia - primera ejecucion)")


#    ASIENTOS
#    Matriz 10x10 (0 = libre, 1 = ocupado).
#    La actualiza el ESPECTADOR al comprar.
def guardarAsientosCSV():
    """
    Guarda la matriz de asientos en asientos.csv (una fila por linea).
    """
    archivo  = open("asientos.csv", "w", newline="", encoding="utf-8")
    escritor = csv.writer(archivo)
    i = 0
    while i < len(matrizAsientos):
        escritor.writerow(matrizAsientos[i])
        i = i + 1
    archivo.close()

def cargarAsientosCSV():
    """
    Lee asientos.csv y actualiza la matriz en memoria.
    Si todavia no existe, deja la matriz vacia (todo libre).
    """
    try:
        archivo = open("asientos.csv", "r", newline="", encoding="utf-8")
        lector  = csv.reader(archivo)
        i = 0
        for fila in lector:
            j = 0
            while j < len(fila):
                matrizAsientos[i][j] = int(fila[j])
                j = j + 1
            i = i + 1
        archivo.close()
    except FileNotFoundError:
        pass    # primera vez: la matriz queda en 0 (todo libre)


#    COMPRAS
#    Estructura anidada se guarda con JSON.
#    Lo escribe el ESPECTADOR, lo lee el ADMINISTRADOR.
def guardarComprasJSON():
    """
    Guarda el diccionario de compras en compras.json.
    """
    archivo = open("compras.json", "w", encoding="utf-8")
    json.dump(dictCompras, archivo, indent=4, ensure_ascii=False)
    archivo.close()

def cargarComprasJSON():
    """
    Lee compras.json y carga las compras en memoria.
    Las claves vuelven como texto desde JSON, asi que las paso a int.
    """
    try:
        archivo = open("compras.json", "r", encoding="utf-8")
        datos   = json.load(archivo)
        archivo.close()
        dictCompras.clear()
        for clave in datos:
            dictCompras[int(clave)] = datos[clave]
    except FileNotFoundError:
        pass    # primera vez: no hay compras todavia

#    CATALOGOS
#    Datos fijos: combos, descuentos y metodos de pago.

def guardarCatalogosJSON():
    """
    Guarda los catalogos (combos, descuentos, metodos) en catalogos.json.
    """
    catalogos = {
        "combos"      : dictCombos,
        "descuentos"  : dictDescuentos,
        "metodosPago" : listaMetodosPago
    }
    archivo = open("catalogos.json", "w", encoding="utf-8")
    json.dump(catalogos, archivo, indent=4, ensure_ascii=False)
    archivo.close()

def cargarCatalogosJSON():
    """
    Lee catalogos.json. Si no existe, lo crea con los valores por defecto.
    """
    try:
        archivo   = open("catalogos.json", "r", encoding="utf-8")
        catalogos = json.load(archivo)
        archivo.close()

        dictCombos.clear()
        dictCombos.update(catalogos["combos"])
        dictDescuentos.clear()
        dictDescuentos.update(catalogos["descuentos"])
        listaMetodosPago.clear()
        listaMetodosPago.extend(catalogos["metodosPago"])
    except FileNotFoundError:
        guardarCatalogosJSON()    # primera vez: creo el archivo con los valores fijos


#    FUNCIONES ADMINISTRATIVAS
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

        dictPeliculas[horario] = nombre
        salas.append(sala)
        precios.append(precio)
        entradasVendidas.append(0)
        codigos.append(codigo)

        imprimir_separador("PELICULA CARGADA CORRECTAMENTE")
        print("   Codigo: " + codigo + " | Pelicula: " + nombre)
        print("   Sala: " + str(sala) + " | Horario: " + horario)
        print("   Precio entrada: $" + str(precio))
        print("==========================================")

        continuar = input("Desea agregar otra pelicula? (S/N): ").upper()
        while continuar != "S" and continuar != "N":
            print("ERROR: Opcion invalida. Ingrese S o N.")
            continuar = input("Desea agregar otra pelicula? (S/N): ").upper()

    guardarCarteleraCSV()    # persisto la cartelera en disco
    print(" Cartelera guardada en cartelera.csv")

def mostrarCarteleraAdmin():
    imprimir_separador("          CARTELERA - CINE DIGITAL")
    if len(dictPeliculas) == 0:
        print("No hay peliculas cargadas.")
    else:
        print(" PELICULAS CARGADAS:\n")
        horarios_lista = list(dictPeliculas.keys())
        nombres_lista  = list(dictPeliculas.values())
        i = 0
        while i < len(horarios_lista):
            print(str(i + 1) + ". " + nombres_lista[i])
            print("   Codigo: " + codigos[i] + " | Sala: " + str(salas[i]) + " | Horario: " + horarios_lista[i])
            print("   PRECIO: $" + str(precios[i]) + " | Vendidas: " + str(entradasVendidas[i]) + "\n")
            i = i + 1
        print(" Total de peliculas: " + str(len(dictPeliculas)))
    print("==========================================")

def venderEntradasAdmin():
    if len(dictPeliculas) == 0:
        print("No hay peliculas cargadas.")
        return
    mostrarCarteleraAdmin()
    nombres_lista = list(dictPeliculas.values())
    indice   = solicitar_numero("Seleccione el numero de pelicula: ", 1, len(dictPeliculas)) - 1
    cantidad = solicitar_numero("Ingrese la cantidad de entradas a vender: ", 1, 1000)
    entradasVendidas[indice] = entradasVendidas[indice] + cantidad
    print("Se vendieron " + str(cantidad) + " entradas para " + nombres_lista[indice])
    guardarCarteleraCSV()    # actualizo el CSV con las nuevas ventas

def verRecaudacion():
    imprimir_separador("   RECAUDACION POR SALA Y TOTAL")
    if len(dictPeliculas) == 0:
        print("No hay peliculas cargadas.\n==========================================")
        return

    dictRecaudacionPorSala = {}
    i = 0
    while i < len(salas):
        sala        = salas[i]
        recaudacion = entradasVendidas[i] * precios[i]
        if sala in dictRecaudacionPorSala:
            dictRecaudacionPorSala[sala] = dictRecaudacionPorSala[sala] + recaudacion
        else:
            dictRecaudacionPorSala[sala] = recaudacion
        i = i + 1

    salasOrdenadas = sorted(dictRecaudacionPorSala.keys())
    j = 0
    while j < len(salasOrdenadas):
        sala = salasOrdenadas[j]
        print(" Sala " + str(sala) + ": $" + str(dictRecaudacionPorSala[sala]))
        j = j + 1

    listaRecaudaciones = list(dictRecaudacionPorSala.values())
    totalGeneral = reduce(lambda acum, x: acum + x, listaRecaudaciones)
    print("==========================================")
    print(" TOTAL GENERAL: $" + str(totalGeneral))
    print("==========================================")

def modificarPelicula():
    if len(dictPeliculas) == 0:
        print("No hay peliculas cargadas.")
        return
    mostrarCarteleraAdmin()
    horarios_lista = list(dictPeliculas.keys())
    indice = solicitar_numero("Seleccione el numero de pelicula a modificar: ", 1, len(dictPeliculas)) - 1
    print("\nQue desea modificar?\n1. Nombre\n2. Sala\n3. Precio\n4. Horario")
    opcion = solicitar_numero("Seleccione opcion: ", 1, 4)
    if opcion == 1:
        nuevoNombre    = solicitar_nombre_validado("Nuevo nombre: ")
        horario_actual = horarios_lista[indice]
        dictPeliculas[horario_actual] = nuevoNombre
    elif opcion == 2:
        salas[indice]   = solicitar_numero("Nueva sala: ", 1, 100)
    elif opcion == 3:
        precios[indice] = solicitar_numero("Nuevo precio: ", 0, 1000000)
    elif opcion == 4:
        nuevoHorario   = solicitar_horario_validado("Nuevo horario: ")
        horario_actual = horarios_lista[indice]
        nombre_actual  = dictPeliculas[horario_actual]
        del dictPeliculas[horario_actual]
        dictPeliculas[nuevoHorario] = nombre_actual
    print("Pelicula modificada exitosamente.")
    guardarCarteleraCSV()    # actualizo el CSV con la modificacion

def calcularTotales():
    imprimir_separador("   TOTALES GENERALES DEL SISTEMA")
    if len(dictPeliculas) == 0:
        print("No hay datos para calcular.\n==========================================")
        return
    total_entradas    = sum(entradasVendidas)
    total_recaudacion = calcularRecaudacionTotalReduce()
    print(" Total de peliculas: " + str(len(dictPeliculas)))
    print(" Total de entradas vendidas: " + str(total_entradas))
    print(" Recaudacion total (reduce): $" + str(total_recaudacion))
    print(" Promedio por pelicula: $" + str(round(total_recaudacion / len(dictPeliculas), 2)))
    print("==========================================")

def estadisticasVentas():
    imprimir_separador("   ESTADISTICAS DE VENTAS")
    if len(dictPeliculas) == 0:
        print("No hay datos para analizar.\n==========================================")
        return
    nombres_lista = list(dictPeliculas.values())
    max_ventas = max(entradasVendidas)
    min_ventas = min(entradasVendidas)
    promedio   = sum(entradasVendidas) / len(entradasVendidas)
    idx_max    = entradasVendidas.index(max_ventas)
    idx_min    = entradasVendidas.index(min_ventas)
    print(" Pelicula mas vendida:   " + nombres_lista[idx_max] + " (" + str(max_ventas) + " entradas)")
    print(" Pelicula menos vendida: " + nombres_lista[idx_min] + " (" + str(min_ventas) + " entradas)")
    print(" Promedio de ventas: " + str(round(promedio, 2)) + " entradas")
    print("==========================================")


#    FUNCIONES DEL ESPECTADOR
def mostrarCarteleraEspectador():
    imprimir_separador("        CARTELERA DISPONIBLE")
    if len(dictPeliculas) == 0:
        print("No hay peliculas disponibles. El administrador debe cargarlas primero.")
    else:
        horarios_lista = list(dictPeliculas.keys())
        nombres_lista  = list(dictPeliculas.values())
        i = 0
        while i < len(horarios_lista):
            print(str(i + 1) + ". " + nombres_lista[i] +
                  " | Sala " + str(salas[i]) +
                  " | Horario: " + horarios_lista[i] +
                  " | Precio: $" + str(precios[i]))
            i = i + 1
        print(" Total de funciones: " + str(len(dictPeliculas)))
    print("==========================================")

def elegirFuncion():
    """
    Muestra cartelera al espectador y retorna la funcion elegida
    """
    imprimir_separador("        CARTELERA DISPONIBLE")
    if len(dictPeliculas) == 0:
        print("No hay peliculas disponibles.\n==========================================")
        return "", 0, "", ""
    horarios_lista = list(dictPeliculas.keys())
    nombres_lista  = list(dictPeliculas.values())
    i = 0
    while i < len(horarios_lista):
        print(str(i + 1) + ". " + nombres_lista[i] +
              " | Sala " + str(salas[i]) +
              " | Horario: " + horarios_lista[i] +
              " | Precio: $" + str(precios[i]))
        i = i + 1
    print("==========================================")
    indice         = solicitar_numero("Seleccione el numero de pelicula: ", 1, len(dictPeliculas)) - 1
    funcionElegida = nombres_lista[indice] + " | Sala " + str(salas[indice]) + " | " + horarios_lista[indice]
    print(" Funcion seleccionada: " + funcionElegida)
    return funcionElegida, salas[indice], nombres_lista[indice], horarios_lista[indice]

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
    nombresCombo = list(dictCombos.keys())
    preciosCombo = list(dictCombos.values())
    i = 0
    while i < len(nombresCombo):
        print(str(i + 1) + ". " + nombresCombo[i] + " - $" + str(preciosCombo[i]))
        i = i + 1
    print("==========================================")
    indice             = solicitar_opcion_lista("Seleccione el numero de combo: ", nombresCombo)
    nombreSeleccionado = nombresCombo[indice]
    print(" Combo seleccionado: " + nombreSeleccionado)
    return nombreSeleccionado, dictCombos[nombreSeleccionado]

def aplicarDescuento():
    imprimir_separador("       APLICAR DESCUENTO")
    tiposDescuento = list(dictDescuentos.keys())
    i = 0
    while i < len(tiposDescuento):
        tipo = tiposDescuento[i]
        print(str(i + 1) + ". " + tipo + " (" + str(int(dictDescuentos[tipo] * 100)) + "%)")
        i = i + 1
    print("==========================================")
    indice           = solicitar_opcion_lista("Seleccione el descuento: ", tiposDescuento)
    tipoSeleccionado = tiposDescuento[indice]
    print(" Descuento aplicado: " + tipoSeleccionado)
    return tipoSeleccionado, dictDescuentos[tipoSeleccionado]

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
    print("  Pelicula: "       + funcionElegida)
    print("  Asiento: "        + asiento)
    print("  Combo: "          + comboElegido)
    print("  Descuento: "      + descuentoElegido)
    print("  Metodo de pago: " + metodoPago)
    print("\n  Subtotal: $"    + str(subtotal))
    print("  Descuento: -$"   + str(round(descuento, 2)))
    if recargo > 0:
        print("  Recargo credito: +$" + str(round(recargo, 2)))
    print("  TOTAL: $"        + str(round(total, 2)))
    print("==========================================")

    confirmacion = input("Confirmar compra? (S/N): ").upper()
    while confirmacion != "S" and confirmacion != "N":
        confirmacion = input("Ingrese S o N: ").upper()

    if confirmacion == "S":
        numeroCompra = len(dictCompras) + 1
        dictCompras[numeroCompra] = {
            "cartelera"       : funcionElegida,
            "asiento"         : asiento,
            "combo"           : comboElegido,
            "descuento"       : descuentoElegido,
            "metodoPago"      : metodoPago,
            "total"           : round(total, 2),
            "nombreComprador" : nombreComprador
        }
        marcar_asiento_ocupado(asiento)

        guardarComprasJSON()     # registro la compra en compras
        guardarAsientosCSV()     # actualizo el asiento ocupado en asientos

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
    if len(dictPeliculas) == 0:
        print("No hay peliculas disponibles.")
        return 0
    try:
        nombreComprador = solicitar_nombre_validado("Ingrese su nombre completo: ")
        funcionElegida, numeroSala, nombrePelicula, horario = elegirFuncion()
        if funcionElegida == "":
            return 0
        asiento                             = seleccionarAsiento(numeroSala, nombrePelicula, horario)
        comboElegido, precioCombo           = elegirCombo()
        descuentoElegido, pctDescuento      = aplicarDescuento()
        metodoPago                          = seleccionarMetodoPago()
        subtotal, descuento, recargo, total = calcularTotal(precioCombo, pctDescuento, metodoPago)
        return confirmarCompra(funcionElegida, asiento, comboElegido, descuentoElegido, metodoPago,
                               subtotal, descuento, recargo, total, nombreComprador,
                               nombrePelicula, numeroSala, horario)
    except Exception as e:
        print("ERROR inesperado durante la compra: " + str(e))
        return 0

def verHistorialCompras():
    imprimir_separador("       HISTORIAL DE COMPRAS")
    if len(dictCompras) == 0:
        print(" No hay compras registradas.")
    else:
        numeros = list(dictCompras.keys())
        i = 0
        while i < len(numeros):
            k     = numeros[i]
            datos = dictCompras[k]
            print("--- Compra #" + str(k) + " ---")
            print("  Comprador: " + datos["nombreComprador"] + " | Funcion: " + datos["cartelera"])
            print("  Asiento: "   + datos["asiento"] + " | Combo: " + datos["combo"])
            print("  Descuento: " + datos["descuento"] +
                  " | Pago: "     + datos["metodoPago"] +
                  " | Total: $"   + str(datos["total"]) + "\n")
            i = i + 1
        print(" Total de compras: " + str(len(dictCompras)))
    print("==========================================")

def verHistorialOrdenado():
    """
    Ordena el historial por nombre usando sorted() con lambda
    """
    imprimir_separador("   HISTORIAL ORDENADO POR COMPRADOR")
    if len(dictCompras) == 0:
        print(" No hay compras registradas.\n==========================================")
        return
    numerosOrdenados = sorted(dictCompras.keys(), key=lambda k: dictCompras[k]["nombreComprador"].upper())
    i = 0
    while i < len(numerosOrdenados):
        k     = numerosOrdenados[i]
        datos = dictCompras[k]
        print("--- Compra #" + str(i + 1) + " ---")
        print("  Comprador: " + datos["nombreComprador"] + " | Funcion: " + datos["cartelera"])
        print("  Asiento: "   + datos["asiento"] + " | Combo: " + datos["combo"])
        print("  Descuento: " + datos["descuento"] +
              " | Pago: "     + datos["metodoPago"] +
              " | Total: $"   + str(datos["total"]) + "\n")
        i = i + 1
    print(" Total de compras: " + str(len(dictCompras)))
    print("==========================================")


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

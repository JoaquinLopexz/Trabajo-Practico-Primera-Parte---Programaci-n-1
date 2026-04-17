# ==============================================
#    SISTEMA INTEGRADO DE GESTIÓN DE CINE
#    VERSIÓN FINAL - 100% CÓDIGO BÁSICO
# ==============================================

# --- DATOS GLOBALES ---
peliculas = []
salas = []
precios = []
entradasVendidas = []
codigos = []
horarios = []
listaCartelera = []
listaAsiento = []
listaComboCliente = []
listaDescuentoAplicado = []
listaMetodoPago = []
listaTotalCompra = []
listaNombreComprador = [] 
listaAsientosOcupados = []

listaNombreCombo = ["Sin combo", "COMBO MEGA FIESTA DEL CINE", "COMBO FIESTA", "COMBOS NACOS FIESTA DEL CINE", "COMBO SUPERMAN", "COMBO LOS 4 FANTASTICOS", "BALDE POCHOCLOS", "POP MEDIANO", "BEBIDA GRANDE", "BEBIDA MEDIANA", "AGUA", "AGUA SABORIZADA", "MOGUL", "CHOCO-PAUSE", "M&M GRANDE", "M&M CHICO", "SKITTLES GRANDE", "SKITTLES MEDIANOS"]
listaPrecioCombo = [0, 20000, 12000, 12000, 24900, 24900, 9800, 8000, 7800, 7000, 4000, 4800, 5000, 3500, 10000, 5900, 9800, 5800]
listaTipoDescuento = ["Sin descuento", "Primer Lunes del Mes", "Segundo Lunes del Mes", "Miércoles de Cine", "Tarjeta Visa", "Tarjeta Mastercard", "Tarjeta American Express", "Tarjeta Naranja"]
listaPorcentajeDescuento = [0.0, 0.30, 0.30, 0.25, 0.15, 0.15, 0.20, 0.10]
listaMetodosPago = ["Billeteras virtuales", "Efectivo", "Visa", "Mastercard", "Crédito", "Débito"]
PRECIO_ENTRADA = 10000

# ==============================================
#    FUNCIONES AUXILIARES
# ==============================================

# Función para convertir un texto completo a mayúsculas
def convertirAMayuscula(texto):
    minusculas = "abcdefghijklmnopqrstuvwxyz"
    mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    resultado = ""
    i = 0
    while i < len(texto):
        caracter = texto[i]
        j = 0
        encontrado = 0
        while j < len(minusculas):
            if minusculas[j] == caracter:
                resultado = resultado + mayusculas[j]
                encontrado = 1
                j = len(minusculas)
            j = j + 1
        if encontrado == 0:
            resultado = resultado + caracter
        i = i + 1
    return resultado

# Función para verificar si un texto contiene otro texto dentro
def contieneCadena(textoPrincipal, textoBuscar):
    if len(textoBuscar) == 0:
        return 1
    if len(textoBuscar) > len(textoPrincipal):
        return 0
    i = 0
    while i <= len(textoPrincipal) - len(textoBuscar):
        j = 0
        coincide = 1
        while j < len(textoBuscar):
            if textoPrincipal[i + j] != textoBuscar[j]:
                coincide = 0
                j = len(textoBuscar)
            j = j + 1
        if coincide == 1:
            return 1
        i = i + 1
    return 0

# Función para redondear un número a dos decimales
def redondearDosDecimales(numero):
    multiplicado = numero * 100
    if multiplicado - int(multiplicado) >= 0.5:
        redondeado = int(multiplicado) + 1
    else:
        redondeado = int(multiplicado)
    return redondeado / 100

# Función para validar si un texto es un número entero
def esEntero(valor):
    if len(valor) == 0:
        return 0
    i = 0
    while i < len(valor):
        if valor[i] < "0" or valor[i] > "9":
            return 0
        i = i + 1
    return 1

# Función para solicitar un número dentro de un rango específico
def solicitarNumero(mensaje, minimo, maximo):
    valido = 0
    numero = 0
    while valido == 0:
        entrada = input(mensaje).strip()
        if len(entrada) == 0:
            print("ERROR: no puede estar vacío.")
        elif esEntero(entrada) == 1:
            numero = int(entrada)
            if numero >= minimo and numero <= maximo:
                valido = 1
            else:
                print("ERROR: debe estar entre " + str(minimo) + " y " + str(maximo))
        else:
            print("ERROR: debe ingresar un número.")
    return numero

# Función para solicitar un texto no vacío al usuario
def solicitarTexto(mensaje):
    texto = input(mensaje).strip()
    while len(texto) == 0:
        print("ERROR: no puede estar vacío.")
        texto = input(mensaje).strip()
    return texto

# Función para solicitar la selección de una opción de una lista
def solicitarOpcionLista(mensaje, lista):
    return solicitarNumero(mensaje, 1, len(lista)) - 1

# Función para imprimir un separador visual con título
def imprimirSeparador(titulo):
    print("==========================================\n" + titulo + "\n==========================================")

# Función para buscar un valor dentro de una lista y retornar su índice
def buscarEnLista(lista, valor):
    i = 0
    while i < len(lista):
        if lista[i] == valor:
            return i
        i = i + 1
    return -1

# Función para calcular máximo, mínimo o promedio de una lista
def calcularEstadistico(lista, tipo):
    if len(lista) == 0:
        return 0
    resultado = lista[0]
    i = 1
    if tipo == "max":
        while i < len(lista):
            if lista[i] > resultado:
                resultado = lista[i]
            i = i + 1
    elif tipo == "min":
        while i < len(lista):
            if lista[i] < resultado:
                resultado = lista[i]
            i = i + 1
    elif tipo == "promedio":
        suma = lista[0]
        while i < len(lista):
            suma = suma + lista[i]
            i = i + 1
        resultado = suma / len(lista)
    return resultado

# Función para mostrar una lista numerada con título y opcionalmente precios
def mostrarListaNumerada(titulo, lista, preciosLista=None):
    imprimirSeparador(titulo)
    i = 0
    while i < len(lista):
        if preciosLista != None:
            print(str(i + 1) + ". " + lista[i] + " - $" + str(preciosLista[i]))
        else:
            print(str(i + 1) + ". " + lista[i])
        i = i + 1
    print("==========================================")

# ==============================================
#    MENÚS PRINCIPALES
# ==============================================

# Función para mostrar el menú principal del sistema
def menuPrincipal():
    imprimirSeparador("       SISTEMA INTEGRADO DE CINE")
    print("1. MODO ADMINISTRADOR\n2. MODO ESPECTADOR\n0. Salir\n==========================================")
    return solicitarNumero("Seleccione una opción: ", 0, 2)

# Función para mostrar el menú del administrador
def menuAdministrador():
    imprimirSeparador("        MODO ADMINISTRADOR")
    opciones = ["Cargar salas y películas", "Mostrar cartelera", "Vender entradas", "Ver recaudación por sala y total", "Modificar película", "Calcular totales generales", "Estadísticas de ventas", "Búsqueda de registros", "Análisis y estadísticas"]
    i = 0
    while i < len(opciones):
        print(str(i + 1) + ". " + opciones[i])
        i = i + 1
    print("0. Volver al menú principal\n==========================================")
    return solicitarNumero("Seleccione una opción: ", 0, 9)

# Función para mostrar el menú del espectador
def menuEspectador():
    imprimirSeparador("         MODO ESPECTADOR")
    print("1. Ver Cartelera\n2. Comprar Entrada\n3. Ver Historial de Compras\n4. Ver Historial Ordenado\n0. Volver al menú principal\n==========================================")
    return solicitarNumero("Seleccione una opción: ", 0, 4)

# ==============================================
#    FUNCIONES ADMINISTRATIVAS
# ==============================================

# Función para generar un código único automático para cada película
def generarCodigoPelicula():
    numero = len(codigos) + 1
    if numero < 10:
        codigo = "PELI00" + str(numero)
    elif numero < 100:
        codigo = "PELI0" + str(numero)
    else:
        codigo = "PELI" + str(numero)
    return codigo

# Función para cargar películas en el sistema con validación de datos
def cargarPeliculas():
    imprimirSeparador("      CARGAR PELÍCULAS Y SALAS")
    cantidadPeliculas = solicitarNumero("¿Cuántas películas desea cargar? (1-10): ", 1, 10)
    i = 0
    while i < cantidadPeliculas:
        imprimirSeparador("         PELÍCULA #" + str(i + 1))
        nombrePelicula = solicitarTexto("Nombre de la película: ")
        sala = solicitarNumero("Número de sala (1-8): ", 1, 8)
        horario = solicitarTexto("Horario de función (ej: 19:30): ")
        codigo = generarCodigoPelicula()
        peliculas.append(nombrePelicula)
        salas.append(sala)
        precios.append(PRECIO_ENTRADA)
        entradasVendidas.append(0)
        codigos.append(codigo)
        horarios.append(horario)
        asientosOcupados = []
        j = 0
        while j < 50:
            asientosOcupados.append(0)
            j = j + 1
        listaAsientosOcupados.append(asientosOcupados)
        print("Código generado: " + codigo)
        i = i + 1
    print("==========================================\n¡Películas cargadas exitosamente!")

# Función para mostrar la cartelera completa con información de películas
def mostrarCarteleraAdmin():
    imprimirSeparador("        CARTELERA COMPLETA")
    if len(peliculas) == 0:
        print(" No hay películas cargadas aún.")
    else:
        i = 0
        while i < len(peliculas):
            print("-------------------------------------------\n[" + codigos[i] + "] " + peliculas[i] + "\nSALA: " + str(salas[i]) + " | HORARIO: " + horarios[i] + " | PRECIO: $" + str(precios[i]) + "\nENTRADAS VENDIDAS: " + str(entradasVendidas[i]))
            i = i + 1
    print("==========================================")

# Función para vender entradas desde el panel de administrador
def venderEntradasAdmin():
    imprimirSeparador("        VENTA DE ENTRADAS (ADMIN)")
    if len(peliculas) == 0:
        print(" Primero debe cargar películas.\n==========================================")
        return
    mostrarCarteleraAdmin()
    indicePelicula = solicitarNumero("Seleccione número de película: ", 1, len(peliculas)) - 1
    cantidadEntradas = solicitarNumero("Cantidad de entradas: ", 1, 10)
    entradasVendidas[indicePelicula] = entradasVendidas[indicePelicula] + cantidadEntradas
    print("==========================================\n¡Venta registrada! Total: $" + str(cantidadEntradas * PRECIO_ENTRADA))

# Función para calcular y mostrar la recaudación por sala y total
def verRecaudacion():
    imprimirSeparador("     RECAUDACIÓN POR SALA")
    if len(peliculas) == 0:
        print(" No hay películas cargadas.\n==========================================")
        return
    recaudacionPorSala = []
    i = 0
    while i < 8:
        recaudacionPorSala.append(0)
        i = i + 1
    i = 0
    while i < len(peliculas):
        numeroSala = salas[i]
        recaudacionPorSala[numeroSala - 1] = recaudacionPorSala[numeroSala - 1] + (entradasVendidas[i] * precios[i])
        i = i + 1
    i = 0
    while i < 8:
        print("Sala " + str(i + 1) + ": $" + str(recaudacionPorSala[i]))
        i = i + 1
    totalRecaudacion = 0
    i = 0
    while i < len(recaudacionPorSala):
        totalRecaudacion = totalRecaudacion + recaudacionPorSala[i]
        i = i + 1
    print("-------------------------------------------\nRECAUDACIÓN TOTAL: $" + str(totalRecaudacion) + "\n==========================================")

# Función para modificar los datos de una película existente
def modificarPelicula():
    imprimirSeparador("      MODIFICAR PELÍCULA")
    if len(peliculas) == 0:
        print(" No hay películas para modificar.\n==========================================")
        return
    mostrarCarteleraAdmin()
    indicePelicula = solicitarNumero("Seleccione película a modificar: ", 1, len(peliculas)) - 1
    print("Película seleccionada: " + peliculas[indicePelicula])
    print("1. Cambiar nombre\n2. Cambiar sala\n3. Cambiar horario\n4. Cambiar precio")
    opcion = solicitarNumero("Seleccione qué desea modificar: ", 1, 4)
    if opcion == 1:
        peliculas[indicePelicula] = solicitarTexto("Nuevo nombre: ")
    elif opcion == 2:
        salas[indicePelicula] = solicitarNumero("Nueva sala (1-8): ", 1, 8)
    elif opcion == 3:
        horarios[indicePelicula] = solicitarTexto("Nuevo horario: ")
    elif opcion == 4:
        precios[indicePelicula] = solicitarNumero("Nuevo precio: ", 1000, 50000)
    print("==========================================\n¡Película modificada exitosamente!")

# Función para calcular y mostrar estadísticas generales del sistema
def calcularTotales():
    imprimirSeparador("     TOTALES GENERALES")
    if len(peliculas) == 0:
        print(" No hay datos para calcular.\n==========================================")
        return
    totalEntradas = 0
    totalRecaudacion = 0
    i = 0
    while i < len(entradasVendidas):
        totalEntradas = totalEntradas + entradasVendidas[i]
        totalRecaudacion = totalRecaudacion + (entradasVendidas[i] * precios[i])
        i = i + 1
    print("PELÍCULAS CARGADAS: " + str(len(peliculas)) + "\nENTRADAS VENDIDAS: " + str(totalEntradas) + "\nRECAUDACIÓN TOTAL: $" + str(totalRecaudacion) + "\n==========================================")

# Función para mostrar estadísticas detalladas de ventas
def estadisticasVentas():
    imprimirSeparador("     ESTADÍSTICAS DE VENTAS")
    if len(peliculas) == 0:
        print(" No hay películas cargadas.\n==========================================")
        return
    if len(entradasVendidas) > 0:
        maxEntradas = calcularEstadistico(entradasVendidas, "max")
        minEntradas = calcularEstadistico(entradasVendidas, "min")
        promedio = calcularEstadistico(entradasVendidas, "promedio")
        promedioRedondeado = redondearDosDecimales(promedio)
        print("Máximo de entradas vendidas: " + str(maxEntradas) + "\nMínimo de entradas vendidas: " + str(minEntradas) + "\nPromedio de entradas: " + str(promedioRedondeado))
        idxMax = buscarEnLista(entradasVendidas, maxEntradas)
        idxMin = buscarEnLista(entradasVendidas, minEntradas)
        if idxMax != -1:
            print("\nPelícula más vendida: " + peliculas[idxMax])
        if idxMin != -1:
            print("Película menos vendida: " + peliculas[idxMin])
    print("==========================================")

# ==============================================
#    FUNCIONES DE ESPECTADOR
# ==============================================

# Función para mostrar la cartelera al público
def mostrarCartelera():
    imprimirSeparador("          CARTELERA")
    if len(peliculas) == 0:
        print(" No hay películas disponibles en este momento.")
    else:
        i = 0
        while i < len(peliculas):
            print("-------------------------------------------\n" + str(i + 1) + ". " + peliculas[i] + "\n   Sala: " + str(salas[i]) + " | Horario: " + horarios[i] + "\n   Precio: $" + str(precios[i]))
            i = i + 1
    print("==========================================")

# Función para mostrar el mapa de asientos disponibles y ocupados
def mostrarMapaAsientos(indicePelicula):
    imprimirSeparador("      MAPA DE ASIENTOS - SALA " + str(salas[indicePelicula]))
    print("         PANTALLA")
    print("    1  2  3  4  5  6  7  8  9 10")
    fila = 1
    columna = 1
    numAsiento = 1
    while fila <= 5:
        if fila == 1:
            print("A", end="")
        elif fila == 2:
            print("B", end="")
        elif fila == 3:
            print("C", end="")
        elif fila == 4:
            print("D", end="")
        elif fila == 5:
            print("E", end="")
        columna = 1
        while columna <= 10:
            if listaAsientosOcupados[indicePelicula][numAsiento - 1] == 0:
                print("  O", end="")
            else:
                print("  X", end="")
            columna = columna + 1
            numAsiento = numAsiento + 1
        print()
        fila = fila + 1
    print("\nO = Disponible  |  X = Ocupado\n==========================================")

# Función para convertir número de asiento a formato letra-número
def convertirNumeroAAsiento(numero):
    fila = (numero - 1) // 10
    columna = (numero - 1) % 10 + 1
    if fila == 0:
        letraFila = "A"
    elif fila == 1:
        letraFila = "B"
    elif fila == 2:
        letraFila = "C"
    elif fila == 3:
        letraFila = "D"
    elif fila == 4:
        letraFila = "E"
    else:
        letraFila = "?"
    return letraFila + str(columna)

# Función para marcar asientos como ocupados después de la compra
def marcarAsientosOcupados(indicePelicula, asientos):
    i = 0
    while i < len(asientos):
        numeroAsiento = asientos[i]
        listaAsientosOcupados[indicePelicula][numeroAsiento - 1] = 1
        i = i + 1

# Función principal para procesar la compra completa de entradas
def procesarCompra():
    imprimirSeparador("         COMPRAR ENTRADA")
    if len(peliculas) == 0:
        print(" No hay películas disponibles.\n==========================================")
        return 0
    mostrarCartelera()
    indicePelicula = solicitarNumero("Seleccione película: ", 1, len(peliculas)) - 1
    mostrarMapaAsientos(indicePelicula)
    cantidadEntradas = solicitarNumero("¿Cuántas entradas desea comprar? (1-5): ", 1, 5)
    asientosSeleccionados = []
    i = 0
    while i < cantidadEntradas:
        asientoValido = 0
        while asientoValido == 0:
            numeroAsiento = solicitarNumero("Seleccione asiento (1-50) para entrada #" + str(i + 1) + ": ", 1, 50)
            if listaAsientosOcupados[indicePelicula][numeroAsiento - 1] == 1:
                print("ERROR: Asiento " + convertirNumeroAAsiento(numeroAsiento) + " ya está ocupado.")
            elif buscarEnLista(asientosSeleccionados, numeroAsiento) != -1:
                print("ERROR: Ya seleccionó ese asiento.")
            else:
                asientosSeleccionados.append(numeroAsiento)
                asientoValido = 1
        i = i + 1
    mostrarListaNumerada("      COMBOS DISPONIBLES", listaNombreCombo, listaPrecioCombo)
    comboSeleccionado = solicitarOpcionLista("Seleccione un combo: ", listaNombreCombo)
    mostrarListaNumerada("      DESCUENTOS DISPONIBLES", listaTipoDescuento)
    descuentoSeleccionado = solicitarOpcionLista("Seleccione descuento: ", listaTipoDescuento)
    mostrarListaNumerada("      MÉTODOS DE PAGO", listaMetodosPago)
    metodoPagoSeleccionado = solicitarOpcionLista("Seleccione método de pago: ", listaMetodosPago)
    nombreCliente = solicitarTexto("Ingrese su nombre completo: ")
    subtotalEntradas = cantidadEntradas * PRECIO_ENTRADA
    precioCombo = listaPrecioCombo[comboSeleccionado]
    subtotal = subtotalEntradas + precioCombo
    porcentajeDescuento = listaPorcentajeDescuento[descuentoSeleccionado]
    descuentoAplicado = subtotal * porcentajeDescuento
    descuentoRedondeado = redondearDosDecimales(descuentoAplicado)
    totalFinal = subtotal - descuentoRedondeado
    totalRedondeado = redondearDosDecimales(totalFinal)
    imprimirSeparador("       RESUMEN DE COMPRA")
    print("Cliente: " + nombreCliente + "\nPelícula: " + peliculas[indicePelicula] + "\nSala: " + str(salas[indicePelicula]) + " | Horario: " + horarios[indicePelicula] + "\n\nEntradas: " + str(cantidadEntradas) + " x $" + str(PRECIO_ENTRADA) + " = $" + str(subtotalEntradas))
    print("Asientos: ", end="")
    i = 0
    while i < len(asientosSeleccionados):
        print(convertirNumeroAAsiento(asientosSeleccionados[i]), end="")
        if i < len(asientosSeleccionados) - 1:
            print(", ", end="")
        i = i + 1
    print("\n\nCombo: " + listaNombreCombo[comboSeleccionado] + " - $" + str(precioCombo) + "\nDescuento: " + listaTipoDescuento[descuentoSeleccionado] + " (" + str(int(porcentajeDescuento * 100)) + "%) = -$" + str(descuentoRedondeado) + "\nMétodo de pago: " + listaMetodosPago[metodoPagoSeleccionado] + "\n\n-------------------------------------------\nTOTAL A PAGAR: $" + str(totalRedondeado) + "\n==========================================")
    confirmacion = convertirAMayuscula(input("¿Confirmar compra? (S/N): ").strip())
    while confirmacion != "S" and confirmacion != "N":
        confirmacion = convertirAMayuscula(input("Ingrese S o N: ").strip())
    if confirmacion == "S":
        entradasVendidas[indicePelicula] = entradasVendidas[indicePelicula] + cantidadEntradas
        marcarAsientosOcupados(indicePelicula, asientosSeleccionados)
        infoCartelera = peliculas[indicePelicula] + " - Sala " + str(salas[indicePelicula]) + " (" + horarios[indicePelicula] + ")"
        asientosTexto = ""
        i = 0
        while i < len(asientosSeleccionados):
            asientosTexto = asientosTexto + convertirNumeroAAsiento(asientosSeleccionados[i])
            if i < len(asientosSeleccionados) - 1:
                asientosTexto = asientosTexto + ", "
            i = i + 1
        listaNombreComprador.append(nombreCliente)
        listaCartelera.append(infoCartelera)
        listaAsiento.append(asientosTexto)
        listaComboCliente.append(listaNombreCombo[comboSeleccionado])
        listaDescuentoAplicado.append(listaTipoDescuento[descuentoSeleccionado])
        listaMetodoPago.append(listaMetodosPago[metodoPagoSeleccionado])
        listaTotalCompra.append(totalRedondeado)
        print("\n¡COMPRA EXITOSA! Disfrute la función.\n==========================================")
        return 1
    else:
        print("\nCompra cancelada.\n==========================================")
        return 0

# Función para mostrar el historial de todas las compras realizadas
def verHistorialCompras():
    imprimirSeparador("     HISTORIAL DE COMPRAS")
    if len(listaCartelera) == 0:
        print(" No hay compras registradas.")
    else:
        i = 0
        while i < len(listaCartelera):
            print("-------------------------------------------\nCOMPRA #" + str(i + 1) + "\nCliente: " + listaNombreComprador[i] + "\nPelícula: " + listaCartelera[i] + "\nAsientos: " + listaAsiento[i] + "\nCombo: " + listaComboCliente[i] + "\nDescuento: " + listaDescuentoAplicado[i] + "\nMétodo de pago: " + listaMetodoPago[i] + "\nTotal: $" + str(listaTotalCompra[i]))
            i = i + 1
    print("==========================================")

# Función para ordenar los registros alfabéticamente por nombre del comprador
def ordenarRegistrosPorInsercion():
    i = 1
    while i < len(listaNombreComprador):
        claveNombre = listaNombreComprador[i]
        claveCartelera = listaCartelera[i]
        claveAsiento = listaAsiento[i]
        claveCombo = listaComboCliente[i]
        claveDescuento = listaDescuentoAplicado[i]
        claveMetodoPago = listaMetodoPago[i]
        claveTotal = listaTotalCompra[i]
        j = i - 1
        while j >= 0 and convertirAMayuscula(listaNombreComprador[j]) > convertirAMayuscula(claveNombre):
            listaNombreComprador[j + 1] = listaNombreComprador[j]
            listaCartelera[j + 1] = listaCartelera[j]
            listaAsiento[j + 1] = listaAsiento[j]
            listaComboCliente[j + 1] = listaComboCliente[j]
            listaDescuentoAplicado[j + 1] = listaDescuentoAplicado[j]
            listaMetodoPago[j + 1] = listaMetodoPago[j]
            listaTotalCompra[j + 1] = listaTotalCompra[j]
            j = j - 1
        listaNombreComprador[j + 1] = claveNombre
        listaCartelera[j + 1] = claveCartelera
        listaAsiento[j + 1] = claveAsiento
        listaComboCliente[j + 1] = claveCombo
        listaDescuentoAplicado[j + 1] = claveDescuento
        listaMetodoPago[j + 1] = claveMetodoPago
        listaTotalCompra[j + 1] = claveTotal
        i = i + 1

# Función para mostrar el historial ordenado alfabéticamente
def verHistorialOrdenado():
    imprimirSeparador("   HISTORIAL ORDENADO POR COMPRADOR")
    if len(listaCartelera) == 0:
        print(" No hay compras registradas.")
    else:
        ordenarRegistrosPorInsercion()
        verHistorialCompras()

# ==============================================
#    FUNCIONES DE BÚSQUEDA Y ANÁLISIS
# ==============================================

# Función para buscar compras por nombre de cliente
def buscarPorNombre(nombreBuscar):
    imprimirSeparador("       BÚSQUEDA POR NOMBRE")
    if len(listaNombreComprador) == 0:
        print(" No hay registros para buscar.\n==========================================")
        return []
    coincidencias = []
    i = 0
    while i < len(listaNombreComprador):
        nombreBuscarMayus = convertirAMayuscula(nombreBuscar)
        nombreCompradorMayus = convertirAMayuscula(listaNombreComprador[i])
        if contieneCadena(nombreCompradorMayus, nombreBuscarMayus) == 1:
            coincidencias.append(i)
        i = i + 1
    if len(coincidencias) == 0:
        print(" No se encontraron resultados para: '" + nombreBuscar + "'")
    else:
        print(" Se encontraron " + str(len(coincidencias)) + " resultado(s):\n")
        j = 0
        while j < len(coincidencias):
            idx = coincidencias[j]
            print("--- Resultado #" + str(j + 1) + " ---\n  Comprador: " + listaNombreComprador[idx] + " | Función: " + listaCartelera[idx] + "\n  Asiento: " + listaAsiento[idx] + " | Total: $" + str(listaTotalCompra[idx]) + "\n")
            j = j + 1
    print("==========================================")
    return coincidencias

# Función para buscar una película por su código único
def buscarPorCodigo(codigoBuscar):
    imprimirSeparador("       BÚSQUEDA POR CÓDIGO")
    if len(codigos) == 0:
        print(" No hay películas cargadas.\n==========================================")
        return -1
    indice = buscarEnLista(codigos, codigoBuscar)
    if indice == -1:
        print(" No se encontró película con código: '" + codigoBuscar + "'")
    else:
        print(" ¡Película encontrada!\n\n  Código: " + codigos[indice] + " | Nombre: " + peliculas[indice] + "\n  Sala: " + str(salas[indice]) + " | Horario: " + horarios[indice] + "\n  Precio: $" + str(precios[indice]) + " | Entradas: " + str(entradasVendidas[indice]))
    print("==========================================")
    return indice

# Función para mostrar el menú de opciones de búsqueda
def menuBusqueda():
    imprimirSeparador("         SISTEMA DE BÚSQUEDA")
    print("1. Buscar compra por nombre de cliente\n2. Buscar película por código\n0. Volver\n==========================================")
    opcion = solicitarNumero("Seleccione una opción: ", 0, 2)
    if opcion == 1:
        buscarPorNombre(solicitarTexto("Ingrese el nombre a buscar: "))
    elif opcion == 2:
        buscarPorCodigo(solicitarTexto("Ingrese el código de la película: "))

# Función para analizar estadísticas de las compras realizadas
def analisisCompras():
    imprimirSeparador("     ANÁLISIS DE COMPRAS")
    if len(listaTotalCompra) == 0:
        print(" No hay compras registradas.\n==========================================")
        return
    maximo = calcularEstadistico(listaTotalCompra, "max")
    minimo = calcularEstadistico(listaTotalCompra, "min")
    promedio = calcularEstadistico(listaTotalCompra, "promedio")
    promedioRedondeado = redondearDosDecimales(promedio)
    sumaTotal = 0
    i = 0
    while i < len(listaTotalCompra):
        sumaTotal = sumaTotal + listaTotalCompra[i]
        i = i + 1
    print(" ESTADÍSTICAS DE VENTAS:\n\n  Total de compras: " + str(len(listaTotalCompra)) + "\n  Recaudación total: $" + str(sumaTotal) + "\n  Compra máxima: $" + str(maximo) + " | Compra mínima: $" + str(minimo) + "\n  Promedio por compra: $" + str(promedioRedondeado))
    idxMax = buscarEnLista(listaTotalCompra, maximo)
    idxMin = buscarEnLista(listaTotalCompra, minimo)
    if idxMax != -1:
        print("\n  COMPRA MÁS ALTA: " + listaNombreComprador[idxMax] + " ($" + str(maximo) + ")")
    if idxMin != -1:
        print("  COMPRA MÁS BAJA: " + listaNombreComprador[idxMin] + " ($" + str(minimo) + ")")
    print("\n==========================================")

# Función para analizar estadísticas de las películas
def analisisPeliculas():
    imprimirSeparador("     ANÁLISIS DE PELÍCULAS")
    if len(peliculas) == 0:
        print(" No hay películas cargadas.\n==========================================")
        return
    if len(entradasVendidas) > 0:
        maxEntradas = calcularEstadistico(entradasVendidas, "max")
        minEntradas = calcularEstadistico(entradasVendidas, "min")
        promedio = calcularEstadistico(entradasVendidas, "promedio")
        promedioRedondeado = redondearDosDecimales(promedio)
        totalEntradas = 0
        i = 0
        while i < len(entradasVendidas):
            totalEntradas = totalEntradas + entradasVendidas[i]
            i = i + 1
        print(" ESTADÍSTICAS DE PELÍCULAS:\n\n  Total de películas: " + str(len(peliculas)) + " | Entradas vendidas: " + str(totalEntradas) + "\n  Máximo: " + str(maxEntradas) + " | Mínimo: " + str(minEntradas) + " | Promedio: " + str(promedioRedondeado))
        idxMax = buscarEnLista(entradasVendidas, maxEntradas)
        idxMin = buscarEnLista(entradasVendidas, minEntradas)
        if idxMax != -1:
            print("\n  MÁS VENDIDA: " + peliculas[idxMax] + " (" + str(maxEntradas) + " entradas)")
        if idxMin != -1:
            print("  MENOS VENDIDA: " + peliculas[idxMin] + " (" + str(minEntradas) + " entradas)")
    print("\n==========================================")

# Función para mostrar el menú de análisis estadístico
def menuAnalisis():
    imprimirSeparador("       SISTEMA DE ANÁLISIS")
    print("1. Análisis de compras\n2. Análisis de películas\n3. Análisis completo\n0. Volver\n==========================================")
    opcion = solicitarNumero("Seleccione una opción: ", 0, 3)
    if opcion == 1:
        analisisCompras()
    elif opcion == 2:
        analisisPeliculas()
    elif opcion == 3:
        analisisCompras()
        print()
        analisisPeliculas()

# ==============================================
#    FUNCIÓN PRINCIPAL
# ==============================================

# Función principal que ejecuta el programa completo
def main():
    print("==========================================\n   BIENVENIDOS A CINE DIGITAL\n==========================================")
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
                elif opcionAdmin == 0:
                    salirAdmin = 1
        elif opcion == 2:
            salirEspectador = 0
            while salirEspectador == 0:
                opcionEspectador = menuEspectador()
                if opcionEspectador == 1:
                    mostrarCartelera()
                elif opcionEspectador == 2:
                    continuarComprando = "S"
                    while continuarComprando == "S":
                        resultado = procesarCompra()
                        if resultado == 1:
                            continuarComprando = convertirAMayuscula(input("¿Desea comprar otra entrada? (S/N): ").strip())
                            while continuarComprando != "S" and continuarComprando != "N":
                                continuarComprando = convertirAMayuscula(input("Ingrese S o N: ").strip())
                        else: 
                            continuarComprando = "N"
                elif opcionEspectador == 3:
                    verHistorialCompras()
                elif opcionEspectador == 4:
                    verHistorialOrdenado()
                elif opcionEspectador == 0:
                    salirEspectador = 1
        elif opcion == 0:
            imprimirSeparador("  ¡Gracias por usar Cine Digital!")
            print("          ¡Hasta pronto!\n==========================================")
            salir = 1

main()

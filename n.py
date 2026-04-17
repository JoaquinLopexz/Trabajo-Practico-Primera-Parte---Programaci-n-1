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
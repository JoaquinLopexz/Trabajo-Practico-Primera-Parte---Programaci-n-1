from functools import reduce   
import csv                      
import json                       

#BLOQUE 1 - CARTELERA 
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



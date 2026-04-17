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


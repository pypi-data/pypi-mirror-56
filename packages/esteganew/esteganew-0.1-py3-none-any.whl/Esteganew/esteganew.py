#--------------------------------ASPECTOS_TECNICOS------------------------------
from os import system, name
from time import sleep
from cryptography.fernet import Fernet
"""
El tipo de encriptación Fernet toma un mensaje codificado a bytes, el tiempo
actual y una llave de 256 bits, retornando un toquen que es una representación
indescifrable e inalterable sin el archivo llave que se implemento en un principio.

"""


def clear():
    """
    Utiliza la libreria os.system para poder limpiar la pantalla de la terminal.
    """

    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')




#-------------------------------------CLASES------------------------------------

#------------------------------------FUNCIONES----------------------------------
def llave():
    """

    Con esta función se genera una llave para empezar el proceso de encriptación,
    la cual es de tipo "bytes", la cual es necesaria para poder crear un mensaje
    encriptado.

    Returns:
        bytes.Doc:  no solo retorna un valor de tipo 'bytes', sino que además
                    retorna un archivo necesario para desencriptar los valores
                    encriptados con la función 'enCRYptar()'.

    """
    llave = Fernet.generate_key()
    with open("miLlave.key", "wb") as k:
        k.write(llave)
    return llave

def enCRYptar(mensaje):
    """
    Esta se encarga de recibir un mensaje de tipo str, y a partir de la función
    'llave()', procesos de codificación nativos de python y el modulo de
    encriptación 'Feret' de la librería 'cryptography.fernet'.

    Args:
        mensaje (str): es el mensaje que va a ser encriptado.

    Returns:
        str: mensaje ya encriptado.

    """

    mensaje_cod = mensaje.encode()
    lLave = llave()
    objeto_crypto = Fernet(lLave)
    mensaje_encript =objeto_crypto.encrypt(mensaje_cod)
    return mensaje_encript.decode()

def deCRYptar(mensaje,nombre_archivo):
    """
    Se encarga de recibir un mensaje encriptado de tipo str y el nombre de un
    archivo con extención '.key', luego por medio de la función 'open()' nativa
    de python extrae el texto del archivo '.key' para aplicar  funciones del
    modulo Fermet, que ayudan a recuperar el mensaje encriptado.

    Args:
        mensaje (str):  Mensaje previamente retornado por la función 'enCRYptar()'.

        nombre_archivo (str):   Nombre del archivo generado por la función
                                'enCRYptar()', el cual por default es
                                'miLlave.key' del cual el nombre se puede
                                cambiar pero no la extención '.key'.

    Returns:
        str: Mensaje ya decriptando

    Raises:
        FileNotFoundError or UnboundLocalError: si el archivo que se presenta no
        existe o no es el indicado para la imagen, se imprime un mensaje, avisando
        que no se logró hacer la desencripción.

    """

    try:
        archivo = open(nombre_archivo, "rb")
    except FileNotFoundError or UnboundLocalError :
        clear()
        print("Lo sentimos, pero no fue posible extraer el mesaje. :(")
        sleep(5)
        clear()
        raise SystemExit

    clave = archivo.read()
    archivo.close()
    mensaje = mensaje.encode()
    objeto_crypto = Fernet(clave)
    try:
        decriptando = objeto_crypto.decrypt(mensaje)
    except:
        clear()
        print("Lo sentimos, pero no fue posible extraer el mesaje. :(")
        sleep(5)
        clear()
        raise SystemExit
    decodificado = decriptando.decode()
    return decodificado

    #--------------------------------ASPECTOS_TECNICOS------------------------------
from os import system, name
from time import sleep
from PIL import Image as im
"""
PIL (Python Image Library) va a ser utilizada ya que dentro de sus funciones uno
puede abrir y alterar imagenes. Se va exportar con el apodo 'im' para mayor
facilidad de uso.
"""



#-------------------------------------CLASES------------------------------------
class Esteganew:
    """
    Esteganew es una clase diseñada con la finalidad de poder esconder texto
    dentro de los bits menos significativos de los pixeles que conforman una
    imagen.
    """


    def __init__(self, nombre_imagen:str, mensaje = None, nuevo_nombre = None ):
        """
        Esta clase tiene requiere en un principio como primer argumento el
        nombre de la imagen que será utilizada (con extención tipo: '.png',
        '.tiff,' .jpg'... etc.) de tipo 'str', como segundo argumento el
        mensaje que se desea esconder tambien de tipo 'str' y para el tercer
        argumento se exige un nombre para el archivo de salida de tipo 'str'.
        """
        try:
            self.imagen = im.open(nombre_imagen, 'r')
        except:
            clear()
            print("Lo sentimos, pero el proceso no puede ser terminado :(")
            sleep(5)
            clear()
            raise SystemExit

        self.copia_img = self.imagen.copy()
        self.mensaje = mensaje
        self.pixeles =  self.copia_img.getdata()
        self.nuevo_nombre = nuevo_nombre


    def generar_data(self):
        """
        Esta función se encarga de transformar el mensaje a binario. Lo que hace
        es adjuntar a una lista el valor de cada caracter, el cual se obtiene en
        un principio transformandolo a su valor en Unicode, y luego este a
        binario.
        """

        lista_data = []
        for i in self.mensaje:
            lista_data.append(format(ord(i), '08b'))
        return lista_data

    def modificar_pixeles(self):
        """
        La razón de esta función es la de convertir los pixeles necesarios de la
        imagen (según lo largo del mensaje) en nuvos pixeles alterando el valor
        RGB de cada pixel reduciendolo en una unidad.
        """

        lista_data = self.generar_data()
        tamano_data = len(lista_data)
        pixel = self.pixeles
        # pixel es un 'Generator' pues es una iteración que solo guarda el
        #valor individual de cada iteración. Se usa el '__next__' para
        #decirle a el 'Generator' que olvide el valor actual y utilice
        #el siguiente.
        imagen_data = iter(pixel)

        #Este ciclo for esta para que según el tamaño del mensaje a adjuntar se
        #editen los valores RGB de cada pixel, reduciendolo en una unidad.
        for i in range(tamano_data):
            #Extrae del 'Generator' los valores de 3 pixeles de forma simultanea.
            pixel = [valor for valor in imagen_data.__next__()[:3]+
                                        imagen_data.__next__()[:3]+
                                        imagen_data.__next__()[:3]]


            #El proceso de alteración de los pixel comienza comparando el
            #valor binario de cada letra con los valores de cada 3 pixeles
            #(R,G,B,R,G,B,R,G,B) ,utilizando los primeros 8 valores para
            #esconder el mensaje y el ultimo para definir la longitud del
            #mensaje al momento de decodificarlo.

            #En la primera parte compara cada bit de cada letra con su
            #respectiva posicion en la tupla (R,G,B,R,G,B,R,G,B), si el
            #valor del bit es igual a '0' y el valor de color en la tupla
            #dividido en 2 deja reciduo, se le resta una unidad al valor
            #de la tupla, si el valor del bit es igual a '4' y el valor
            #de color en la tupla dividido en 2 no deja reciduo, se le
            #resta una unidad al valor de la tupla.
            for j in range(0,8):

                if (lista_data[i][j] == "0") and (pixel[j]%2 != 0):
                    pixel[j] -= 1

                elif (lista_data[i][j] == "1") and (pixel[j] % 2 == 0):
                    if pixel[j] != 0:
                        pixel[j] -= 1
                    else:
                        pixel[j] += 1

            #Este condicional revisa si el mensaje ya codificado completamente,
            #para que el decodificador sea capaz de interpretarlo se acuerda
            #si el ultimo valor de la tupla (R,G,B,R,G,B,R,G,B) es par el
            #mensaje continua y si el valor es impar, significa que el mensaje
            #ya a acabado.
            if (i == tamano_data - 1):
                if (pixel[-1] % 2 == 0):
                    pixel[-1] -= 1
            else:
                if (pixel[-1] % 2 != 0):
                    pixel[-1] -= 1

            pixel = tuple(pixel)
            yield pixel[0:3]
            yield pixel[3:6]
            yield pixel[6:9]


    def cambiar_pix(self):
        """
        Esta función se encarga de modificar ya en la nueva image los valores
        de los pixeles. A partir de las cordenadas (x, y) de la imagen.
        """

        #El ancho de la imagen
        w = self.copia_img.size[0]
        (x, y) = (0, 0)

        for pix in self.modificar_pixeles():
            self.copia_img.putpixel((x,y),pix)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def codificar(self):
        """
        La función codificar() esta dada para retornar un archivo en
        formato '.png', con el mensaje ya escondido.
        """

        if (self.mensaje == None):
            raise Exception("Necesitas un mensaje si quieres codificar.")
        elif (self.nuevo_nombre == None):
            raise Exception("Necesitas un nuevo nombre para el archivo si quieres codificar.")
        else:
            self.cambiar_pix()
            self.copia_img.save("{}.png".format(self.nuevo_nombre), "PNG")

    def decodificar(self):
        """
        Esta función cumple la labor de retornar el mensaje oculto dentro de
        una imagen ya codificada.
        """
        if (self.mensaje != None):
            raise Exception("No necesitas un mensaje si quieres decodificar.")
        elif (self.nuevo_nombre != None):
            raise Exception("No necesitas un nuevo nombre para el archivo si quieres decodificar.")
        else:
            mensaje_secreto = ""
            imagen_data = iter(self.imagen.getdata())

            while (True):
                pixeles = [valor for valor in imagen_data.__next__()[:3]+
                                            imagen_data.__next__()[:3]+
                                            imagen_data.__next__()[:3]]

                str_binario = ""

                for i in pixeles[:8]:
                    if (i % 2 == 0):
                        str_binario += "0"
                    else:
                        str_binario += "1"

                mensaje_secreto += chr(int(str_binario, 2))
                if pixeles[-1] % 2 != 0:
                    return mensaje_secreto

# ==============================================================================
# ==============================================================================
# =================================FIN==========================================
# ===========================MUCHAS GRACIAS=====================================
# ================================ <3 ==========================================
# ==============================================================================
# ==============================================================================

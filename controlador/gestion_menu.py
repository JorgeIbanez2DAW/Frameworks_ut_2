from modelo.Usuario import Usuario
from modelo.BBDD_Error import BBDD_Error
import modelo.bbdd as bbdd


def dar_de_alta(configuracion: dict[str, str], usuario: Usuario = None) -> None:
    cnx = None
    try:
        cnx = bbdd.connection(configuracion)
        bbdd.add_usuario(cnx, usuario)
        print("Añadido correctamente")
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def modificar(configuracion: dict[str, str], usuario_modificado: Usuario):
    cnx = None
    try:
        cnx = bbdd.connection(configuracion)
        bbdd.update_usuario(cnx, usuario_modificado)
        print("Modificado correctamente")
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)

def obtener(configuracion: dict[str, str], codigo: str) -> Usuario:
    cnx = None
    try:
        cnx = bbdd.connection(configuracion)
        usuario = bbdd.get_usuario(cnx, codigo)
        print("Obtenido correctamente")
        return usuario
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def descargar_bbdd(configuracion: dict[str, str], formato: str = "csv"):
    cnx = None
    try:
        cnx = bbdd.connection(configuracion)
        print(bbdd.descargar_usuarios(cnx, formato))
        bbdd.close(cnx)
        print("Descargado correctamente")
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def visualizar(configuracion: dict[str, str]):
    print("Ver")


def dar_de_baja(configuracion: dict[str, str], usuario: Usuario):
    print("Baja")

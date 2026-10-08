import modelo.bbdd as bbdd
import vista.menus as v_menus
from modelo.Usuario import Usuario
from modelo.BBDD_Error import BBDD_Error
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


def dar_de_alta(configuracion: dict[str, str], usuario: Usuario) -> None:
    cnx: None | MySQLConnectionAbstract | PooledMySQLConnection = None
    try:
        cnx = bbdd.connection(configuracion)
        bbdd.add_usuario(cnx, usuario)
        v_menus.imprimir_mensajes(1)
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def modificar(configuracion: dict[str, str], usuario_modificado: Usuario) -> None:
    cnx: None | MySQLConnectionAbstract | PooledMySQLConnection = None
    try:
        cnx = bbdd.connection(configuracion)
        bbdd.update_usuario(cnx, usuario_modificado)
        v_menus.imprimir_mensajes(2)
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def obtener(configuracion: dict[str, str], codigo: str) -> Usuario | None:
    cnx: None | MySQLConnectionAbstract | PooledMySQLConnection = None
    try:
        cnx = bbdd.connection(configuracion)
        usuario = bbdd.get_usuario(cnx, codigo)
        if usuario is None:
            v_menus.imprimir_mensajes(5)
        return usuario
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def descargar_bbdd(configuracion: dict[str, str], formato: str = "csv") -> None:
    cnx: None | MySQLConnectionAbstract | PooledMySQLConnection = None
    try:
        cnx = bbdd.connection(configuracion)
        v_menus.imprimir(bbdd.descargar_usuarios(cnx, formato))
        bbdd.close(cnx)
        v_menus.imprimir_mensajes(3)
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def visualizar(configuracion: dict[str, str], limit: int = 10) -> None:
    cnx: None | MySQLConnectionAbstract | PooledMySQLConnection = None
    offset: int = 0
    fin: bool = False

    try:
        cnx = bbdd.connection(configuracion)
        while not fin:
            usuarios = bbdd.get_usuarios(cnx, limit, offset)

            if len(usuarios) == 0:
                fin = True
            else:
                for usuario in usuarios:
                    v_menus.imprimir(usuario)

                if len(usuarios) < limit or not v_menus.get_continuar():
                    fin = True
                else:
                    offset += limit
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)


def dar_de_baja(configuracion: dict[str, str], usuario: Usuario) -> None:
    cnx: None | MySQLConnectionAbstract | PooledMySQLConnection = None
    try:
        cnx = bbdd.connection(configuracion)
        lineas = bbdd.borrar_usuario(cnx, usuario.cod)
        if lineas == 1:
            v_menus.imprimir_mensajes(4)

        else:
            v_menus.imprimir_mensajes(5)
    except BBDD_Error as e:
        print(e)
    finally:
        if cnx is not None:
            bbdd.close(cnx)

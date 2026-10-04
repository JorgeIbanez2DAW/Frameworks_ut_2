import mysql.connector
from keyring.backends import null
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from modelo.Usuario import Usuario
from modelo.BBDD_Error import BBDD_Error


def connection(config: dict[str, str]) -> PooledMySQLConnection | MySQLConnectionAbstract | None:
    try:
        return mysql.connector.connect(
            host=config["host"],
            port=config["port"],
            user=config["usuario"],
            password=config["password"],
            database=config["database"]
        )
    except mysql.connector.Error:
        raise BBDD_Error("Error al conectarse a la base de datos")


def close(cnx: MySQLConnectionAbstract) -> None:
    try:
        cnx.close()
    except mysql.connector.Error:
        raise BBDD_Error("Error al desconectarse de la base de datos")


def add_usuario(cnx: MySQLConnectionAbstract, usuario: Usuario) -> None:
    if usuario:
        try:
            cursor = cnx.cursor()
            sql = "INSERT INTO usuarios (nombre, apellido_1, apellido_2, fecha_nacimiento) VALUES (%s, %s, %s, %s)"
            data = (usuario.nombre, usuario.apellido_1, usuario.apellido_2, usuario.fecha_nacimiento)
            cursor.execute(sql, data)
            cnx.commit()
        except mysql.connector.Error:
            raise BBDD_Error("Error al insertar usuario")
        finally:
            cursor.close()


def get_usuario(cnx: MySQLConnectionAbstract, codigo: str) -> Usuario:
    try:
        cursor = cnx.cursor()
        sql = "SELECT nombre, apellido_1, apellido_2, fecha_nacimiento FROM usuarios WHERE cod = %s"
        data = (codigo,)
        cursor.execute(sql, data)
        datos = cursor.fetchone()
        if datos is None:
            raise BBDD_Error("El código entregado no existe")
        return Usuario(codigo, datos[0], datos[1], datos[2], datos[3])
    except mysql.connector.Error:
        raise BBDD_Error("Error al obtener usuario")
    finally:
        cursor.close()


def update_usuario(cnx: MySQLConnectionAbstract, usuario: Usuario) -> None:
    try:
        cursor = cnx.cursor()
        sql = "UPDATE usuarios SET nombre = %s, apellido_1 = %s, apellido_2 = %s, fecha_nacimiento = %s WHERE cod = %s"
        data = (usuario.nombre, usuario.apellido_1, usuario.apellido_2, usuario.fecha_nacimiento, usuario.cod)
        cursor.execute(sql, data)
        cnx.commit()
    except mysql.connector.Error:
        raise BBDD_Error("Error al actualizar usuario")
    finally:
        cursor.close()


def descargar_usuarios(cnx: MySQLConnectionAbstract, formato: str = "csv") -> str:
    formato = formato if formato in ["json", "csv", "yaml", "toml"] else "csv"
    salida: str = ""
    usuarios: list[Usuario] = []  # es más rápido al crear la cadena de texto pero consume más memoria

    try:
        cursor = cnx.cursor()
        query = "SELECT * FROM usuarios"
        cursor.execute(query)
        for cod, nombre, apellido_1, apellido_2, fecha_nacimiento in cursor:
            usuarios.append(Usuario(str(cod), nombre, apellido_1, apellido_2, fecha_nacimiento))
        cursor.close()
    except mysql.connector.Error:
        raise BBDD_Error("Error al descargar la bbdd")

    match formato:
        case "csv":
            return "\n".join([usu.to_csv() for usu in usuarios])
        case "json":
            return "\n".join([usu.to_json() for usu in usuarios])
        case "yaml":
            return "\n".join([usu.to_yaml() for usu in usuarios])
        case "toml":
            return "\n".join([usu.to_toml() for usu in usuarios])

    return salida

# borrar usuario ejemplo
# cnx.autocommit = True
# cursor = cnx.cursor()
# del_persona = "DELETE FROM personas WHERE cod = 1"
# print(del_persona)
# cursor.execute(del_persona)
# emp_no = cursor.lastrowid
# print(emp_no)
#  cnx.commit()  Ya no es necesario por el autocommit
# cursor.close()

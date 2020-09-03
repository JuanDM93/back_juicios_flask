from api.utils.db import db_connect


def validarUsuario(email):
    # Validar usuario
    sql = "SELECT COUNT(1) AS BIT FROM usuarios "
    sql += "WHERE email = '" + str(email).lstrip().rstrip().upper()
    sql += "'"
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    if rv["BIT"] == 0:
        return False
    return True


def informacionActualizacionOregristroUsuario(email):
    # informacion usuario interna nuevos usuario o actualizacion
    sql = "select usuarios.apellido_paterno, usuarios.apellido_materno,"
    sql += "usuarios.nombre, usuarios.email, despachos.nombre "
    sql += "as nombre_despacho "
    sql += "from usuarios  INNER JOIN despachos on "
    sql += "despachos.id = usuarios.id_despacho"
    sql += " WHERE email = '" + str(email) + "'"
    cur, response = db_connect(sql)
    rv = cur.fetchone()
    return rv


def validarExpedienteDespachos(nombre_despacho):
    # Validar expediente
    sql = "SELECT COUNT(1) AS BIT FROM despachos "
    sql += "WHERE nombre = '" + str(nombre_despacho).lstrip().rstrip().upper()
    sql += "'"
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    if rv["BIT"] == 0:
        return False
    return True

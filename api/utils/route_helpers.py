from api.utils.db import db_connect
from datetime import datetime, timedelta


def eliminarCorreosAbogadosLocales(
    # Eliminar abogados reponsables
        id_juicio_local, listaCorreoAbogadosLocalesElimar):
    data = "("
    for CorreoAbogadoLocal in listaCorreoAbogadosLocalesElimar:
        data += "'" + CorreoAbogadoLocal + "', "
    data = data[:-2]
    data += ")"
    sql = "DELETE from abogados_responsables_juicios_locales WHERE email IN "
    sql += data
    sql += " AND id_juicio_local = " + str(id_juicio_local)
    db_connect(sql)


def registrarCorreosAbogadosLocales(
    # Metodo para asignar abogados responsables
        numero_de_expediente, id_juzgado_local,
        listaCorreoAbogadosLocales):
    sql = "SELECT id FROM juicios_locales WHERE numero_de_expediente = '"
    sql += str(numero_de_expediente)
    sql += "' AND id_juzgado_local = " + str(id_juzgado_local)
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    id_juicio_local = rv["id"]

    data = ""
    for CorreoAbogadoLocal in listaCorreoAbogadosLocales:
        data += "('" + str(id_juicio_local)
        data += "', '" + CorreoAbogadoLocal + "'), "
        # TODO
        # enviarCorreo(correoabogadolocal, 'texto formateado'--data['nombre'])
    data = data[:-2]

    sql = "INSERT INTO abogados_responsables_juicios_locales"
    sql += " (id_juicio_local, email) VALUES"
    sql += data
    db_connect(sql)


def correosLigadosJuiciosLocales(id_juicio_local):
    # Correos juicios locales
    sql = "SELECT email "
    sql += "FROM abogados_responsables_juicios_locales "
    sql += "WHERE id_juicio_local  = " + str(id_juicio_local)
    cur, response = db_connect(sql)
    rv = cur.fetchall()
    return rv


def metodo_actualizar_juicio(
    # Helper juicio local
        actor, demandado, numero_de_expediente, id_juzgado_local,
        emails, emailsEliminar, id_juicio_local):

    sql = "UPDATE juicios_locales SET "
    sql += "actor = '" + str(actor).lstrip().rstrip().upper() + "', "
    sql += "demandado = '" + str(demandado).lstrip().rstrip().upper() + "', "
    sql += "numero_de_expediente = '" + str(numero_de_expediente) + "', "
    sql += "id_juzgado_local = '" + str(id_juzgado_local) + "' "
    sql += " WHERE id = " + str(id_juicio_local)
    db_connect(sql)

    eliminarCorreosAbogadosLocales(id_juicio_local, emailsEliminar)
    registrarCorreosAbogadosLocales(
        numero_de_expediente, id_juzgado_local, emails)


def validarExpedienteJuiciosLocales(numero_de_expediente, id_juzgado_local):
    # Validar expediente
    sql = "SELECT COUNT(1) AS BIT FROM juicios_locales "
    sql += "WHERE numero_de_expediente = '" + str(numero_de_expediente)
    sql += "' AND id_juzgado_local = " + str(id_juzgado_local)
    cur, __ = db_connect(sql)

    rv = cur.fetchone()
    if rv["BIT"] == 0:
        return False
    return True


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


def dataActualizacionOinsercion(id_juzgado_local, numero_de_expediente):
    # data actualizacion o insercion
    sql = "select juicios_locales.id as id_juicio_local, "
    sql += "juzgados_locales.nombre as juzgado, "
    sql += "juicios_locales.id_juzgado_local, "
    sql += "juicios_locales.numero_de_expediente as expediente"
    sql += " from juicios_locales INNER JOIN juzgados_locales "
    sql += "on juzgados_locales.id = juicios_locales.id_juzgado_local "
    sql += "WHERE juicios_locales.id_juzgado_local = "
    sql += str(id_juzgado_local)
    sql += " and  juicios_locales.numero_de_expediente = '"
    sql += str(numero_de_expediente) + "'"
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    return rv


def eliminarAcuerdosLocales(id_juicio_local):
    # eliminar acuerdos locales
    sql = "DELETE FROM acuerdos_locales where id_juicio_local = "
    sql += str(id_juicio_local)
    __, response = db_connect(sql)


def acuerdosHistoricos(id_juicio_local):
    # en lazar acuerdos historicos
    fechasql = datetime.strftime(
        datetime.now() - timedelta(days=1), '%Y-%m-%d')
    yearsql = datetime.strftime(
        datetime.now() - timedelta(days=365), '%Y')

    sql = "SELECT acuerdos_locales.fecha, acuerdos_locales.descripcion"
    sql += " FROM acuerdos_locales where acuerdos_locales.id_juicio_local = "
    sql += str(id_juicio_local) + " AND "
    sql += " acuerdos_locales.fecha BETWEEN '" + yearsql
    sql += "-01-01' AND '" + fechasql + "'"
    sql += " ORDER BY acuerdos_locales.fecha DESC "
    cur, response = db_connect(sql)
    rv = cur.fetchall()
    return rv


def acuerdoslocalesdiarios(id_juicio_local):
    # acuerdos locales diarios
    fechasql = datetime.strftime(
        datetime.now() - timedelta(days=1), '%Y-%m-%d')
    sql = "SELECT acuerdos_locales.fecha, acuerdos_locales.descripcion"
    sql += " FROM acuerdos_locales where acuerdos_locales.id_juicio_local = "
    sql += str(id_juicio_local)+" AND "
    sql += " acuerdos_locales.fecha = '" + fechasql + "'"
    sql += " ORDER BY acuerdos_locales.fecha DESC "

    cur, response = db_connect(sql)
    rv = cur.fetchall()
    return rv


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


def listaCorreosLigador(id_juicio_local):
    lista = []
    for correo in correosLigadosJuiciosLocales(id_juicio_local):
        lista.append(correo["email"])
    return lista


def informacionLocalExpedienteHistorico(expediente, id_juzgado_local):
    sql = "select juicios_locales.numero_de_expediente as expediente, "
    sql += " juzgados_locales.nombre as juzgado, juicios_locales.actor,"
    sql += " juicios_locales.demandado, juicios_locales.id "
    sql += " as id_juicio_local FROM juicios_locales "
    sql += " INNER JOIN juzgados_locales ON juzgados_locales.id "
    sql += " = juicios_locales.id_juzgado_local "
    sql += " WHERE juicios_locales.numero_de_expediente = '"
    sql += str(expediente)
    sql += "' AND juicios_locales.id_juzgado_local = "
    sql += str(id_juzgado_local)

    cur, __ = db_connect(sql)
    rv = cur.fetchall()

    for r in rv:
        r["emails"] = listaCorreosLigador(r["id_juicio_local"])
    for r in rv:
        r["acuerdos"] = acuerdosHistoricos(r["id_juicio_local"])
    return rv

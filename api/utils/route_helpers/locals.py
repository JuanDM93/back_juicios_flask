from datetime import datetime, timedelta
from api.utils.db import db_connect


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


def validarExpedienteLocal(acuerdo):
    # Validar usuario
    sql = "SELECT COUNT(1) AS BIT FROM acuerdos_locales "
    sql += "WHERE descripcion = '" + str(acuerdo)
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
        datetime.now(), '%Y-%m-%d')
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
    for r in rv:
        r["fecha"] = r["fecha"].strftime('%Y-%m-%d')
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


def acuerdoslocalesdiarios(id_juicio_local):
    # acuerdos locales diarios
    fechasql = datetime.strftime(
        datetime.now(), '%Y-%m-%d')
    sql = "SELECT acuerdos_locales.fecha, acuerdos_locales.descripcion"
    sql += " FROM acuerdos_locales where acuerdos_locales.id_juicio_local = "
    sql += str(id_juicio_local)+" AND "
    sql += " acuerdos_locales.fecha = '" + fechasql + "'"
    sql += " ORDER BY acuerdos_locales.fecha DESC "

    cur, response = db_connect(sql)
    rv = cur.fetchall()

    for r in rv:
        r["fecha"] = r["fecha"].strftime('%Y-%m-%d')
    return rv


def sqlenviarcorreo(data):
    return informacionLocalExpedienteHistorico(
        data[0]["expediente"], data[0]["id_juzgado_local"])


def sqlenviarcorreoDiario():
    fechasql = datetime.strftime(
        datetime.now(),
        '%Y-%m-%d'
    )
    sql = "SELECT juicios_locales.numero_de_expediente as expediente, "
    sql += "juzgados_locales.nombre as juzgado,"
    sql += "juicios_locales.actor, juicios_locales.demandado, "
    sql += "juicios_locales.id as id_juicio_local "
    sql += "FROM acuerdos_locales INNER JOIN juicios_locales "
    sql += "ON juicios_locales.id = acuerdos_locales.id_juicio_local "
    sql += "INNER JOIN juzgados_locales "
    sql += "ON juzgados_locales.id = juicios_locales.id_juzgado_local "
    sql += "WHERE  acuerdos_locales.fecha = '" + fechasql + "'"

    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = listaCorreosLigador(r["id_juicio_local"])
    for r in rv:
        r["acuerdos"] = acuerdoslocalesdiarios(r["id_juicio_local"])
    for dataMail in rv:
        dataMail['tipo'] = 'u_j_l'
        sendMulti(dataMail)

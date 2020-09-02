from flask import (
    Blueprint, request, jsonify
)
# Helpers
from api.utils.db import db_connect
from api.utils.mail.service import sendMulti
import api.utils.route_helpers as rh
from api.utils.pdf.fetch import pdf_service


bp = Blueprint(
    "federales", __name__,
    url_prefix='/federales')


# Get juzgados
@bp.route('/juzgados', methods=['GET'])
def juzgados():
    # mysql
    sql = "SELECT * from juzgados_federales"
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    return jsonify(rv)


@bp.route('/juicios', methods=['POST'])
def juicios():
    # Obtener los juicios federales la informacion
    id_despacho = request.get_json()['id_despacho']
    sql = "SELECT "
    sql += 'juzgados_federales.nombre as nombre_juzgado_federal, '
    sql += 'juicios_federales.id_juzgado_federal,  '
    sql += 'juicios_federales.actor,  '
    sql += 'juicios_federales.demandado,  '
    sql += 'juicios_federales.numero_de_expediente,  '
    sql += 'abogados_responsables_juicios_federales.id_juicio_federal,  '
    sql += 'abogados_responsables_juicios_federales.email,  '
    sql += 'usuarios.id_despacho  '
    sql += 'FROM abogados_responsables_juicios_federales '
    sql += 'LEFT JOIN usuarios ON usuarios.email = '
    sql += 'abogados_responsables_juicios_federales.email '
    sql += 'INNER JOIN juicios_federales on juicios_federales.id = '
    sql += 'abogados_responsables_juicios_federales.id_juicio_federal '
    sql += 'INNER JOIN juzgados_federales on juzgados_federales.id = '
    sql += 'juicios_federales.id_juzgado_federal '
    sql += 'WHERE usuarios.id_despacho  =  ' + str(id_despacho) + ' '
    sql += 'GROUP BY  abogados_responsables_juicios_federales.id_juicio_federal '
    sql += 'ORDER BY juicios_federales.id_juzgado_federal, '
    sql += 'juicios_federales.numero_de_expediente DESC;'
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = rh.correosLigadosJuiciosfederales(
            r["id_juicio_federal"])
    return jsonify(rv)


@bp.route('/alta_juicio', methods=['POST'])
def alta_juicio():
    # Ruta de alta juicio federal
    actor = request.get_json()['actor']
    demandado = request.get_json()['demandado']
    numero_de_expediente = request.get_json()['numero_de_expediente']
    id_juzgado_federal = request.get_json()['id_juzgado_federal']
    emails = request.get_json()['emails']

    if rh.validarExpedienteJuiciosfederales(
        numero_de_expediente, id_juzgado_federal
            ):
        return jsonify({
            'status': 400,
            'mensaje': 'Esta repetido el registro'})

    sql = "INSERT INTO juicios_federales "
    sql += "(actor, demandado, numero_de_expediente, id_juzgado_federal)"
    sql += " VALUES ('"
    sql += str(actor).lstrip().rstrip().upper() + "', '"
    sql += str(demandado).lstrip().rstrip().upper() + "', '"
    sql += str(numero_de_expediente) + "', '"
    sql += str(id_juzgado_federal) + "')"
    db_connect(sql)

    rh.registrarCorreosAbogadosfederales(
        numero_de_expediente, id_juzgado_federal, emails)
    rv = rh.dataActualizacionOinsercion(id_juzgado_federal, numero_de_expediente)

    pdf_service([rv])

    dataMail = rh.sqlenviarcorreo([rv])

    dataMail[0]['tipo'] = 'a_j_l'

    sendMulti(dataMail[0])

    # TODO
    # sedmail donde mande los datos y los acuerdos
    # sqlenviarcorreo
    # emails
    return jsonify({'status': 200})


@bp.route('/eliminar_juicio', methods=['POST'])
def eliminar_juicio():
    # Eliminar juicio federal
    id_juicio_federal = request.get_json()['id_juicio_federal']
    emails = request.get_json()['emails']
    numero_de_expediente = request.get_json()['numero_de_expediente']
    juzgado = request.get_json()['juzgado']

    data = {}
    data['tipo'] = 'd_j_l'

    data['emails'] = emails
    data['expediente'] = numero_de_expediente
    data["juzgado"] = juzgado

    sql = "DELETE FROM juicios_federales where id = " + str(id_juicio_federal)
    __, response = db_connect(sql)

    rh.eliminarAcuerdosfederales(id_juicio_federal)

    if response > 0:
        result = {'message': 'record delete'}
        sendMulti(data)
    else:
        result = {'message': 'no record found'}

    rh.eliminarCorreosAbogadosfederales(id_juicio_federal, emails)
    return jsonify({
        'status': 200, 'result': result
        })


@bp.route('/actualizar_juicio', methods=['POST'])
def actualizar_juicio():
    # Actualizar juicio federal
    orginalNumeroExpediente = request.get_json()['orginalNumeroExpediente']   #
    orginalJuzgado = request.get_json()['orginalJuzgado']                     #
    emailsEliminar = request.get_json()['emailsEliminar']                     #
    id_juicio_federal = request.get_json()['id_juicio_federal']                   #
    emails = request.get_json()['emails']
    id_juzgado_federal = request.get_json()['id_juzgado_local']
    numero_de_expediente = request.get_json()['numero_de_expediente']
    demandado = request.get_json()['demandado']
    actor = request.get_json()['actor']

    # from .utils.m_help import return_juzgado
    # data['juzgado_federal'] = return_juzgado(id_juzgado_federal)
    #  TODO
    # data['acuerdos'] = pdf(args)
    #
    if orginalNumeroExpediente is False:
        if rh.validarExpedienteJuiciosfederales(
            numero_de_expediente, id_juzgado_federal
                ):
            return jsonify({
                'status': 400,
                'mensaje': 'Esta repetido el registro'})

        rh.metodo_actualizar_juicio(
            actor, demandado, numero_de_expediente, id_juzgado_federal,
            emails, emailsEliminar, id_juicio_federal)
        rh.eliminarAcuerdosfederales(id_juicio_federal)
        rv = rh.dataActualizacionOinsercion(
            id_juzgado_federal, numero_de_expediente)

        pdf_service([rv])

        dataMail = rh.sqlenviarcorreo([rv])
        dataMail[0]['tipo'] = 'u_j_l'
        sendMulti(dataMail[0])

        return jsonify({'status': 200})

    if orginalJuzgado is True:
        rh.metodo_actualizar_juicio(
            actor, demandado, numero_de_expediente, id_juzgado_federal,
            emails, emailsEliminar, id_juicio_federal)

        rv = rh.dataActualizacionOinsercion(
            id_juzgado_federal, numero_de_expediente)
        dataMail = rh.sqlenviarcorreo([rv])
        dataMail[0]['tipo'] = 'u_j_l'
        sendMulti(dataMail[0])

        return jsonify({'status': 200})

    if rh.validarExpedienteJuiciosfederales(
        numero_de_expediente, id_juzgado_federal
            ):
        return jsonify({
            'status': 400, 'mensaje': 'Esta repetido el registro'
            })
    rh.metodo_actualizar_juicio(
        actor, demandado, numero_de_expediente, id_juzgado_federal,
        emails, emailsEliminar, id_juicio_federal)
    rh.eliminarAcuerdosfederales(id_juicio_federal)
    rv = rh.dataActualizacionOinsercion(id_juzgado_federal, numero_de_expediente)

    pdf_service([rv])
    dataMail = rh.sqlenviarcorreo([rv])
    dataMail[0]['tipo'] = 'u_j_l'
    sendMulti(dataMail[0])

    return jsonify({'status': 200})


@bp.route('/juicios_asignados', methods=['POST'])
def juicios_asignados():
    # Juicios federales asignados
    id_usuario = request.get_json()['id_usuario']
    sql = 'SELECT '
    sql += 'juzgados_federales.nombre as nombre_juzgado_federal, '
    sql += 'juicios_federales.id_juzgado_federal,  '
    sql += 'juicios_federales.actor,  '
    sql += 'juicios_federales.demandado,  '
    sql += 'juicios_federales.numero_de_expediente,  '
    sql += 'abogados_responsables_juicios_federales.id_juicio_federal,  '
    sql += 'abogados_responsables_juicios_federales.email,  '
    sql += 'usuarios.id_despacho  '
    sql += 'FROM abogados_responsables_juicios_federales '
    sql += 'LEFT JOIN usuarios ON usuarios.email = '
    sql += 'abogados_responsables_juicios_federales.email '
    sql += 'INNER JOIN juicios_federales on juicios_federales.id'
    sql += ' = abogados_responsables_juicios_federales.id_juicio_federal '
    sql += 'INNER JOIN juzgados_federales on juzgados_federales.id = '
    sql += 'juicios_federales.id_juzgado_federal '
    sql += 'WHERE usuarios.id  =  ' + str(id_usuario) + ' '
    sql += 'GROUP BY  abogados_responsables_juicios_federales.id_juicio_federal '
    sql += 'ORDER BY juicios_federales.id_juzgado_federal, '
    sql += 'juicios_federales.numero_de_expediente DESC;'

    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = rh.correosLigadosJuiciosfederales(r["id_juicio_federal"])
    return jsonify(rv)


@bp.route('/filtro_juicios', methods=['POST'])
def filtro_juicios():
    # Filtros Juicios federales
    id_despacho = request.get_json()['id_despacho']
    id_juzgado_federal = request.get_json()['id_juzgado_federal']
    numero_de_expediente = request.get_json()['numero_de_expediente']

    Where = ""
    if (
        len(numero_de_expediente) > 0 and
        str(numero_de_expediente).isspace() is False
            ):
        Where += " AND juicios_federales.numero_de_expediente like '%"
        Where += str(numero_de_expediente) + "%' "

    if id_juzgado_federal > 0:
        Where += " AND juicios_federales.id_juzgado_federal = '"
        Where += str(id_juzgado_federal) + "' "

    sql = 'SELECT '
    sql += 'juzgados_federales.nombre as nombre_juzgado_federal, '
    sql += 'juicios_federales.id_juzgado_federal,  '
    sql += 'juicios_federales.actor,  '
    sql += 'juicios_federales.demandado,  '
    sql += 'juicios_federales.numero_de_expediente,  '
    sql += 'abogados_responsables_juicios_federales.id_juicio_federal,  '
    sql += 'abogados_responsables_juicios_federales.email,  '
    sql += 'usuarios.id_despacho  '
    sql += 'FROM abogados_responsables_juicios_federales '
    sql += 'LEFT JOIN usuarios ON usuarios.email = '
    sql += 'abogados_responsables_juicios_federales.email '
    sql += 'INNER JOIN juicios_federales on juicios_federales.id '
    sql += '= abogados_responsables_juicios_federales.id_juicio_federal '
    sql += 'INNER JOIN juzgados_federales on juzgados_federales.id '
    sql += '= juicios_federales.id_juzgado_federal '
    sql += 'WHERE usuarios.id_despacho  =  '
    sql += str(id_despacho) + ' ' + Where
    sql += 'GROUP BY  abogados_responsables_juicios_federales.id_juicio_federal '
    sql += 'ORDER BY juicios_federales.id_juzgado_federal, '
    sql += 'juicios_federales.numero_de_expediente DESC;'

    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = rh.correosLigadosJuiciosfederales(
            r["id_juicio_federal"])
    return jsonify(rv)


@bp.route('/detalle_expediente', methods=['POST'])
def detalle_expediente():
    id_juzgado_federal = request.get_json()['id_juzgado_federal']
    numero_de_expediente = request.get_json()['numero_de_expediente']
    return jsonify(
        rh.informacionfederalExpedienteHistorico(
            numero_de_expediente, id_juzgado_federal))


@bp.route('/juicios_fecha', methods=['POST'])
def juicios_fecha():
    # Obtener los juicios federales la informacion
    id_despacho = request.get_json()['id_despacho']
    fecha = request.get_json()['fecha']

    sql = "SELECT "
    sql += 'juzgados_federales.nombre as nombre_juzgado_federal, '
    sql += 'juicios_federales.id_juzgado_federal,  '
    sql += 'juicios_federales.actor,  '
    sql += 'juicios_federales.demandado,  '
    sql += 'juicios_federales.numero_de_expediente,  '
    sql += 'abogados_responsables_juicios_federales.id_juicio_federal,  '
    sql += 'usuarios.id_despacho  '
    sql += 'FROM abogados_responsables_juicios_federales '
    sql += 'LEFT JOIN usuarios ON usuarios.email = '
    sql += 'abogados_responsables_juicios_federales.email '
    sql += 'INNER JOIN juicios_federales on juicios_federales.id = '
    sql += 'abogados_responsables_juicios_federales.id_juicio_federal '
    sql += 'INNER JOIN juzgados_federales on juzgados_federales.id = '
    sql += 'juicios_federales.id_juzgado_federal '
    sql += 'INNER JOIN acuerdos_federales on acuerdos_federales.id_juicio_federal = '
    sql += 'juicios_federales.id '
    sql += 'WHERE usuarios.id_despacho  =  ' + str(id_despacho) + ' '
    sql += 'AND acuerdos_federales.fecha = "' + str(fecha) + '" '
    sql += 'GROUP BY  abogados_responsables_juicios_federales.id_juicio_federal '
    sql += 'ORDER BY juicios_federales.id_juzgado_federal, '
    sql += 'juicios_federales.numero_de_expediente DESC;'
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = rh.correosLigadosJuiciosfederales(
            r["id_juicio_federal"])
    return jsonify(rv)

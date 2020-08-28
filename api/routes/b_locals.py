from flask import (
    Blueprint, request, jsonify
)
# Helpers
from api.utils.db import db_connect
# from api.utils.mail.service import sendMulti
import api.utils.route_helpers as rh


bp = Blueprint(
    "locales", __name__,
    url_prefix='/locales')


# Get juzgados
@bp.route('/juzgados', methods=['GET'])
def juzgados():
    # mysql
    sql = "SELECT * from juzgados_locales"
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    return jsonify(rv)


@bp.route('/juicios', methods=['POST'])
def juicios():
    # Obtener los juicios locales la informacion
    id_despacho = request.get_json()['id_despacho']
    sql = "SELECT "
    sql += 'juzgados_locales.nombre as nombre_juzgado_local, '
    sql += 'juicios_locales.id_juzgado_local,  '
    sql += 'juicios_locales.actor,  '
    sql += 'juicios_locales.demandado,  '
    sql += 'juicios_locales.numero_de_expediente,  '
    sql += 'abogados_responsables_juicios_locales.id_juicio_local,  '
    sql += 'abogados_responsables_juicios_locales.email,  '
    sql += 'usuarios.id_despacho  '
    sql += 'FROM abogados_responsables_juicios_locales '
    sql += 'LEFT JOIN usuarios ON usuarios.email = '
    sql += 'abogados_responsables_juicios_locales.email '
    sql += 'INNER JOIN juicios_locales on juicios_locales.id = '
    sql += 'abogados_responsables_juicios_locales.id_juicio_local '
    sql += 'INNER JOIN juzgados_locales on juzgados_locales.id = '
    sql += 'juicios_locales.id_juzgado_local '
    sql += 'WHERE usuarios.id_despacho  =  ' + str(id_despacho) + ' '
    sql += 'GROUP BY  abogados_responsables_juicios_locales.id_juicio_local '
    sql += 'ORDER BY juicios_locales.id_juzgado_local, '
    sql += 'juicios_locales.numero_de_expediente DESC;'
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = rh.correosLigadosJuiciosLocales(
            r["id_juicio_local"])
    return jsonify(rv)


@bp.route('/alta_juicio', methods=['POST'])
def alta_juicio():
    # Ruta de alta juicio local
    actor = request.get_json()['actor']
    demandado = request.get_json()['demandado']
    numero_de_expediente = request.get_json()['numero_de_expediente']
    id_juzgado_local = request.get_json()['id_juzgado_local']
    emails = request.get_json()['emails']

    if rh.validarExpedienteJuiciosLocales(
        numero_de_expediente, id_juzgado_local
            ):
        return jsonify({
            'status': 400,
            'mensaje': 'Esta repetido el registro'})

    sql = "INSERT INTO juicios_locales "
    sql += "(actor, demandado, numero_de_expediente, id_juzgado_local)"
    sql += " VALUES ('"
    sql += str(actor).lstrip().rstrip().upper() + "', '"
    sql += str(demandado).lstrip().rstrip().upper() + "', '"
    sql += str(numero_de_expediente) + "', '"
    sql += str(id_juzgado_local) + "')"
    db_connect(sql)

    rh.registrarCorreosAbogadosLocales(
        numero_de_expediente, id_juzgado_local, emails)
    rv = rh.dataActualizacionOinsercion(id_juzgado_local, numero_de_expediente)

    from api.utils.pdf.fetch import fetch_pdf_service
    fetch_pdf_service([rv])
    # TODO
    # sedmail donde mande los datos y los acuerdos
    # sqlenviarcorreo
    # emails
    return jsonify({'status': 200})


@bp.route('/eliminar_juicio', methods=['POST'])
def eliminar_juicio():
    # Eliminar juicio local
    id_juicio_local = request.get_json()['id_juicio_local']
    emails = request.get_json()['emails']

    sql = "DELETE FROM juicios_locales where id = " + str(id_juicio_local)
    __, response = db_connect(sql)

    rh.eliminarAcuerdosLocales(id_juicio_local)

    if response > 0:
        result = {'message': 'record delete'}
    else:
        result = {'message': 'no record found'}

    rh.eliminarCorreosAbogadosLocales(id_juicio_local, emails)
    return jsonify({
        'status': 200, 'result': result
        })


@bp.route('/actualizar_juicio', methods=['POST'])
def actualizar_juicio():
    # Actualizar juicio local
    orginalNumeroExpediente = request.get_json()['orginalNumeroExpediente']   #
    orginalJuzgado = request.get_json()['orginalJuzgado']                     #
    emailsEliminar = request.get_json()['emailsEliminar']                     #
    id_juicio_local = request.get_json()['id_juicio_local']                   #
    emails = request.get_json()['emails']
    id_juzgado_local = request.get_json()['id_juzgado_local']
    numero_de_expediente = request.get_json()['numero_de_expediente']
    demandado = request.get_json()['demandado']
    actor = request.get_json()['actor']

    # from .utils.m_help import return_juzgado
    data = {}
    data['tipo'] = 'a_j_l'

    data['emails'] = emails
    data['numero_de_expediente'] = numero_de_expediente
    data['actor'] = actor
    data['demandado'] = demandado
    # data['juzgado_local'] = return_juzgado(id_juzgado_local)
    #  TODO
    # data['acuerdos'] = pdf(args)
    #
    if orginalNumeroExpediente is False:
        if rh.validarExpedienteJuiciosLocales(
            numero_de_expediente, id_juzgado_local
                ):
            return jsonify({
                'status': 400,
                'mensaje': 'Esta repetido el registro'})

        rh.metodo_actualizar_juicio(
            actor, demandado, numero_de_expediente, id_juzgado_local,
            emails, emailsEliminar, id_juicio_local)
        rh.eliminarAcuerdosLocales(id_juicio_local)
        rv = rh.dataActualizacionOinsercion(
            id_juzgado_local, numero_de_expediente)

        from api.utils.pdf.fetch import fetch_history
        fetch_history([rv])
        # sendMulti(data)
        return jsonify({'status': 200})

    if orginalJuzgado is True:
        rh.metodo_actualizar_juicio(
            actor, demandado, numero_de_expediente, id_juzgado_local,
            emails, emailsEliminar, id_juicio_local)
        # sendMulti(data)
        return jsonify({'status': 200})

    if rh.validarExpedienteJuiciosLocales(
        numero_de_expediente, id_juzgado_local
            ):
        return jsonify({
            'status': 400, 'mensaje': 'Esta repetido el registro'
            })
    rh.metodo_actualizar_juicio(
        actor, demandado, numero_de_expediente, id_juzgado_local,
        emails, emailsEliminar, id_juicio_local)
    rh.eliminarAcuerdosLocales(id_juicio_local)
    rv = rh.dataActualizacionOinsercion(id_juzgado_local, numero_de_expediente)

    from api.utils.pdf.fetch import fetch_history
    fetch_history([rv])
    # sendMulti(data)
    return jsonify({'status': 200})


@bp.route('/juicios_asignados', methods=['POST'])
def juicios_asignados():
    # Juicios locales asignados
    id_usuario = request.get_json()['id_usuario']
    sql = 'SELECT '
    sql += 'juzgados_locales.nombre as nombre_juzgado_local, '
    sql += 'juicios_locales.id_juzgado_local,  '
    sql += 'juicios_locales.actor,  '
    sql += 'juicios_locales.demandado,  '
    sql += 'juicios_locales.numero_de_expediente,  '
    sql += 'abogados_responsables_juicios_locales.id_juicio_local,  '
    sql += 'abogados_responsables_juicios_locales.email,  '
    sql += 'usuarios.id_despacho  '
    sql += 'FROM abogados_responsables_juicios_locales '
    sql += 'LEFT JOIN usuarios ON usuarios.email = '
    sql += 'abogados_responsables_juicios_locales.email '
    sql += 'INNER JOIN juicios_locales on juicios_locales.id'
    sql += ' = abogados_responsables_juicios_locales.id_juicio_local '
    sql += 'INNER JOIN juzgados_locales on juzgados_locales.id = '
    sql += 'juicios_locales.id_juzgado_local '
    sql += 'WHERE usuarios.id  =  ' + str(id_usuario) + ' '
    sql += 'GROUP BY  abogados_responsables_juicios_locales.id_juicio_local '
    sql += 'ORDER BY juicios_locales.id_juzgado_local, '
    sql += 'juicios_locales.numero_de_expediente DESC;'

    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = rh.correosLigadosJuiciosLocales(r["id_juicio_local"])
    return jsonify(rv)


@bp.route('/filtro_juicios', methods=['POST'])
def filtro_juicios():
    # Filtros Juicios locales
    id_despacho = request.get_json()['id_despacho']
    id_juzgado_local = request.get_json()['id_juzgado_local']
    numero_de_expediente = request.get_json()['numero_de_expediente']

    Where = ""
    if (
        len(numero_de_expediente) > 0 and
        str(numero_de_expediente).isspace() is False
            ):
        Where += " AND juicios_locales.numero_de_expediente like '%"
        Where += str(numero_de_expediente) + "%' "

    if id_juzgado_local > 0:
        Where += " AND juicios_locales.id_juzgado_local = '"
        Where += str(id_juzgado_local) + "' "

    sql = 'SELECT '
    sql += 'juzgados_locales.nombre as nombre_juzgado_local, '
    sql += 'juicios_locales.id_juzgado_local,  '
    sql += 'juicios_locales.actor,  '
    sql += 'juicios_locales.demandado,  '
    sql += 'juicios_locales.numero_de_expediente,  '
    sql += 'abogados_responsables_juicios_locales.id_juicio_local,  '
    sql += 'abogados_responsables_juicios_locales.email,  '
    sql += 'usuarios.id_despacho  '
    sql += 'FROM abogados_responsables_juicios_locales '
    sql += 'LEFT JOIN usuarios ON usuarios.email = '
    sql += 'abogados_responsables_juicios_locales.email '
    sql += 'INNER JOIN juicios_locales on juicios_locales.id '
    sql += '= abogados_responsables_juicios_locales.id_juicio_local '
    sql += 'INNER JOIN juzgados_locales on juzgados_locales.id '
    sql += '= juicios_locales.id_juzgado_local '
    sql += 'WHERE usuarios.id_despacho  =  '
    sql += str(id_despacho) + ' ' + Where
    sql += 'GROUP BY  abogados_responsables_juicios_locales.id_juicio_local '
    sql += 'ORDER BY juicios_locales.id_juzgado_local, '
    sql += 'juicios_locales.numero_de_expediente DESC;'

    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = rh.correosLigadosJuiciosLocales(
            r["id_juicio_local"])
    return jsonify(rv)

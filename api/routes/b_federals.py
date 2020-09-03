from flask import (
    Blueprint, request, jsonify
)
# Helpers
from api.utils.db import db_connect
import api.utils.route_helpers.federals as rh
from api.utils.mail.service import sendMulti


bp = Blueprint(
    "federales", __name__,
    url_prefix='/federales')


# Get juzgados
@bp.route('/circuitos_federales', methods=['GET'])
def circuitos_federales():
    # mysql
    sql = "SELECT * from circuitos_federales"
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    return jsonify(rv)


@bp.route('/juzgados_federales', methods=['POST'])
def juzgados_federales():
    cir_id = request.get_json()['cir_id']
    sql = "SELECT * from juzgados_federales"
    sql += " WHERE juzgados_federales.cir_id = " + str(cir_id)
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    return jsonify(rv)


@bp.route('/tipo_de_juicios_federales', methods=['POST'])
def tipo_de_juicios_federales():
    org_id = request.get_json()['org_id']
    sql = "SELECT * from tipo_de_juicios_federales"
    sql += " WHERE org_id = " + str(org_id)
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    return jsonify(rv)


@bp.route('/alta_juicios_federales', methods=['POST'])
def alta_juicios_federales():

    cir_id = request.get_json()['cir_id']
    id_org = request.get_json()['id_org']
    t_ast = request.get_json()['t_ast']
    n_exp = request.get_json()['n_exp']

    data = {}

    data['cir_id'] = cir_id
    data['id_org'] = id_org
    data['t_ast'] = t_ast
    data['n_exp'] = n_exp
    data['tipo'] = 'a_j_f'

    if rh.validarJuicioFederal(data):
        return jsonify({
                'status': 400,
                'mensaje': 'Esta repetido el registro'})

    Quejoso_Actor_Recurrente_Concursada = request.get_json()['Quejoso_Actor_Recurrente_Concursada']
    Tercero_Interesado_Demandado_Acreedor = request.get_json()['Tercero_Interesado_Demandado_Acreedor']
    Autoridades = request.get_json()['Autoridades']
    listaCorreoAbogadosFederales = request.get_json()['listaCorreoAbogadosFederales']

    sql = "INSERT INTO juicios_federales "
    sql += "(cir_id, id_org, t_ast, n_exp, Quejoso_Actor_Recurrente_Concursada,Tercero_Interesado_Demandado_Acreedor,Autoridades )"
    sql += " VALUES ("
    sql += str(cir_id) + ", "
    sql += str(id_org) + ", "
    sql += str(t_ast) + ", '"
    sql += str(n_exp).lstrip().rstrip().upper() + "', '"
    sql += str(Quejoso_Actor_Recurrente_Concursada).lstrip().rstrip().upper() + "', '"
    sql += str(Tercero_Interesado_Demandado_Acreedor).lstrip().rstrip().upper() + "', '"
    sql += str(Autoridades).lstrip().rstrip().upper() + "')"
    db_connect(sql)

    rh.registrarCorreosAbogadosFederales(data, listaCorreoAbogadosFederales)
    rh.insertarAcuerdosDB([data])
    return jsonify({'status': 200})


@bp.route('/acuerdos_federales', methods=['POST'])
def acuerdos_federales():
    id_org = request.get_json()['id_org']
    t_ast = request.get_json()['t_ast']
    n_exp = request.get_json()['n_exp']
    data = {}
    data['id_org'] = id_org
    data['t_ast'] = t_ast
    data['n_exp'] = n_exp
    d = rh.get_acuerdos(data)
    return jsonify(d)


@bp.route('/juicios_federales', methods=['POST'])
def juicios_federales():
    id_despacho = request.get_json()['id_despacho']
    sql = "SELECT juicios_federales.id as id_juicio_federal,"
    sql += "juicios_federales.id_org, circuitos_federales.NOM_LARGO,"
    sql += "circuitos_federales.NOM_CIR, juzgados_federales.cir_id,"
    sql += "juzgados_federales.nombre_juzgado,"
    sql += "tipo_de_juicios_federales.t_ast, tipo_de_juicios_federales.nombre_tipo_juicio,"
    sql += "usuarios.id_despacho, juicios_federales.Quejoso_Actor_Recurrente_Concursada,"
    sql += "juicios_federales.Tercero_Interesado_Demandado_Acreedor,"
    sql += "juicios_federales.n_exp,"
    sql += "juicios_federales.Autoridades FROM abogados_responsables_juicios_federales "
    sql += "INNER JOIN usuarios on usuarios.email = abogados_responsables_juicios_federales.email "
    sql += "INNER JOIN juicios_federales on juicios_federales.id = abogados_responsables_juicios_federales.id_juicio_federal "
    sql += "INNER JOIN circuitos_federales ON circuitos_federales.c_id = juicios_federales.cir_id "
    sql += "INNER JOIN juzgados_federales ON juzgados_federales.org_id = juicios_federales.id_org "
    sql += "INNER JOIN tipo_de_juicios_federales ON tipo_de_juicios_federales.t_ast = juicios_federales.t_ast "
    sql += "WHERE usuarios.id_despacho  = " + str(id_despacho)
    sql += " GROUP BY  abogados_responsables_juicios_federales.id_juicio_federal "
    sql += "ORDER BY circuitos_federales.id,  juicios_federales.n_exp DESC"
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = rh.listaCorreosLigador(
            r["id_juicio_federal"])
    return jsonify(rv)


@bp.route('/filtro_juicios_federales', methods=['POST'])
def filtro_juicios():
    # Filtros Juicios locales

    cir_id = request.get_json()['cir_id']
    id_org = request.get_json()['id_org']
    t_ast = request.get_json()['t_ast']
    n_exp = request.get_json()['n_exp']
    id_despacho = request.get_json()['id_despacho']

    Where = ""
    if (
        len(n_exp) > 0 and
        str(n_exp).isspace() is False
            ):
        Where += " AND juicios_federales.n_exp like '%"
        Where += str(n_exp) + "%' "

    if cir_id > 0:
        Where += " AND juicios_federales.cir_id = "
        Where += str(cir_id) + " "

    if id_org > 0:
        Where += " AND juicios_federales.id_org = "
        Where += str(id_org) + " "

    if t_ast > 0:
        Where += " AND juicios_federales.t_ast = "
        Where += str(t_ast) + " "

    sql = "SELECT juicios_federales.id as id_juicio_federal,"
    sql += "juicios_federales.id_org, circuitos_federales.NOM_LARGO,"
    sql += "circuitos_federales.NOM_CIR, juzgados_federales.cir_id,"
    sql += "juzgados_federales.nombre_juzgado,"
    sql += "tipo_de_juicios_federales.t_ast, tipo_de_juicios_federales.nombre_tipo_juicio,"
    sql += "usuarios.id_despacho, juicios_federales.Quejoso_Actor_Recurrente_Concursada,"
    sql += "juicios_federales.Tercero_Interesado_Demandado_Acreedor,"
    sql += "juicios_federales.n_exp,"
    sql += "juicios_federales.Autoridades FROM abogados_responsables_juicios_federales "
    sql += "INNER JOIN usuarios on usuarios.email = abogados_responsables_juicios_federales.email "
    sql += "INNER JOIN juicios_federales on juicios_federales.id = abogados_responsables_juicios_federales.id_juicio_federal "
    sql += "INNER JOIN circuitos_federales ON circuitos_federales.c_id = juicios_federales.cir_id "
    sql += "INNER JOIN juzgados_federales ON juzgados_federales.org_id = juicios_federales.id_org "
    sql += "INNER JOIN tipo_de_juicios_federales ON tipo_de_juicios_federales.t_ast = juicios_federales.t_ast "
    sql += "WHERE usuarios.id_despacho  = " + str(id_despacho) + Where
    sql += " GROUP BY  abogados_responsables_juicios_federales.id_juicio_federal "
    sql += "ORDER BY circuitos_federales.id,  juicios_federales.n_exp DESC"
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = rh.listaCorreosLigador(
            r["id_juicio_federal"])
    return jsonify(rv)


@bp.route('/eliminar_juicio_federal', methods=['POST'])
def eliminar_juicio_federal():
    # Eliminar juicio local
    id_juicio_federal = request.get_json()['id_juicio_federal']
    emails = request.get_json()['emails']

    NOM_CIR = request.get_json()['NOM_CIR']
    NOM_LARGO = request.get_json()['NOM_LARGO']
    n_exp = request.get_json()['n_exp']
    nombre_juzgado = request.get_json()['nombre_juzgado']
    nombre_tipo_juicio = request.get_json()['nombre_tipo_juicio']

    data = {}
    data['tipo'] = 'd_j_f'
    data['NOM_LARGO'] = NOM_LARGO
    data['NOM_CIR'] = NOM_CIR
    data['nombre_juzgado'] = nombre_juzgado
    data['nombre_tipo_juicio'] = nombre_tipo_juicio
    data['n_exp'] = n_exp
    data['emails'] = emails

    sql = "DELETE FROM juicios_federales where id = " + str(id_juicio_federal)
    __, response = db_connect(sql)

    rh.eliminarAcuerdosFederales(id_juicio_federal)
    rh.eliminarCorreosAbogadosFederales(id_juicio_federal, emails)

    if response > 0:
        result = {'message': 'record delete'}
        sendMulti(data)
    else:
        result = {'message': 'no record found'}

    return jsonify({
        'status': 200, 'result': result
        })

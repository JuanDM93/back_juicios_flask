from flask import (
    Blueprint, request, jsonify
)
# Helpers
from api.utils.db import db_connect
import api.utils.route_helpers.federals as rh


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
    sql += str(Autoridades) + "')"
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

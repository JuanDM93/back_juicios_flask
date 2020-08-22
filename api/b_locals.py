from flask import (
    Blueprint, request, jsonify
)

bp = Blueprint(
    "locales", __name__,
    url_prefix='/locales')

#DB
from .db import db_connect

# Mail
from .utils.mail.service import sendMulti

# Helpers
from .utils.route_helpers import *

# Get juzgados
@bp.route('/juzgados', methods=['GET'])
def juzgados():
    # mysql
    sql = "SELECT * from juzgados_locales"
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    return jsonify(rv)

# Obtener los juicios locales la informacion
@bp.route('/juicios', methods=['POST'])
def juicios():
    id_despacho = request.get_json()['id_despacho']
    sql = "SELECT "
    sql += 'juzgados_locales.nombre as nombre_juzgado_local, ' \
    'juicios_locales.id_juzgado_local,  ' \
    'juicios_locales.actor,  ' \
    'juicios_locales.demandado,  ' \
    'juicios_locales.numero_de_expediente,  ' \
    'abogados_responsables_juicios_locales.id_juicio_local,  ' \
    'abogados_responsables_juicios_locales.email,  ' \
    'usuarios.id_despacho  ' \
    'FROM abogados_responsables_juicios_locales ' \
    'LEFT JOIN usuarios ON usuarios.email = abogados_responsables_juicios_locales.email  ' \
    'INNER JOIN juicios_locales on juicios_locales.id = abogados_responsables_juicios_locales.id_juicio_local ' \
    'INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local ' \
    'WHERE usuarios.id_despacho  =  ' + str(id_despacho) + ' ' \
    'GROUP BY  abogados_responsables_juicios_locales.id_juicio_local ' \
    'ORDER BY juicios_locales.id_juzgado_local, juicios_locales.numero_de_expediente DESC;'                
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = correosLigadosJuiciosLocales(
            r["id_juicio_local"])
    return jsonify(rv)

# Ruta de alta juicio local
@bp.route('/alta_juicio', methods=['POST'])
def alta_juicio():
    actor = request.get_json()['actor']
    demandado = request.get_json()['demandado']
    numero_de_expediente = request.get_json()['numero_de_expediente']
    id_juzgado_local = request.get_json()['id_juzgado_local']
    emails = request.get_json()['emails']

    if validarExpedienteJuiciosLocales(numero_de_expediente, id_juzgado_local):
        return jsonify({
            'status' : 400,
            'mensaje': 'Esta repetido el registro' })
    else:
        sql = "INSERT INTO juicios_locales "
        sql += "(actor, demandado, numero_de_expediente, id_juzgado_local) VALUES ('"
        sql += str(actor).lstrip().rstrip().upper() + "', '"
        sql += str(demandado).lstrip().rstrip().upper() + "', '"
        sql += str(numero_de_expediente) + "', '"
        sql += str(id_juzgado_local) + "')"
        db_connect(sql)

        registrarCorreosAbogadosLocales(
            numero_de_expediente, id_juzgado_local, emails)
        
        sql = "select juicios_locales.id as id_juicio_local, juzgados_locales.nombre as juzgado ,juicios_locales.numero_de_expediente as expediente"
        sql += " from juicios_locales INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local "
        sql += "WHERE juicios_locales.id_juzgado_local = "+ str(id_juzgado_local)+ " and  juicios_locales.numero_de_expediente = '"
        sql += str(numero_de_expediente) +"'"
        cur, __ = db_connect(sql)
        rv = cur.fetchone()
        
        from .utils.pdf.parse import fetch_history
        fetch_history([rv])

        ## TODO
        ##sedmail donde mande los datos y los acuerdos
        ##sqlenviarcorreo
        ## emails
        
        return jsonify({'status' : 200})

# Eliminar juicio local
@bp.route('/eliminar_juicio', methods=['POST'])
def eliminar_juicio():
    id_juicio_local = request.get_json()['id_juicio_local']
    emails = request.get_json()['emails']
    
    sql = "DELETE FROM juicios_locales where id = " + str(id_juicio_local)
    __, response = db_connect(sql)
    
    sql2 = "DELETE FROM acuerdos_locales where id_juicio_local = " + str(id_juicio_local)
    __, response = db_connect(sql2)
    
    if response > 0:
        result = {'message': 'record delete'}
    else:
        result = {'message': 'no record found'}
    
    eliminarCorreosAbogadosLocales(id_juicio_local, emails)
    return jsonify({
        'status': 200, 'result': result
        })

# Actualizar juicio local
@bp.route('/actualizar_juicio', methods=['POST'])
def actualizar_juicio():

    orginalNumeroExpediente = request.get_json()['orginalNumeroExpediente']#
    orginalJuzgado = request.get_json()['orginalJuzgado']#
    emailsEliminar = request.get_json()['emailsEliminar']#
    id_juicio_local = request.get_json()['id_juicio_local']#
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

    #data['acuerdos'] = pdf(args)
    ##

    if orginalNumeroExpediente == False:
        if validarExpedienteJuiciosLocales(numero_de_expediente, id_juzgado_local):
            return jsonify({
                'status' : 400, 'mensaje': 'Esta repetido el registro'
                })
        else:
            metodo_actualizar_juicio(
                actor, demandado, numero_de_expediente, id_juzgado_local,
                emails, emailsEliminar, id_juicio_local)
            sendMulti(data)
            return jsonify({
                'status': 200
                })
    else:
        if orginalJuzgado == True:
            metodo_actualizar_juicio(
                actor, demandado, numero_de_expediente, id_juzgado_local,
                emails, emailsEliminar, id_juicio_local)
            sendMulti(data)
            return jsonify({
                'status': 200
                })
        else:
            if validarExpedienteJuiciosLocales(numero_de_expediente, id_juzgado_local):
                return jsonify({
                    'status' : 400, 'mensaje': 'Esta repetido el registro'
                    })
            else:
                metodo_actualizar_juicio(
                    actor, demandado, numero_de_expediente, id_juzgado_local,
                    emails, emailsEliminar, id_juicio_local)
                sendMulti(data)
                return jsonify({
                    'status': 200
                    })

# Juicios locales asignados
@bp.route('/juicios_asignados', methods=['POST'])
def juicios_asignados():
    id_usuario = request.get_json()['id_usuario']

    sql = 'SELECT ' \
    'juzgados_locales.nombre as nombre_juzgado_local, ' \
    'juicios_locales.id_juzgado_local,  '\
    'juicios_locales.actor,  '\
    'juicios_locales.demandado,  '\
    'juicios_locales.numero_de_expediente,  '\
    'abogados_responsables_juicios_locales.id_juicio_local,  '\
    'abogados_responsables_juicios_locales.email,  '\
    'usuarios.id_despacho  '\
    'FROM abogados_responsables_juicios_locales '\
    'LEFT JOIN usuarios ON usuarios.email = abogados_responsables_juicios_locales.email  '\
    'INNER JOIN juicios_locales on juicios_locales.id = abogados_responsables_juicios_locales.id_juicio_local '\
    'INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local '\
    'WHERE usuarios.id  =  '+ str(id_usuario) +' '\
    'GROUP BY  abogados_responsables_juicios_locales.id_juicio_local '\
    'ORDER BY juicios_locales.id_juzgado_local, juicios_locales.numero_de_expediente DESC;'    

    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    
    for r in rv:
        r["emails"] = correosLigadosJuiciosLocales(r["id_juicio_local"])
    return jsonify(rv)
    
# Filtros Juicios locales
@bp.route('/filtro_juicios', methods=['POST'])
def filtro_juicios():
    id_despacho = request.get_json()['id_despacho']
    id_juzgado_local = request.get_json()['id_juzgado_local']
    numero_de_expediente = request.get_json()['numero_de_expediente'] 
    
    Where = ""
    if len(numero_de_expediente) > 0 and str(numero_de_expediente).isspace() == False:
        Where += " AND juicios_locales.numero_de_expediente like '%"+ str(numero_de_expediente) +"%' "
  
    if id_juzgado_local > 0:
        Where += " AND juicios_locales.id_juzgado_local = '"+ str(id_juzgado_local) +"' "
                    
    sql = 'SELECT ' \
    'juzgados_locales.nombre as nombre_juzgado_local, '\
    'juicios_locales.id_juzgado_local,  '\
    'juicios_locales.actor,  '\
    'juicios_locales.demandado,  '\
    'juicios_locales.numero_de_expediente,  '\
    'abogados_responsables_juicios_locales.id_juicio_local,  '\
    'abogados_responsables_juicios_locales.email,  '\
    'usuarios.id_despacho  '\
    'FROM abogados_responsables_juicios_locales '\
    'LEFT JOIN usuarios ON usuarios.email = abogados_responsables_juicios_locales.email  '\
    'INNER JOIN juicios_locales on juicios_locales.id = abogados_responsables_juicios_locales.id_juicio_local '\
    'INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local '\
    'WHERE usuarios.id_despacho  =  '+ str(id_despacho) +' '+ Where + \
    'GROUP BY  abogados_responsables_juicios_locales.id_juicio_local '\
    'ORDER BY juicios_locales.id_juzgado_local, juicios_locales.numero_de_expediente DESC;'\

    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = correosLigadosJuiciosLocales(
            r["id_juicio_local"])
    return jsonify(rv)

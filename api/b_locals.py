from flask import (
    Blueprint, request, jsonify
)

bp = Blueprint(
    "locales", __name__,
    url_prefix='/locales')

#DB
from .db import db_connect

# Mail
from .utils.mail import sendMulti

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
        
        ## TODO
        sql_juzgado = ''
        cur, res = db_connect(sql_juzgado)
        juzgado = cur.fetchone()

        data = []
        juzgado = {
            'juzgado': juzgado,
            'expediente': numero_de_expediente}
        data.append(juzgado)

        from .utils.pdf.parse import fetch_history
        fetch_history(data)
        ##

        return jsonify({'status' : 200})

# Eliminar juicio local
@bp.route('/eliminar_juicio', methods=['POST'])
def eliminar_juicio():
    id_juicio_local = request.get_json()['id_juicio_local']
    emails = request.get_json()['emails']
    
    sql = "DELETE FROM juicios_locales where id = " + str(id_juicio_local)
    __, response = db_connect(sql)
    
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

##TODO##
# should reuse bellow code (local, federal)
from flask import current_app

# Eliminar abogados reponsables
def eliminarCorreosAbogadosLocales(id_juicio_local, listaCorreoAbogadosLocalesElimar):
    data = "("
    for CorreoAbogadoLocal in listaCorreoAbogadosLocalesElimar:
        data += "'" + CorreoAbogadoLocal + "', "
    data = data[:-2]
    data += ")"
    sql = "DELETE from abogados_responsables_juicios_locales WHERE email IN " + data
    sql += " AND id_juicio_local = " + str(id_juicio_local) 
    db_connect(sql)

# Metodo para asignar abogados responsables
def registrarCorreosAbogadosLocales(
    numero_de_expediente, id_juzgado_local, listaCorreoAbogadosLocales
    ):
    sql = "SELECT id FROM juicios_locales WHERE numero_de_expediente = '"
    sql += str(numero_de_expediente) 
    sql += "' AND id_juzgado_local = " + str(id_juzgado_local)
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    id_juicio_local = rv["id"]
    
    data = ""
    for CorreoAbogadoLocal in listaCorreoAbogadosLocales:
        data += "('" + str(id_juicio_local) +"', '" + CorreoAbogadoLocal + "'), "
        #enviarCorreo(correoabogadolocal, 'texto formateado'--data['nombre'])
    data = data[:-2]
    
    sql = "INSERT INTO abogados_responsables_juicios_locales (id_juicio_local, email) VALUES"
    sql += data
    db_connect(sql)

# Correos juicios locales
def correosLigadosJuiciosLocales(id_juicio_local):
    sql = "SELECT email " 
    sql += "FROM abogados_responsables_juicios_locales "
    sql += "WHERE id_juicio_local  = " + str(id_juicio_local)                
    cur, response = db_connect(sql)
    rv = cur.fetchall()
    return rv    

# Helper juicio local
def metodo_actualizar_juicio(
    actor, demandado, numero_de_expediente, id_juzgado_local,
    emails, emailsEliminar, id_juicio_local
    ):

    sql = "UPDATE juicios_locales SET "
    sql += "actor = '" + str(actor) + "', " 
    sql += "demandado = '" + str(demandado) + "', "
    sql += "numero_de_expediente = '" + str(numero_de_expediente) + "', "
    sql += "id_juzgado_local = '" + str(id_juzgado_local) + "' "
    sql += " WHERE id = " + str(id_juicio_local)
    db_connect(sql)

    eliminarCorreosAbogadosLocales(id_juicio_local, emailsEliminar)
    registrarCorreosAbogadosLocales(numero_de_expediente, id_juzgado_local, emails)

# Validar expediente
def validarExpedienteJuiciosLocales(numero_de_expediente, id_juzgado_local):
    sql = "SELECT COUNT(1) AS BIT FROM juicios_locales "
    sql += "WHERE numero_de_expediente = '" + str(numero_de_expediente)
    sql += "' AND id_juzgado_local = " + str(id_juzgado_local)
    cur, __ = db_connect(sql) 

    rv = cur.fetchone()
    if rv["BIT"] == 0 :
        return False
    else:
        return True

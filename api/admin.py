from flask import (
    Blueprint, request, jsonify
)
#DB
from .db import db_connect

# BCRYPT
from .utils.auth import bcrypt

from .utils.route_helpers import *


bp = Blueprint(
    "admin", __name__,
    url_prefix='/admin')

# REGISTER
@bp.route('/register', methods=['POST'])
def register():
    # qs
    apellido_paterno = request.get_json()['apellido_paterno']
    apellido_materno = request.get_json()['apellido_materno']
    nombre = request.get_json()['nombre']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(
        request.get_json()['password']).decode('utf-8')
    id_tipo_usuario = request.get_json()['id_tipo_usuario']
    id_despacho = request.get_json()['id_despacho']
    creado = datetime.utcnow()

    # sql
    sql = "INSERT INTO usuarios ("
    sql += "apellido_paterno, apellido_materno, nombre, email, password, id_tipo_usuario, id_despacho, creado"
    sql += ") VALUES ('"
    sql += str(apellido_paterno).lstrip().rstrip().upper() + "', '" 
    + str(apellido_materno).lstrip().rstrip().upper() + "', '"
    + str(nombre).lstrip().rstrip().upper() + "', '"
    + str(email) + "', '" 
    + str(password) + "', '"
    + str(id_tipo_usuario) + "', '"
    + str(id_despacho) + "', '"
    + str(creado) + "')"
    db_connect(sql)
    
    return jsonify({'status' : 200})


@bp.route('/logotipo', methods=['POST'])
def logotipo():
    id_despacho = request.get_json()['id_despacho']
    cur, __ = db_connect("select imagen from despachos WHERE id = " + str(id_despacho))
    rv = cur.fetchone()
    return jsonify(rv["imagen"])


@bp.route('/desapachos', methods=['GET'])
def despachos():
    cur, __ = db_connect("select * from despachos")
    rv = cur.fetchall()
    return jsonify(rv)


@bp.route('/altaDespacho', methods=['POST'])
def altaDespacho():
    nombreDespacho = request.get_json()['nombreDespacho']
    base64 = request.get_json()['base64']
    
    if validarExpedienteDespachos(nombreDespacho):
        return jsonify({'status' : 400, 'mensaje': 'Esta repetido el registro' })
    
    sql = "INSERT INTO despachos (nombre,imagen) VALUES ('" + str(nombreDespacho).lstrip().rstrip().upper() + "', '" + str(base64) +"')"
    db_connect(sql)
    return jsonify({'status':200})


@bp.route('/eliminarDespacho', methods=['POST'])
def eliminarDespacho():
    id_despacho = request.get_json()['id_despacho']
    
    sql = "DELETE FROM despachos where id = " + str(id_despacho)
    __, response = db_connect(sql)
    
    if response > 0:
        result = {'message': 'record delete'}
    else:
        result = {'message': 'no record found'}
    
    return jsonify({
        'status': 200, 'result': result
        })


@bp.route('/actualizarDespacho', methods=['POST'])
def actualizarDespacho():
    id_despacho = request.get_json()['id_despacho']
    nombreDespacho = request.get_json()['nombreDespacho']
    base64 = request.get_json()['base64']
    originalNombre = request.get_json()['originalNombre']
    if originalNombre == False:
        if validarExpedienteDespachos(nombreDespacho):
            return jsonify({'status' : 400, 'mensaje': 'Esta repetido el registro' })
        else:
            sql = "UPDATE despachos SET "
            sql += "nombre = '" + str(nombreDespacho).lstrip().rstrip().upper() + "', " 
            sql += "imagen = '" + str(base64) + "'"
            sql += " WHERE id = " + str(id_despacho)
            db_connect(sql)
            return jsonify({
                'status': 200
                })
    else:
        sql = "UPDATE despachos SET "
        sql += "nombre = '" + str(nombreDespacho).lstrip().rstrip().upper() + "', " 
        sql += "imagen = '" + str(base64) + "'"
        sql += " WHERE id = " + str(id_despacho)
        db_connect(sql)
        return jsonify({
                'status': 200
                })

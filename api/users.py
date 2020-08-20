from datetime import datetime
from flask import (
    Blueprint, request, jsonify
)
# DB
from .db import db_connect

# JWT & BCRYPT
from .utils.auth import init_auth
jwt, bcrypt = init_auth()

bp = Blueprint(
    "users", __name__,
    url_prefix='/users')

# CORS
from flask_cors import CORS
CORS(bp)

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

# LOGIN
@bp.route('/login', methods=['POST'])
def login():
    # qs
    email = request.get_json()['email']
    password = request.get_json()['password']
    
    # sql
    sql = "SELECT * FROM usuarios where email = '" + str(email) + "'"
    cur, __ = db_connect(sql)
    rv = cur.fetchone()

	# PASS
    if bcrypt.check_password_hash(rv['password'], password):
        access_token = jwt._create_access_token(
            identity = {
                'apellido_paterno': rv['apellido_paterno'],
                'apellido_materno': rv['apellido_materno'],
                'nombre': rv['nombre'],
                'id': rv['id'],
                'id_tipo_usuario': rv['id_tipo_usuario'],
                'id_despacho': rv['id_despacho']
                })
        return jsonify({
            "access_token": access_token, 
            "user": [{
                "apellido_paterno": rv["apellido_paterno"],
                "apellido_materno": rv["apellido_materno"],
                "nombre": rv["nombre"],
                "id": rv["id"],
                "id_tipo_usuario": rv["id_tipo_usuario"],
                "id_despacho": rv["id_despacho"]
                }]
            })
    else:
        return jsonify({
            "error":"Invalid username and password"
            })

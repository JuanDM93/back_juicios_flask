from datetime import datetime
from flask import (
    Blueprint, request, jsonify
)
# DB
from api.utils.db import db_connect
# JWT & BCRYPT
from .utils.auth import jwt, bcrypt


bp = Blueprint(
    "users", __name__,
    url_prefix='/users')


@bp.route('/login', methods=['POST'])
def login():
    # LOGIN
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
    return jsonify({
        "error": "Invalid username and password"
        })

from datetime import datetime
from flask import (
    Blueprint, request, jsonify
)
# Helpers
from api.utils.db import db_connect
from api.utils.auth import bcrypt
from api.utils.mail.service import sendMulti
import api.utils.route_helpers.users as rh


bp = Blueprint(
    "admin", __name__,
    url_prefix='/admin')


@bp.route('/register', methods=['POST'])
def register():
    # REGISTER
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
    if rh.validarUsuario(email):
        return jsonify({
            'status': 400, 'mensaje': 'Esta repetido el registro'})
    sql = "INSERT INTO usuarios ("
    sql += "apellido_paterno, apellido_materno, nombre, email, password, "
    sql += "id_tipo_usuario, id_despacho, creado"
    sql += ") VALUES ('"
    sql += str(apellido_paterno).lstrip().rstrip().upper() + "', '"
    sql += str(apellido_materno).lstrip().rstrip().upper() + "', '"
    sql += str(nombre).lstrip().rstrip().upper() + "', '"
    sql += str(email) + "', '"
    sql += str(password) + "', '"
    sql += str(id_tipo_usuario) + "', '"
    sql += str(id_despacho) + "', '"
    sql += str(creado) + "')"
    db_connect(sql)

    data = rh.informacionActualizacionOregristroUsuario(email)
    data['tipo'] = 'a_u'
    data['password'] = request.get_json()['password']
    data['emails'] = [email]
    sendMulti(data)
    return jsonify({'status': 200})


@bp.route('/informacionperfil', methods=['POST'])
def informacionperfil():
    id_usuario = request.get_json()['id_usuario']
    sql = "select  id as id_usuario, apellido_paterno, "
    sql += "apellido_materno, nombre, "
    sql += "email, id_tipo_usuario, id_despacho from  usuarios WHERE id = "
    sql += str(id_usuario)
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    return rv


@bp.route('/listausuarios', methods=['POST'])
def listausuarios():
    superroot = request.get_json()['superroot']
    id_despacho = request.get_json()['id_despacho']
    where = ""
    if superroot is False:
        where = "WHERE usuarios.id_despacho = "
        where += str(id_despacho) + " AND NOT tipo_de_usuario.id = 1"
    sql = "SELECT  usuarios.id as id_usuario, usuarios.apellido_paterno, "
    sql += "usuarios.apellido_materno, "
    sql += "usuarios.nombre, usuarios.email, usuarios.id_tipo_usuario, "
    sql += "tipo_de_usuario.nombre as nombre_tipo_usuario, "
    sql += "usuarios.id_despacho,"
    sql += "despachos.nombre as nombre_despacho from usuarios "
    sql += "INNER JOIN despachos on despachos.id = usuarios.id_despacho "
    sql += " INNER JOIN tipo_de_usuario on "
    sql += "tipo_de_usuario.id = usuarios.id_tipo_usuario "
    sql += where
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    return jsonify(rv)


@bp.route('/eliminarUsuario', methods=['POST'])
def eliminarUsuario():
    # eliminarUsuario
    id_usuario = request.get_json()['id_usuario']
    email = request.get_json()['email']
    data = rh.informacionActualizacionOregristroUsuario(email)

    sql = "DELETE FROM usuarios where id = " + str(id_usuario)
    __, response = db_connect(sql)

    if response > 0:
        result = {'message': 'record deleted'}
        data['tipo'] = 'u_d'
        data['emails'] = [email]
        sendMulti(data)
    else:
        result = {'message': 'record not found'}

    return jsonify({
        'status': 200, 'result': result
        })


@bp.route('/actualizarUsuario', methods=['POST'])
def actualizarUsuario():
    id_usuario = request.get_json()['id_usuario']
    apellido_paterno = request.get_json()['apellido_paterno']
    apellido_materno = request.get_json()['apellido_materno']
    nombre = request.get_json()['nombre']
    email = request.get_json()['email']
    newPwd = request.get_json()['newPwd']
    if newPwd is True:
        password = bcrypt.generate_password_hash(
            request.get_json()['password']).decode('utf-8')
    id_tipo_usuario = request.get_json()['id_tipo_usuario']
    id_despacho = request.get_json()['id_despacho']
    # creado = datetime.utcnow()

    originalemail = request.get_json()['originalemail']

    if originalemail is False:
        if rh.validarUsuario(email):
            return jsonify({
                'status': 400, 'mensaje': 'Esta repetido el registro'})

        sql = "UPDATE usuarios SET "
        sql += " apellido_paterno = '"
        sql += str(apellido_paterno).lstrip().rstrip().upper() + "', "
        sql += " apellido_materno = '"
        sql += str(apellido_materno).lstrip().rstrip().upper() + "', "
        sql += " nombre = '" + str(nombre).lstrip().rstrip().upper() + "', "
        sql += " email = '" + str(email) + "', "
        if newPwd is True:
            sql += " password = '" + str(password) + "', "
        sql += " id_tipo_usuario = " + str(id_tipo_usuario) + ", "
        sql += " id_despacho = " + str(id_despacho)
        sql += " WHERE id = " + str(id_usuario)
        db_connect(sql)

        data = rh.informacionActualizacionOregristroUsuario(email)
        data['tipo'] = 'u_u'
        data['newPwd'] = newPwd
        if newPwd is True:
            data['password'] = request.get_json()['password']
        data['emails'] = [email]
        sendMulti(data)

        return jsonify({'status': 200})

    sql = "UPDATE usuarios SET "
    sql += " apellido_paterno = '"
    sql += str(apellido_paterno).lstrip().rstrip().upper() + "', "
    sql += " apellido_materno = '"
    sql += str(apellido_materno).lstrip().rstrip().upper() + "', "
    sql += " nombre = '" + str(nombre).lstrip().rstrip().upper() + "', "
    sql += " email = '" + str(email) + "', "
    if newPwd is True:
        sql += " password = '" + str(password) + "', "
    sql += " id_tipo_usuario = " + str(id_tipo_usuario) + ", "
    sql += " id_despacho = " + str(id_despacho)
    sql += " WHERE id = " + str(id_usuario)
    db_connect(sql)

    data = rh.informacionActualizacionOregristroUsuario(email)
    data['tipo'] = 'u_u'
    data['newPwd'] = newPwd
    if newPwd is True:
        data['password'] = request.get_json()['password']
    data['emails'] = [email]
    sendMulti(data)

    return jsonify({'status': 200})


@bp.route('/logotipo', methods=['POST'])
def logotipo():
    id_despacho = request.get_json()['id_despacho']
    sql = "select imagen from despachos WHERE id = " + str(id_despacho)
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    return jsonify(rv["imagen"])


@bp.route('/tipousuario', methods=['GET'])
def dtipousuario():
    sql = "select * from tipo_de_usuario"
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    return jsonify(rv)


@bp.route('/desapachos', methods=['GET'])
def despachos():
    sql = "select * from despachos"
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    return jsonify(rv)


@bp.route('/altaDespacho', methods=['POST'])
def altaDespacho():
    nombreDespacho = request.get_json()['nombreDespacho']
    base64 = request.get_json()['base64']
    status = request.get_json()['status']

    if rh.validarExpedienteDespachos(nombreDespacho):
        return jsonify({
            'status': 400, 'mensaje': 'Esta repetido el registro'})

    sql = "INSERT INTO despachos (nombre,imagen,status) VALUES ('"
    sql += str(nombreDespacho).lstrip().rstrip().upper()
    sql += "', '" + str(base64) + "', "
    sql += "'" + str(status) + "' "
    sql += ")"
    db_connect(sql)
    return jsonify({'status': 200})


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
    status = request.get_json()['status']
    if originalNombre is False:
        if rh.validarExpedienteDespachos(nombreDespacho):
            return jsonify({
                'status': 400, 'mensaje': 'Esta repetido el registro'})

        sql = "UPDATE despachos SET "
        sql += "nombre = '" + str(nombreDespacho).lstrip().rstrip().upper()
        sql += "', " + "imagen = '" + str(base64) + "'"
        sql += ", " + "status = '" + str(status) + "'"
        sql += " WHERE id = " + str(id_despacho)
        db_connect(sql)
        return jsonify({'status': 200})

    sql = "UPDATE despachos SET "
    sql += "nombre = '" + str(nombreDespacho).lstrip().rstrip().upper() + "', "
    sql += "imagen = '" + str(base64) + "'"
    sql += ", " + "status = '" + str(status) + "'"
    sql += " WHERE id = " + str(id_despacho)
    db_connect(sql)
    return jsonify({'status': 200})


@bp.route('/filtroUsuarios', methods=['POST'])
def filtroUsuarios():

    id_despacho = request.get_json()['id_despacho']
    where = "WHERE usuarios.id_despacho = "
    where += str(id_despacho)
    sql = "SELECT  usuarios.id as id_usuario, usuarios.apellido_paterno, "
    sql += "usuarios.apellido_materno, "
    sql += "usuarios.nombre, usuarios.email, usuarios.id_tipo_usuario, "
    sql += "tipo_de_usuario.nombre as nombre_tipo_usuario, "
    sql += "usuarios.id_despacho,"
    sql += "despachos.nombre as nombre_despacho from usuarios "
    sql += "INNER JOIN despachos on despachos.id = usuarios.id_despacho "
    sql += " INNER JOIN tipo_de_usuario on "
    sql += "tipo_de_usuario.id = usuarios.id_tipo_usuario "
    sql += where
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    return jsonify(rv)

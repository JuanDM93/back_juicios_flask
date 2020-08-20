from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'juicios'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_SECRET_KEY']  = environ.get('JWT_SECRET_KEY')

mysql = MySQL(app)
bcrypt = Bcrypt(app)
jwt  = JWTManager(app)
CORS(app)

def hello_job():
    app.logger.info('Hello Job! The time is: %s' % datetime.now())
    scheduler = BackgroundScheduler()
    # in your case you could change seconds to hours
    scheduler.add_job(hello_job, trigger='interval', hours=24)
    scheduler.start()

@app.route('/users/register', methods=['POST'])
def register():
    cur = mysql.connection.cursor()
    apellido_paterno = request.get_json()['apellido_paterno']
    apellido_materno = request.get_json()['apellido_materno']
    nombre = request.get_json()['nombre']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    id_tipo_usuario = request.get_json()['id_tipo_usuario']
    id_despacho = request.get_json()['id_despacho']
    creado = datetime.utcnow()
    cur.execute("INSERT INTO usuarios ("+
    "apellido_paterno, apellido_materno, nombre, email, password, id_tipo_usuario, id_despacho, creado"+
    ") VALUES ('" + 
		str(apellido_paterno).lstrip().rstrip().upper() + "', '" + 
		str(apellido_materno).lstrip().rstrip().upper() + "', '" + 
		str(nombre).lstrip().rstrip().upper() + "', '" + 
		str(email) + "', '" + 
		str(password) + "', '" + 
		str(id_tipo_usuario) + "', '" + 
		str(id_despacho) + "', '" + 
		str(creado) + "')")
    mysql.connection.commit()
    
    return jsonify({'status' : 200})

@app.route('/users/login', methods=['POST'])
def login():
    cur = mysql.connection.cursor()
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""
    cur.execute("SELECT * FROM usuarios where email = '" + str(email) + "'")
    rv = cur.fetchone()
	
    if bcrypt.check_password_hash(rv['password'], password):
        access_token = create_access_token(identity = {'apellido_paterno': rv['apellido_paterno'],
        'apellido_materno': rv['apellido_materno'],'nombre': rv['nombre'],
        'id': rv['id'],'id_tipo_usuario': rv['id_tipo_usuario'],'id_despacho': rv['id_despacho']
        })
        result = jsonify({
            "access_token":access_token, 
            "user": [{"apellido_paterno": rv["apellido_paterno"],
            "apellido_materno": rv["apellido_materno"],
            "nombre": rv["nombre"],
            "id": rv["id"],
            "id_tipo_usuario": rv["id_tipo_usuario"],
            "id_despacho": rv["id_despacho"]
        }]})
    else:
        result = jsonify({"error":"Invalid username and password"})
    
    return result

@app.route('/juzgados_locales', methods=['GET'])
def juzgados_locales():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from juzgados_locales")
    rv = cur.fetchall()
    return jsonify(rv)

#elimar abogados reponsables
def eliminarCorreosAbogadosLocales(id_juicio_local, listaCorreoAbogadosLocalesElimar):
    data = "("
    finalFor = 0
    tamanofor = len(listaCorreoAbogadosLocalesElimar) - 1
    for CorreoAbogadoLocal in listaCorreoAbogadosLocalesElimar:
        if finalFor < tamanofor:
            data += "'" + CorreoAbogadoLocal + "', "
        else:
            data += "'" + CorreoAbogadoLocal
        finalFor += 1
    data += "')"
    cur = mysql.connection.cursor()
    cur.execute("DELETE from abogados_responsables_juicios_locales WHERE email IN " 
                + data +
                " AND id_juicio_local = " + str(id_juicio_local) 
                )
    mysql.connection.commit()

##metodo para asignar abogados responsables
def registrarCorreosAbogadosLocales(numero_de_expediente, id_juzgado_local, listaCorreoAbogadosLocales):
    data = ""
    finalFor = 0
    tamanofor = len(listaCorreoAbogadosLocales) - 1 
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM juicios_locales WHERE numero_de_expediente = '" + str(numero_de_expediente) 
                + "' AND id_juzgado_local = " + str(id_juzgado_local))
    rv = cur.fetchone()
    
    id_juicio_local = rv["id"]
    
    for CorreoAbogadoLocal in listaCorreoAbogadosLocales:
        if finalFor < tamanofor:
            data += "('" + str(id_juicio_local) +"', '" + CorreoAbogadoLocal + "'), "
        else:
            data += "('" + str(id_juicio_local) +"', '"+ CorreoAbogadoLocal + "')"
        finalFor += 1
    sql = "INSERT INTO abogados_responsables_juicios_locales (id_juicio_local, email) VALUES" + data
    app.logger.info(sql)
    cur = mysql.connection.cursor()
    cur.execute(sql)
    mysql.connection.commit()

#ruta de alta juicio local
@app.route('/alta_juicio_local', methods=['POST'])
def alta_juicio_local():
    actor = request.get_json()['actor']
    demandado = request.get_json()['demandado']
    numero_de_expediente = request.get_json()['numero_de_expediente']
    id_juzgado_local = request.get_json()['id_juzgado_local']
    emails = request.get_json()['emails']
    if validarExpedienteJuiciosLocales(numero_de_expediente, id_juzgado_local) == True:
        return jsonify({'status' : 400, 'mensaje': 'Esta repetido el registro' })
    else:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO juicios_locales " +  "(actor, demandado, numero_de_expediente, id_juzgado_local) VALUES ('" + 
                    str(actor).lstrip().rstrip().upper() + "', '" + 
                    str(demandado).lstrip().rstrip().upper() + "', '" + 
                    str(numero_de_expediente) + "', '" + 
                    str(id_juzgado_local) + "')"   )
        mysql.connection.commit()    
        registrarCorreosAbogadosLocales(numero_de_expediente, id_juzgado_local, emails)
        return jsonify({'status' : 200})

def correosLigadosJuiciosLocales(id_juicio_local):
    cur = mysql.connection.cursor()
    cur.execute("SELECT " +
                "email " +
                "FROM abogados_responsables_juicios_locales " +
                "WHERE id_juicio_local  = " + str(id_juicio_local) 
                )
    rv = cur.fetchall()
    return rv

#obtener los juicios locales la informacion
@app.route('/juicios_locales', methods=['POST'])
def juicios_locales():
    cur = mysql.connection.cursor()
    id_despacho = request.get_json()['id_despacho']
    cur.execute(""+
                "SELECT " +
                "juzgados_locales.nombre as nombre_juzgado_local, "+
                "juicios_locales.id_juzgado_local,  "+
                "juicios_locales.actor,  "+
                "juicios_locales.demandado,  "+
                "juicios_locales.numero_de_expediente,  "+
                "abogados_responsables_juicios_locales.id_juicio_local,  "+
                "abogados_responsables_juicios_locales.email,  "+
                "usuarios.id_despacho  "+
                "FROM abogados_responsables_juicios_locales "+
                "LEFT JOIN usuarios ON usuarios.email = abogados_responsables_juicios_locales.email  "+
                "INNER JOIN juicios_locales on juicios_locales.id = abogados_responsables_juicios_locales.id_juicio_local "+
                "INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local "+
                "WHERE usuarios.id_despacho  =  "+str(id_despacho) +" "+
                "GROUP BY  abogados_responsables_juicios_locales.id_juicio_local "+
                "ORDER BY juicios_locales.id_juzgado_local, juicios_locales.numero_de_expediente DESC;"
                +""
                )
     
    rv = cur.fetchall()
    
    for r in rv:
        r["emails"] = correosLigadosJuiciosLocales(r["id_juicio_local"])
    return jsonify(rv)
    
@app.route('/eliminar_juicio_local', methods=['POST'])
def eliminar_juicio_local():
    
    id_juicio_local = request.get_json()['id_juicio_local']
    emails = request.get_json()['emails']
    
    cur = mysql.connection.cursor()
    response = cur.execute("DELETE FROM juicios_locales where id = " + str(id_juicio_local))
    mysql.connection.commit()
    
    if response > 0:
            result = {'message': 'record delete'}
    else:
        result = {'message': 'no record found'}
    
    eliminarCorreosAbogadosLocales(id_juicio_local, emails)
    return jsonify({'status': 200, 'result': result})

def metodo_actualizar_juicio(actor,demandado,numero_de_expediente,id_juzgado_local,emails,emailsEliminar,id_juicio_local):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE juicios_locales SET "+
                 "actor = '" + str(actor) + "', " +
                 "demandado = '" + str(demandado) + "', " +
                 "numero_de_expediente = '" + str(numero_de_expediente) + "', " +
                 "id_juzgado_local = '" + str(id_juzgado_local) + "' " +
                 " WHERE id = " +
                 str(id_juicio_local))
    mysql.connection.commit()
    eliminarCorreosAbogadosLocales(id_juicio_local, emailsEliminar)
    registrarCorreosAbogadosLocales(numero_de_expediente, id_juzgado_local, emails)

@app.route('/actualizar_juicio_local', methods=['POST'])
def actualizar_juicio_local():
    orginalNumeroExpediente = request.get_json()['orginalNumeroExpediente']
    orginalJuzgado = request.get_json()['orginalJuzgado']
    actor = request.get_json()['actor']
    demandado = request.get_json()['demandado']
    numero_de_expediente = request.get_json()['numero_de_expediente']
    id_juzgado_local = request.get_json()['id_juzgado_local']
    emails = request.get_json()['emails']
    emailsEliminar = request.get_json()['emailsEliminar']
    id_juicio_local = request.get_json()['id_juicio_local']
    if orginalNumeroExpediente == False:
        if validarExpedienteJuiciosLocales(numero_de_expediente, id_juzgado_local) == True:
            return jsonify({'status' : 400, 'mensaje': 'Esta repetido el registro' })
        else:
            metodo_actualizar_juicio(actor,demandado,numero_de_expediente,id_juzgado_local,emails,emailsEliminar,id_juicio_local)
            return jsonify({'status': 200})
    else:
        if orginalJuzgado == True:
            metodo_actualizar_juicio(actor,demandado,numero_de_expediente,id_juzgado_local,emails,emailsEliminar,id_juicio_local)
            return jsonify({'status': 200})
        else:
            if validarExpedienteJuiciosLocales(numero_de_expediente, id_juzgado_local) == True:
                return jsonify({'status' : 400, 'mensaje': 'Esta repetido el registro' })
            else:
                metodo_actualizar_juicio(actor,demandado,numero_de_expediente,id_juzgado_local,emails,emailsEliminar,id_juicio_local)
                return jsonify({'status': 200})
            
@app.route('/filtro_juicios_locales', methods=['POST'])
def filtro_juicios_locales():
    cur = mysql.connection.cursor()
    id_despacho = request.get_json()['id_despacho']
    id_juzgado_local = request.get_json()['id_juzgado_local']
    numero_de_expediente = request.get_json()['numero_de_expediente'] 
    Where = "";
    if len(numero_de_expediente) > 0 and str(numero_de_expediente).isspace() == False:
        Where += " AND juicios_locales.numero_de_expediente like '%"+ str(numero_de_expediente) +"%' "
  
    if id_juzgado_local > 0:
        Where += " AND juicios_locales.id_juzgado_local = '"+ str(id_juzgado_local) +"' "
                    
    cur.execute(""+
                "SELECT " +
                "juzgados_locales.nombre as nombre_juzgado_local, "+
                "juicios_locales.id_juzgado_local,  "+
                "juicios_locales.actor,  "+
                "juicios_locales.demandado,  "+
                "juicios_locales.numero_de_expediente,  "+
                "abogados_responsables_juicios_locales.id_juicio_local,  "+
                "abogados_responsables_juicios_locales.email,  "+
                "usuarios.id_despacho  "+
                "FROM abogados_responsables_juicios_locales "+
                "LEFT JOIN usuarios ON usuarios.email = abogados_responsables_juicios_locales.email  "+
                "INNER JOIN juicios_locales on juicios_locales.id = abogados_responsables_juicios_locales.id_juicio_local "+
                "INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local "+
                "WHERE usuarios.id_despacho  =  "+ str(id_despacho) +" "+ Where +
                "GROUP BY  abogados_responsables_juicios_locales.id_juicio_local "+
                "ORDER BY juicios_locales.id_juzgado_local, juicios_locales.numero_de_expediente DESC;"
                +""
                )
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = correosLigadosJuiciosLocales(r["id_juicio_local"])
    return jsonify(rv)

def validarExpedienteJuiciosLocales(numero_de_expediente, id_juzgado_local):
    cur = mysql.connection.cursor()    
    sql = "SELECT COUNT(1) AS BIT FROM juicios_locales WHERE numero_de_expediente = '" + str(numero_de_expediente) + "' AND id_juzgado_local = " + str(id_juzgado_local)
    app.logger.info(sql) 
    cur.execute(sql)
    rv = cur.fetchone()
    if rv["BIT"] == 0 :
        return False
    else:
        return True
    
@app.route('/juicios_locales_asignados', methods=['POST'])
def juicios_locales_asignados():
    cur = mysql.connection.cursor()
    id_usuario = request.get_json()['id_usuario']
    cur.execute(""+
                "SELECT " +
                "juzgados_locales.nombre as nombre_juzgado_local, "+
                "juicios_locales.id_juzgado_local,  "+
                "juicios_locales.actor,  "+
                "juicios_locales.demandado,  "+
                "juicios_locales.numero_de_expediente,  "+
                "abogados_responsables_juicios_locales.id_juicio_local,  "+
                "abogados_responsables_juicios_locales.email,  "+
                "usuarios.id_despacho  "+
                "FROM abogados_responsables_juicios_locales "+
                "LEFT JOIN usuarios ON usuarios.email = abogados_responsables_juicios_locales.email  "+
                "INNER JOIN juicios_locales on juicios_locales.id = abogados_responsables_juicios_locales.id_juicio_local "+
                "INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local "+
                "WHERE usuarios.id  =  "+ str(id_usuario) +" "+
                "GROUP BY  abogados_responsables_juicios_locales.id_juicio_local "+
                "ORDER BY juicios_locales.id_juzgado_local, juicios_locales.numero_de_expediente DESC;"
                +""
                )
     
    rv = cur.fetchall()
    
    for r in rv:
        r["emails"] = correosLigadosJuiciosLocales(r["id_juicio_local"])
    return jsonify(rv)

#ruta de validacion para pruebas
@app.route('/validate', methods=['POST'])
def validate():
    cur = mysql.connection.cursor()
    email = request.get_json()['email']
    cur.execute("SELECT COUNT(1) AS BIT FROM juicios.usuarios WHERE juicios.usuarios.email = '" + str(email) + "'")
    rv = cur.fetchone()
    if rv["BIT"] == 0 :
        app.logger.info("no existe")
    else:
        app.logger.info("existe")
        cur.execute("SELECT * FROM usuarios where email = '" + str(email) + "'")
        rv = cur.fetchone()
        app.logger.info(rv["id"])
    return jsonify(rv)

if __name__ == '__main__':
    app.run(debug=True)

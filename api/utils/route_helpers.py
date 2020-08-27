from api.db import db_connect
from datetime import date, datetime, timedelta 

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
    numero_de_expediente, id_juzgado_local,
    listaCorreoAbogadosLocales):
    sql = "SELECT id FROM juicios_locales WHERE numero_de_expediente = '"
    sql += str(numero_de_expediente) 
    sql += "' AND id_juzgado_local = " + str(id_juzgado_local)
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    id_juicio_local = rv["id"]
    
    data = ""
    for CorreoAbogadoLocal in listaCorreoAbogadosLocales:
        data += "('" + str(id_juicio_local) +"', '" + CorreoAbogadoLocal + "'), "
        #TODO
        # enviarCorreo(correoabogadolocal, 'texto formateado'--data['nombre'])
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
    emails, emailsEliminar, id_juicio_local):

    sql = "UPDATE juicios_locales SET "
    sql += "actor = '" + str(actor).lstrip().rstrip().upper() + "', " 
    sql += "demandado = '" + str(demandado).lstrip().rstrip().upper() + "', "
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
    return True
    

# Validar expediente
def validarExpedienteDespachos(nombre_despacho):
    sql = "SELECT COUNT(1) AS BIT FROM despachos "
    sql += "WHERE nombre = '" + str(nombre_despacho).lstrip().rstrip().upper()
    sql += "'"
    cur, __ = db_connect(sql) 
    rv = cur.fetchone()
    if rv["BIT"] == 0 :
        return False
    return True

# Validar usuario
def validarUsuario(email):
    sql = "SELECT COUNT(1) AS BIT FROM usuarios "
    sql += "WHERE email = '" + str(email).lstrip().rstrip().upper()
    sql += "'"
    cur, __ = db_connect(sql) 
    rv = cur.fetchone()
    if rv["BIT"] == 0 :
        return False
    return True


#data actualizacion o insercion 
def dataActualizacionOinsercion(id_juzgado_local, numero_de_expediente):
    sql = "select juicios_locales.id as id_juicio_local, juzgados_locales.nombre as juzgado ,juicios_locales.numero_de_expediente as expediente"
    sql += " from juicios_locales INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local "
    sql += "WHERE juicios_locales.id_juzgado_local = "+ str(id_juzgado_local)+ " and  juicios_locales.numero_de_expediente = '"
    sql += str(numero_de_expediente) +"'"
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    return rv

#eliminar acuerdos locales
def eliminarAcuerdosLocales(id_juicio_local):
    sql = "DELETE FROM acuerdos_locales where id_juicio_local = " + str(id_juicio_local)
    __, response = db_connect(sql)


#en lazar acuerdos historicos
def acuerdosHistoricos(id_juicio_local):
    fechasql = datetime.strftime(datetime.now() - timedelta(days=1), '%Y-%m-%d')
    yearsql = datetime.strftime(datetime.now() - timedelta(days=365), '%Y')
    sql = "SELECT acuerdos_locales.fecha, acuerdos_locales.descripcion"
    sql += " FROM acuerdos_locales where acuerdos_locales.id_juicio_local = "+ str(id_juicio_local)+" AND "
    sql += " acuerdos_locales.fecha BETWEEN '"+yearsql+"-01-01' AND '"+ fechasql +"'"
    cur, response = db_connect(sql)
    rv = cur.fetchall()
    return rv 

#acuerdos locales diarios
def acuerdoslocalesdiarios(id_juicio_local):
    fechasql = datetime.strftime(datetime.now() - timedelta(days=1), '%Y-%m-%d')
    sql = "SELECT acuerdos_locales.fecha, acuerdos_locales.descripcion"
    sql += " FROM acuerdos_locales where acuerdos_locales.id_juicio_local = "+ str(id_juicio_local)+" AND "
    sql += " acuerdos_locales.fecha = '"+ fechasql +"'"
    cur, response = db_connect(sql)
    rv = cur.fetchall()
    return rv 
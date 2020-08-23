from api.db import db_connect


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
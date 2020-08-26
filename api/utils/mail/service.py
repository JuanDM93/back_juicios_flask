from flask_mail import Mail, Message

from . import m_help


mail = Mail()


def search_msg(data):
    if data['tipo'] == 'a_j_l':
        return m_help.ms_actual_local(data)

    if data['tipo'] == 'a_j_f':
        return m_help.ms_actual_fed(data)
        
    if data['tipo'] == 'n_j_l':
        return m_help.ms_nuevo_local(data)


def sendMulti(data):
    subject, message = search_msg(data)
    with mail.connect() as conn:
        for user in data['emails']:
            msg = Message(
                recipients=[user],
                subject=subject,
                body=message,
            )
            conn.send(msg)

"""
rv = [
    {
        'fecha': '2020-08-20',
        'acuerdo': ' sdgvsduycs dcfsudcg uisdc uisdv' ,
        'expediente: '379/2020',
        'actor': 'actor',
        'demandado': 'damandado',
        'juzgado' : 'juzgado',
        'id_juicio_local': 1,
        'emails': ['correo@hotmail.com', 'rcchsdcu@hotmail.com']
    },  
    {
        'fecha': '2020-08-20',
        'acuerdo': ' sdgvsduycs dcfsudcg uisdc uisdv' ,
        'expediente: '379/2020',
        'actor': 'actor',
        'demandado': 'damandado',
        'juzgado' : 'juzgado',
        'id_juicio_local': 1,
        'emails': ['correo@hotmail.com', 'rcchsdcu@hotmail.com']
    },  
    {
        'fecha': '2020-08-20',
        'acuerdo': ' sdgvsduycs dcfsudcg uisdc uisdv' ,
        'expediente: '379/2020',
        'actor': 'actor',
        'demandado': 'damandado',
        'juzgado' : 'juzgado',
        'id_juicio_local': 1,
        'emails': ['correo@hotmail.com', 'rcchsdcu@hotmail.com']
    },  
]
"""
# este metodo esta en route_helpers
from ..route_helpers import correosLigadosJuiciosLocales
def sqlenviarcorreo(data):
    fechasql = datetime.strftime(datetime.now() - timedelta(days=1), '%Y-%m-%d')
    yearsql = datetime.strftime(datetime.now(), '%Y')
    sql =""
    if(len(data)>1):
        sql += " select juicios_locales.id as id_juicio_local, acuerdos_locales.fecha, acuerdos_locales.descripcion as acuerdo, juicios_locales.numero_de_expediente as expediente,"
        sql += "juicios_locales.actor, juicios_locales.demandado, juzgados_locales.nombre as juzgado FROM acuerdos_locales "
        sql += "INNER JOIN juicios_locales ON juicios_locales.id = acuerdos_locales.id_juicio_local "
        sql += "INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local "
        sql += "WHERE  acuerdos_locales.fecha = '"+fechasql+"'" 
        cur, __ = db_connect(sql)
        rv = cur.fetchall()
        for r in rv:
            # este metodo esta en route_helpers
            r["emails"] = correosLigadosJuiciosLocales(r["id_juicio_local"])
        return rv
    else:
        sql += " select juicios_locales.id as id_juicio_local, acuerdos_locales.fecha, acuerdos_locales.descripcion as acuerdo, juicios_locales.numero_de_expediente as expediente,"
        sql += "juicios_locales.actor, juicios_locales.demandado, juzgados_locales.nombre as juzgado FROM acuerdos_locales "
        sql += "INNER JOIN juicios_locales ON juicios_locales.id = acuerdos_locales.id_juicio_local "
        sql += "INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local "
        sql += "WHERE juicios_locales.numero_de_expediente = '" +str(data[0]["expediente"]) + "' AND  juicios_locales.id_juzgado_local = " +str(data[0]["id_juzgado_local"]) +  "AND "
        sql += "acuerdos_locales.fecha BETWEEN '"+fechasql+"' AND '"+yearsql+"-01-01'"
        cur, __ = db_connect(sql)
        rv = cur.fetchone()
        # este metodo esta en route_helpers
        rv["emails"] = correosLigadosJuiciosLocales(rv["id_juicio_local"])
        return [rv]
        

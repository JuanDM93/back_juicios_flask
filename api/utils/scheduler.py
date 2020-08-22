from flask_apscheduler import APScheduler

# SCHEDULER
scheduler = APScheduler()

def start_jobs(app):
    scheduler.init_app(app)
    scheduler.start()

# interval examples
@scheduler.task(
    'interval', id='do_job_1',
    seconds=30, misfire_grace_time=900)
def job1():
    print('Job 1 executed')

# cron examples
@scheduler.task(
    'cron', id='do_job_2',
    minute='*')
def job2():
    print('Job 2 executed')

# dayly pdf
from api.utils.pdf.parse import fetch_day
from datetime import datetime, timedelta
@scheduler.task(
    'cron', id='daylyPDF',
    week='*',
    )


def daylyPDF():
    
    sql = "SELECT juicios_locales.id as id_juicio_local, juzgados_locales.nombre as juzgado, "
    sql += "juicios_locales.numero_de_expediente as expediente FROM juicios_locales "
    sql += "INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local"
    hoy = datetime.now().date()
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    fetch_day(hoy, data)
    print('daylyPDF')
    
    
    
    
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
            ##este metodo esta en b_locals
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
        ##este metodo esta en b_locals
        rv["emails"] = correosLigadosJuiciosLocales(rv["id_juicio_local"])
        return [rv]
        

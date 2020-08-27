from flask_apscheduler import APScheduler

# SCHEDULER
scheduler = APScheduler()


def start_jobs(app):
    scheduler.init_app(app)
    scheduler.start()
#-------------------
# interval example
@scheduler.task(
    'interval', id='do_job_1',
    seconds=30,)
def job1():
    #logger
    with scheduler.app.app_context():
        scheduler.app.logger.debug('Do Job Scheduler 30')

# Mail test
from .mail.service import sendMulti
@scheduler.task(
    'cron', id='mail_tester',
    day='*', hour='*', minute='30')
def mail_tester():
    data = {}
    data['tipo'] = 'a_j_l'
    data['emails'] = ['ricaror@hotmail.com']
    data['numero_de_expediente'] = '1/2020'
    data['actor'] = 'ACTOR'
    data['demandado'] = 'DEMANDADO'

    with scheduler.app.app_context():
        sendMulti(data)
        scheduler.app.logger.debug('Mail job executed')

# dayly pdf
from datetime import datetime
from api.utils.pdf.fetch import fetch_day
@scheduler.task(
    'cron', id='daylyPDF',
    day='*', hour='7')
def daylyPDF():
    sql = "SELECT juicios_locales.id as id_juicio_local, juzgados_locales.nombre as juzgado, "
    sql += "juicios_locales.numero_de_expediente as expediente FROM juicios_locales "
    sql += "INNER JOIN juzgados_locales on juzgados_locales.id = juicios_locales.id_juzgado_local"
    #cur, __ = db_connect(sql)
    #rv = cur.fetchall()
    
    #data = [rv['']]
    
    hoy = datetime.now().date()
    #fetch_day(hoy, data)
    print(f'daylyPDF {hoy}')
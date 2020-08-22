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
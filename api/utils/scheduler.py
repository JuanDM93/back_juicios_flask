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

    sqlactual = ''
    cur, res = db_connect(sqlactual)
    juzgado = cur.fetchone()

    data = []
    
    juzgados = {
        'juzgado': juzgado,
        'expediente': numero_de_expediente}
    hoy = datetime.now().date()
    fetch_day(hoy, data)
    print('daylyPDF')

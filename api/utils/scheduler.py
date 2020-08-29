from flask_apscheduler import APScheduler

from api.utils.db import db_connect
from api.utils.mail.service import sendMulti
from api.utils.pdf.fetch import pdf_service


scheduler = APScheduler()


def start_jobs(app):
    scheduler.init_app(app)
    scheduler.start()


@scheduler.task(
    'interval', id='do_job_1',
    seconds=30,)
def job1():
    # interval example
    with scheduler.app.app_context():
        scheduler.app.logger.debug('Do Job Scheduler 30')


@scheduler.task(
    'cron', id='mail_tester',
    day='*', hour='*', minute='30')
def mail_tester():
    # Mail test
    data = {}
    data['tipo'] = 'a_j_l'
    data['emails'] = ['ricaror@hotmail.com']
    data['numero_de_expediente'] = '1/2020'
    data['actor'] = 'ACTOR'
    data['demandado'] = 'DEMANDADO'

    with scheduler.app.app_context():
        sendMulti(data)
        scheduler.app.logger.debug('Mail job executed')


@scheduler.task(
    'cron', id='dailyPDF',
    day='*', hour='*', minute=30)
def dailyPDF():
    # daily pdf
    sql = "SELECT juicios_locales.id as id_juicio_local, "
    sql += "juzgados_locales.nombre as juzgado, "
    sql += "juicios_locales.numero_de_expediente as expediente "
    sql += "FROM juicios_locales "
    sql += "INNER JOIN juzgados_locales on "
    sql += "juzgados_locales.id = juicios_locales.id_juzgado_local"

    cur, __ = db_connect(sql)
    rv = cur.fetchall()

    data = [rv]
    pdf_service(data, daily=True)

    with scheduler.app.app_context():
        scheduler.app.logger.debug('dailyPDF job')

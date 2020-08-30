from flask_apscheduler import APScheduler

from api.utils.db import db_connect
from api.utils.mail.service import sendMulti
from api.utils.pdf.fetch import pdf_service


scheduler = APScheduler()


def start_jobs(app):
    scheduler.init_app(app)
    scheduler.start()


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
    'cron', id='daily_federal',
    day='*', hour='*', minute=1)
def daily_federal():
    # daily federal
    sql = ''
    with scheduler.app.app_context():
        """
        cur, __ = db_connect(sql)
        rv = cur.fetchall()

        data = []

        from api.utils.pdf.scrapper import get_federals
        get_federals(data)
        """
        scheduler.app.logger.debug('dailyFederal job')


@scheduler.task(
    'cron', id='daily_local',
    day='*', hour='*', minute='1')
def daily_local():
    # daily_local
    sql = "SELECT juicios_locales.id as id_juicio_local, "
    sql += "juzgados_locales.nombre as juzgado, "
    sql += "juicios_locales.numero_de_expediente as expediente "
    sql += "FROM juicios_locales "
    sql += "INNER JOIN juzgados_locales on "
    sql += "juzgados_locales.id = juicios_locales.id_juzgado_local"

    with scheduler.app.app_context():
        """
        cur, __ = db_connect(sql)
        rv = cur.fetchall()

        data = [rv]
        if data is None:
            pdf_service(data, daily=True)
        """
        scheduler.app.logger.debug('dailyLocal job')

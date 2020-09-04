from flask_apscheduler import APScheduler

from api.utils.db import db_connect
from api.utils.mail.service import sendMulti
from api.utils.pdf.fetch import pdf_service
from api.utils.route_helpers.locals import sqlenviarcorreoDiario
from api.utils.route_helpers.federals import insertarAcuerdosDB


scheduler = APScheduler()


def start_jobs(app):
    scheduler.init_app(app)
    scheduler.start()


@scheduler.task(
    'cron', id='mail_tester',
    day_of_week='*', hour='4', minute='20',
    )
def mail_tester():
    # Mail test
    data = {}
    data['tipo'] = 'a_j_f'
    data['emails'] = ['ricaror@hotmail.com']
    data['numero_de_expediente'] = '1/2020'
    data['actor'] = 'ACTOR'
    data['demandado'] = 'DEMANDADO'

    with scheduler.app.app_context():
        sendMulti(data)
        scheduler.app.logger.debug('Mail job executed')


@scheduler.task(
    'cron', id='daily_federal',
    day_of_week='mon-fri', hour=23,  minute=21,
    )
def daily_federal():
    # daily federal
    sql = "SELECT cir_id, id_org, t_ast, n_exp from juicios_federales"
    with scheduler.app.app_context():
        cur, __ = db_connect(sql)
        rv = cur.fetchall()
        for r in rv:
            r['tipo'] = 'u_j_f'
        insertarAcuerdosDB(rv)

        scheduler.app.logger.debug('dailyFederal job')


@scheduler.task(
    'cron', id='daily_local',
    day_of_week='mon-fri', hour=7,  minute=1,
    )
def daily_local():
    # daily_local
    sql = "SELECT juicios_locales.id as id_juicio_local, "
    sql += "juzgados_locales.nombre as juzgado, "
    sql += "juicios_locales.numero_de_expediente as expediente, "
    sql += "juicios_locales.id_juzgado_local "
    sql += "FROM juicios_locales "
    sql += "INNER JOIN juzgados_locales on "
    sql += "juzgados_locales.id = juicios_locales.id_juzgado_local"

    with scheduler.app.app_context():
        cur, __ = db_connect(sql)
        rv = cur.fetchall()

        if rv is not None:
            pdf_service(rv, daily=True)
            for dataMail in sqlenviarcorreoDiario():
                dataMail['tipo'] = 'u_j_l'
                sendMulti(dataMail)

        scheduler.app.logger.debug('dailyLocal job')

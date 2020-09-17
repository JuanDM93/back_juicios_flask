import requests
from datetime import datetime

from api.utils.db import db_connect
from api.utils.pdf.fetch import get_response
from api.utils.route_helpers.locals import validarExpedienteLocal


def extract_acuerdo(pdf, data):
    x = pdf.find(data['juzgado'])
    juzgado = pdf[x:]

    punto = "SECRETARÍA “A”"
    punto_a = juzgado.find(punto)
    juzgado = juzgado[punto_a:]
    y = juzgado[len(punto):].find(punto)

    juzgado = juzgado[punto_a:y]

    acuerdo = "Exp. " + data['expediente']
    y = juzgado.find(acuerdo)
    if y == -1:
        return None

    ac_separa = '\n\n'
    x = juzgado.find(ac_separa)
    acuerdos = juzgado[x:(y+len(acuerdo))]

    result = acuerdos.split(ac_separa)[-1]
    return result


def extract_multi(pdf, data):
    result = []
    for d in data:
        d['acuerdo'] = extract_acuerdo(pdf, d)
        if d['acuerdo'] is not None:
            result.append(d)
    return result


def is_parsed(f_name, data=None):
    # tika
    from tika import parser
    from flask import current_app

    try:
        pdf = parser.from_buffer(
            f_name,
            'http://tika:9998/tika',
            requestOptions={
                'timeout': 60,
            }
        )
    except Exception:
        current_app.logger.warn('TIKA: No response from server')
    try:
        pdf = parser.from_buffer(f_name)
    except Exception:
        current_app.logger.warn('TIKA: No local jar found')
    finally:
        if pdf:
            if pdf['content']:
                return extract_multi(pdf['content'], data)
        return []


def req_cdmx(fecha: str):
    url = 'https://www.poderjudicialcdmx.gob.mx/'
    url += f'wp-content/PHPs/boletin/boletin_repositorio/{fecha}1.pdf'
    with requests.sessions.Session() as s:
        return get_response(s, url)


def fetch_pdf(fecha, data: []):
    fechaurl = datetime.strftime(fecha, '%d%m%Y')
    response = req_cdmx(fechaurl)
    if response is not None:
        result = is_parsed(response, data)
        if len(result) > 0:
            values = ""
            for r in result:
                f_str = fecha
                fecha_sql = datetime.strftime(f_str, '%Y-%m-%d')
                if validarExpedienteLocal(r["acuerdo"]) is False:
                    url = 'https://www.poderjudicialcdmx.gob.mx/'
                    url += f'wp-content/PHPs/boletin/boletin_repositorio/{fechaurl}1.pdf'
                    values += "( '" + fecha_sql + "','" + str(r["acuerdo"]) + "',"
                    values += str(r["id_juicio_local"])+",'" + url +"'),"
            if len(values) > 0:
                values = values[:-1]
                sql = "INSERT INTO "
                sql += "acuerdos_locales (fecha,descripcion,id_juicio_local, pdfboletin) "
                sql += "VALUES " + values
                db_connect(sql)

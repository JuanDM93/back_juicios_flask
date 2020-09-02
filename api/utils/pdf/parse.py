import requests
from time import sleep
from datetime import datetime

from api.utils.db import db_connect
from api.utils.route_helpers import validarExpedienteLocal


def extract_acuerdo(pdf: str, data):
    x = pdf.find(data['juzgado'])
    juzgado = pdf[x:]
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
    pdf = parser.from_buffer(
        f_name,
        'http://tika:9998/tika',
        requestOptions={
            'timeout': 3600,
        },
    )
    pdf = pdf['content']

    # has content
    if len(pdf) > 1:
        return extract_multi(pdf, data)
    return []


def req_cdmx(fecha: str):
    url = 'https://www.poderjudicialcdmx.gob.mx/'
    url += f'wp-content/PHPs/boletin/boletin_repositorio/{fecha}1.pdf'
    with requests.Session() as s:
        response = s.get(url)
        # TODO check other status??? timeouts...
        if response.status_code == 200:
            return response.content
        if response.status_code == 500:
            sleep(1)
            return req_cdmx(fecha)
        return None


def fetch_pdf(fecha, data: []):
    fechaurl = datetime.strftime(fecha, '%d%m%Y')
    response = req_cdmx(fechaurl)
    if response is not None:
        result = is_parsed(response, data)
        # SQL
        if len(result) > 0:
            values = ""
            for r in result:
                f_str = fecha
                fecha_sql = datetime.strftime(f_str, '%Y-%m-%d')
                if validarExpedienteLocal(r["acuerdo"]) is False:
                    values += "( '" + fecha_sql + "','" + str(r["acuerdo"]) + "',"
                    values += str(r["id_juicio_local"]) + "),"
            if len(values) > 0:
                values = values[:-1]
                sql = "INSERT INTO "
                sql += "acuerdos_locales (fecha,descripcion,id_juicio_local) "
                sql += "VALUES " + values
                db_connect(sql)

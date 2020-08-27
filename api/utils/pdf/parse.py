import requests
from time import sleep
from pathlib import Path
from random import randint
from datetime import (datetime, timedelta)

from ...db import db_connect


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


def is_parsed(f_name, data):
    # tika
    from tika import parser
    pdf = parser.from_file(f_name)['content']

    # has content
    if len(pdf) > 1:
        return extract_multi(pdf, data)
    return []


def req_cdmx(fecha: str):
    url = 'https://www.poderjudicialcdmx.gob.mx/'
    url += f'wp-content/PHPs/boletin/boletin_repositorio/{fecha}1.pdf'
    response = requests.get(url)

    if response.status_code == 200:
        return True, response.content
    if response.status_code == 404:
        return False, response
    sleep(1)
    return req_cdmx(fecha)


def fetch_pdf(fecha, data: []):
    fechaurl = datetime.strftime(fecha, '%d%m%Y')

    flag, response = req_cdmx(fechaurl)
    if flag:
        # create pdf
        ran = randint(0, 1000)
        f_name = f'{fechaurl}{ran}.pdf'
        file_pdf = Path(f_name)
        file_pdf.write_bytes(response)

        result = is_parsed(f_name, data)
        # SQL
        if len(result) > 0:
            values = ""
            for r in result:
                f_str = fecha - timedelta(days=1)
                fecha_sql = datetime.strftime(f_str, '%Y-%m-%d')
                values += "( '" + fecha_sql + "','" + str(r["acuerdo"]) + "',"
                values += str(r["id_juicio_local"]) + "),"

            values = values[:-1]
            sql = "INSERT INTO "
            sql += "acuerdos_locales (fecha,descripcion,id_juicio_local) "
            sql += "VALUES " + values
            db_connect(sql)

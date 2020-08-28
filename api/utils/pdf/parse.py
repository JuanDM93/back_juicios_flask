import requests
import tempfile
from time import sleep
from pathlib import Path
from datetime import (datetime, timedelta)

from api.utils.db import db_connect


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


def extract_actuales(pdf: str):
    flag = True
    result = {}
    while flag:
        juzgado_separa = ''
        x = pdf.find(juzgado_separa)
        if x == -1:
            return {}
        y = pdf[x:].find(juzgado_separa)
        juzgado = pdf[x:y]
        # TODO
        acuerdo_id = "Exp. "
        ac_separa = '\n\n'
        x = juzgado.find(ac_separa)
        y = juzgado.find(acuerdo_id)
        juzgado = juzgado[x:y]
        acuerdos = juzgado[x:(y + len(juzgado))]
        acuerdos = acuerdos.split(ac_separa)

    result = {
        'juzgado': 'test',
        'acuerdos': acuerdos,
        }
    return result


def extract_multi(pdf, data):
    result = []
    for d in data:
        d['acuerdo'] = extract_acuerdo(pdf, d)
        if d['acuerdo'] is not None:
            result.append(d)

    return result


def extract_new(pdf):
    result = []
    data = extract_actuales(pdf)
    for d in data:
        result.append(d)

    return result


def is_parsed(f_name, data=None):
    # tika
    from tika import parser
    pdf = parser.from_file(f_name)['content']

    # has content
    if len(pdf) > 1:
        if data is None:
            return extract_new(pdf)
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


def fetch_pdf(fecha, data: [] = []):
    fechaurl = datetime.strftime(fecha, '%d%m%Y')
    flag, response = req_cdmx(fechaurl)
    if flag:
        with tempfile.TemporaryDirectory() as pdf_dir:
            # create pdf
            f_name = f'{fechaurl}.pdf'
            file_pdf = Path(pdf_dir + f_name)
            file_pdf.write_bytes(response)

            if len(data) > 1:
                result = is_parsed(pdf_dir + f_name, data)
        print(len(result))


def fetch_pdf_old(fecha, data: []):
    fechaurl = datetime.strftime(fecha, '%d%m%Y')

    flag, response = req_cdmx(fechaurl)
    if flag:
        with tempfile.TemporaryDirectory() as pdf_dir:
            # create pdf
            f_name = f'{fechaurl}.pdf'
            file_pdf = Path(pdf_dir + f_name)
            file_pdf.write_bytes(response)

            result = is_parsed(pdf_dir + f_name, data)
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

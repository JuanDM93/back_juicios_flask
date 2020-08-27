import requests
from tika import parser
from pathlib import Path
from datetime import date, datetime, timedelta 

from api.db import db_connect


def extract_acuerdo(pdf:str, data):
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
        if d['acuerdo'] != None:
            result.append(d)

    return result


def is_parsed(data, file='metadata.pdf'):
    # tika
    pdf = parser.from_file(file)
 
    # has content
    if len(pdf['content']) > 1:
        return extract_multi(pdf['content'], data)
    return []


from time import sleep
def req_cdmx(fecha:str):    
    url = f'https://www.poderjudicialcdmx.gob.mx/wp-content/PHPs/boletin/boletin_repositorio/{fecha}1.pdf'
    response = requests.get(url)
    
    if response.status_code == 200:
        return False, response.content
    if response.status_code == 404:
        return True, response
    sleep(1)
    return req_cdmx(fecha)


def fetch_pdf(fecha, data:[]):
    fechaurl = datetime.strftime(fecha,'%d%m%Y')

    flag, response = req_cdmx(fechaurl)
    if flag:
        break

    # create pdf
    filename = Path('metadata.pdf')
    filename.write_bytes(response)
    result = is_parsed(data)
    ## SQL
    if len(result) > 0:
        values = ""
        for r in result: 
            fecha_sql = datetime.strftime(fecha - timedelta(days=1), '%Y-%m-%d')
            values += "( '" + fecha_sql + "','" +  str(r["acuerdo"]) + "'," + str(r["id_juicio_local"]) +"),"

        values = values[:-1]
        sql = "INSERT INTO acuerdos_locales (fecha,descripcion,id_juicio_local) VALUES " + values
        db_connect(sql)

import requests
from tika import parser
from pathlib import Path
from datetime import date, datetime, timedelta 

from api.db import db_connect
"""
data = [
    {
        'juz': 'PRIMERO DE LO CIVIL',
        'acuerdos': ['1101/2010'],
    },
    {
        'juz': 'SEGUNDO DE LO CIVIL',
        'acuerdos': ['1101/2010'],
    },
]

data len = 1
data len = 1010010101
"""
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
        d["acuerdo"] = extract_acuerdo(pdf, d)
        if d["acuerdo"] != None:
            result.append(d)
        else:
            return None
    return result


def is_parsed(data, pdf='metadata.pdf'):
    # tika
    pdf = parser.from_file(pdf)
    # has content
    
    if len(pdf['content']) > 1:
        #if len(data) > 1:
        return extract_multi(pdf['content'], data)
        #return extract_acuerdo(pdf['content'], data)
    return None


def fetch_pdf(date, data:[]):
    fechaurl = date.strftime('%d%m%Y')
    ##############
    
    #try con 
    
    url = f'https://www.poderjudicialcdmx.gob.mx/wp-content/PHPs/boletin/boletin_repositorio/{fechaurl}1.pdf'
    # fetch
    response = requests.get(url)
    # create pdf
    
    
    ###################
    filename = Path('metadata.pdf')
    filename.write_bytes(response.content)
    result = is_parsed(data)
    ## SQL
    if result != None:
        values = ""
        for r in result:
            fechasql = datetime.strftime(date - timedelta(days=1), '%Y-%m-%d')
            #fecha - 1
            #yyyy-mm-dd
            #values += "( '" +  datetime.strftime(datetime.strptime(date[2:4] + "-"  + date[0:2] + "-" + date[4:8],'%m-%d-%Y') - timedelta(days=1),  '%Y/%m/%d')+ "','" +  str(r["acuerdo"]) + "'," + str(r["id_juicio_local"]) +"),"
            values += "( '" + fechasql + "','" +  str(r["acuerdo"]) + "'," + str(r["id_juicio_local"]) +"),"
        values = values[:-1]
        sql = "INSERT INTO acuerdos_locales (fecha,descripcion,id_juicio_local) VALUES " + values
        db_connect(sql)
    ###

# public methods
# --------------
def fetch_day(date, data):
    fetch_pdf(date, data)


def fetch_history(data):
    init_date = date(2020, 8, 1)
    now = datetime.now().date()
    while now != init_date:
        fetch_day(now, data)
        now = now - timedelta(days=1)
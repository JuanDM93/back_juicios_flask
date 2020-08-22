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
    acuerdo = data['acuerdos']
    y = juzgado.find(acuerdo)
    if y == -1:
        return None    
    ac_separa = '\n\n'
    x = juzgado.find(ac_separa)
    acuerdos = juzgado[x:(y+len(acuerdo))]
    result = acuerdos.split(ac_separa)[-1]
    return result


def extract_multi(pdf, data):
    result = {}
    for d in data:
        result[d['acuerdo']] = extract_acuerdo(pdf['content'], d)
    return result


def is_parsed(data, pdf='metadata.pdf'}):
    # tika
    pdf = parser.from_file(pdf)
    # has content
    if pdf['content'] < 1:
        if len(data) > 1:
            return extract_multi(pdf['content'], data)
        return extract_acuerdo(pdf['content'], data)
    return None


def fetch_pdf(date:str, data:[]):
    url = f'https://www.poderjudicialcdmx.gob.mx/wp-content/PHPs/boletin/boletin_repositorio/{date}1.pdf'
    # fetch
    response = requests.get(url)
    # create pdf
    filename = Path('metadata.pdf')
    filename.write_bytes(response.content)

    ## SQL
    if result is None:
        pass
    for r in result:
        sql = f'{r['acuerdos']}'
    ###
    result = is_parsed(data)

# public methods
# --------------
def fetch_day(date, data):
    now = str(date).split('-')
    now = str().join(now[::-1])
    fetch_pdf(now, data)


def fetch_history(data):
    init_date = date(2020, 8, 1)
    now = datetime.now().date()
    while now != init_date:
        fetch_day(now, data)
        now = now - timedelta(days=1)
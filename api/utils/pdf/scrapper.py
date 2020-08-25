import bs4
import requests
from time import sleep

# Scrap Tipos
def scrap_tipo(data):
    b_url = 'https://www.dgepj.cjf.gob.mx/internet/expedientes/ExpedienteyTipo.asp'
    body = {
        'Organismo': data['org_id'],
        'Buscar': 'Buscar',
        'Circuito': data['cir_id'],
    }
    html = requests.post(b_url, body)
    soup = bs4.BeautifulSoup(html.text)
    
    # Tipos
    select = soup.find(
        'select', {
            'name': 'TipoAsunto',
        })
    options = select.findAll('option')
    
    # Object
    results = {} 
    if len(options) > 1:
        for o in options:
            results[o.get('value')] = o.text

        return results

# Scrap Circuitos
def scrap_circuitos(url, circuito):
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text)

    # Circuito
    c_name = soup.find(
        'input', {
            'name': 'CircuitoName',
        })
    c_name = c_name['value']    
    
    c_id = soup.find(
        'input', {
            'name': 'Circuito',
        })
    c_id = c_id['value']

    # Organismos
    select = soup.find(
        'select', {
            'name': 'Organismo',
        })
    options = select.findAll('option')

    # Object
    results = {
        'c_name': c_name,
        'c_id': c_id,
        'organismos': {}
    }
    if len(options) > 1:
        for o in options:
            o_id = o.get('value')
            o_txt = o.text

            data = {
                'org_id': o_id,
                'cir_id': c_id,
            }            
            results['organismos'][o_id] = {
                o_txt: scrap_tipo(data),
            }

        return True, results
    return False, results

# GET circuitos
def get_circuitos():
    cirs_ids = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        20, 30, 38, 39, 40, 41, 42, 43,
        44, 45, 46, 47, 48, 49, 50, 51,
        52, 53, 54, 55, 56, 109
    ]
    circuitos = {}
    #for i in range(1, 1000):
    for i in cirs_ids:
        b_url = f'https://www.dgepj.cjf.gob.mx/internet/expedientes/circuitos.asp?Cir={i}'
        flag, result = scrap_circuitos(b_url, i)
        if flag:
            circuitos[i] = result
    return circuitos

# GET Acuerdos
def get_acuerdos(data):
    t_ast = data['t_ast']
    id_org = data['id_org']
    n_exp = data['n_exp']

    b_url = 'https://www.dgepj.cjf.gob.mx/siseinternet/reportes/vercaptura.aspx?'
    form = f'tipoasunto={t_ast}&organismo={id_org}&expediente={n_exp}&tipoprocedimiento=0'

    html = requests.get(b_url + form)
    soup = bs4.BeautifulSoup(html.text)

    select = soup.find(
            'table', {
                'id': 'grvAcuerdos',
            })
    tabla = select.findAll('tr')
    titles = tabla[0].findAll('th')

    acuerdos = []
    for a in tabla[1:]:
        ac_data = a.findAll('td')
        acuerdo = {}
        for v in range(len(titles[:-1])):
            acuerdo[titles[v].text] = ac_data[v].text
        acuerdos.append(acuerdo)

    for ac in acuerdos:
        ac['No.'] = ac['No.'].replace('\n', '')
    
    return acuerdos
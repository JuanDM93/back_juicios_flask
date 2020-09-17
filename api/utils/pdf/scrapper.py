import bs4
import requests
from api.utils.session import get_response


def scrap_tipo(s, data):
    # Scrap Tipos
    b_url = 'https://www.dgepj.cjf.gob.mx/'
    b_url += 'internet/expedientes/ExpedienteyTipo.asp'
    body = {
        'Organismo': data['org_id'],
        'Buscar': 'Buscar',
        'Circuito': data['cir_id'],
    }
    html = s.post(b_url, body)
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


def scrap_circuitos(s, url, circuito):
    # Scrap Circuitos
    html = get_response(s, url)
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
                o_txt: scrap_tipo(s, data),
            }
        return True, results
    return False, results


def get_circuitos():
    # GET circuitos
    cirs_ids = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        20, 30, 38, 39, 40, 41, 42, 43,
        44, 45, 46, 47, 48, 49, 50, 51,
        52, 53, 54, 55, 56, 109
    ]
    circuitos = {}
    with requests.sessions.Session() as s:
        # for i in range(1, 1000):
        for i in cirs_ids:
            b_url = 'https://www.dgepj.cjf.gob.mx/'
            b_url += f'internet/expedientes/circuitos.asp?Cir={i}'
            flag, result = scrap_circuitos(s, b_url, i)
            if flag:
                circuitos[i] = result
        return circuitos


def get_acuerdos(data):
    # GET Acuerdos -PUBLICO- mods al b_federals
    t_ast = data['t_ast']
    id_org = data['id_org']
    n_exp = data['n_exp']

    b_url = 'https://www.dgepj.cjf.gob.mx/'
    b_url += 'siseinternet/reportes/vercaptura.aspx?'
    form = f'tipoasunto={t_ast}'
    form += f'&organismo={id_org}'
    form += f'&expediente={n_exp}'

    with requests.sessions.Session() as s:
        html = get_response(s, b_url + form)
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


def get_federals(datas):
    # dailyFederal
    for d in datas:
        d['acuerdos'] = get_acuerdos(d)


def scrap_locals(session, xfun, args=[]):
    url = 'http://boletinpj.poderjudicialcdmx.gob.mx:816/v2/'

    body = {
            'xjxfun': f'{xfun}',
            'xjxargs[]': [],
        }

    for arg in args:
        a = f'S{arg}'
        body['xjxargs[]'].append(a)

    response = session.post(url, body)

    if len(args) > 1:
        fun = 'numero'
        json = response.json()
        ob = json.get('xjxobj')
        text = ob[-1]['data']
    else:
        fun = 'materia'
        text = response.text

    soup = bs4.BeautifulSoup(text)
    select = soup.find(
        'select', {
            'name': f'slc{fun}',
        })
    options = select.findAll('option')

    result = {}
    for o in options[1:]:
        value = o.get('value')
        text = str(o.text).replace(' ', '')
        text = text.replace('\"}]}', '')
        result[text] = value

    return result


def build_json_salas(j_locals):
    nums = [
        '',
        'PRIMERA',
        'SEGUNDA',
        'TERCERA',
        'CUARTA',
        'QUINTA',
        'SEXTA',
        'SEPTIMA',
        'OCTAVA',
        'NOVENA',
        'DECIMA',
    ]

    salas = j_locals['SALA']

    nombres = {}
    for tipo in salas:
        nombres[tipo] = []
        s_nums = salas[tipo]
        for n in s_nums:
            name = nums[int(n)] + ' SALA DE LO ' + tipo
            nombres[tipo].append(name)

    return nombres


def build_json_juz(j_locals):
    unidades = [
        '',
        'PRIMERO',
        'SEGUNDO',
        'TERCERO',
        'CUARTO',
        'QUINTO',
        'SEXTO',
        'SEPTIMO',
        'OCTAVO',
        'NOVENO',
        'DECIMO',
    ]
    decimos = [
        '',
        'DECIMO',
        'VIGESIMO',
        'TRIGESIMO',
        'CUADRAGESIMO',
        'QUINCUAGESIMO',
        'OCTOGESIMO',
        'SEPTUAGESIMO',
        # MAX 73
    ]

    juzgados = j_locals['JUZGADO']

    nombres = {}
    for tipo in juzgados:
        nombres[tipo] = []
        j_nums = juzgados[tipo]
        for n in j_nums.values():
            d_num = decimos[int(n[:1])]
            u_num = unidades[int(n[1:])]
            name = f'{d_num} {u_num} DE LO {tipo}'
            nombres[tipo].append(name)

    return nombres


def scrapper_locals():
    # --- get nombres
    url = 'http://boletinpj.poderjudicialcdmx.gob.mx:816/v2/'
    with requests.sessions.Session() as s:
        response = get_response(s, url)

        soup = bs4.BeautifulSoup(response.text)
        select = soup.find(
            'select', {
                'name': 'slcautoridad',
            })
        options = select.findAll('option')

        result = {}
        for o in options[1:]:
            o_txt = str(o.text).replace(' ', '')
            o_txt = o_txt.replace('\"}]}', '')
            value = o.get('value')
            print(f"{value}:{o_txt}")

            result[o_txt] = {}
            materias = scrap_locals(s, 'Materias', [value])

            for m in materias:
                numeros = scrap_locals(s, 'Numeros', [value, materias.get(m)])
                result[o_txt][m] = numeros

        nombres_salas = build_json_salas(result['SALA'])
        nombres_juzgados = build_json_juz(result['JUZGADO'])
        # get_sqls(0)
        # db_connect(sql)
        result = (nombres_salas, nombres_juzgados)
        return result

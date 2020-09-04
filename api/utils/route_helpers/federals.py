import bs4
import requests
from time import sleep
from api.utils.mail.service import sendMulti
from api.utils.db import db_connect


def registrarCorreosAbogadosFederales(
        data,
        listaCorreoAbogadosFederales
        ):
    sql = "SELECT id FROM juicios_federales WHERE n_exp = '"
    sql += str(data['n_exp'])
    sql += "' AND t_ast = " + str(data['t_ast'])
    sql += " AND id_org = " + str(data['id_org'])
    sql += " AND cir_id = " + str(data['cir_id'])
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    id_juicio_federal = rv["id"]

    data = ""
    for CorreoAbogadoLocal in listaCorreoAbogadosFederales:
        data += "('" + str(id_juicio_federal)
        data += "', '" + CorreoAbogadoLocal + "'), "
        # TODO
        # enviarCorreo(correoabogadolocal, 'texto formateado'--data['nombre'])
    data = data[:-2]

    sql = "INSERT INTO abogados_responsables_juicios_federales"
    sql += " (id_juicio_federal, email) VALUES"
    sql += data
    db_connect(sql)


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

    html = statusJuiciosFederales(b_url + form)

    if html is None:
        return []

    soup = bs4.BeautifulSoup(html)

    select = soup.find(
            'table', {
                'id': 'grvAcuerdos',
            })

    if select is None:
        return []

    tabla = select.findAll('tr')
    titles = tabla[0].findAll('th')

    titulos = [
        "No",
        "Fecha_del_Auto",
        "Tipo_Cuaderno",
        "Fecha_de_publicacion",
        "Resumen",
        "parametros",
    ]

    acuerdos = []
    for a in tabla[1:]:
        ac_data = a.findAll('td')
        acuerdo = {}
        for v in range(len(titulos)):
            if v == len(titles) - 1:
                link = ac_data[v].findAll('a')
                href = link[0].get('href')
                href = href.replace('javascript:DoVerAcuerdo(', '')
                href = href.replace(")", '')
                href = href.replace('\"', '')
                # print(str(href).findAll('DoVerAcuerdo'))
                acuerdo[titulos[v]] = href.split(',')
            else:
                acuerdo[titulos[v]] = ac_data[v].text

        acuerdos.append(acuerdo)

    for ac in acuerdos:
        ac['No'] = ac['No'].replace('\n', '')

    # for ac in acuerdos:
    #   print(ac['parametros'][4][0:10])
    for ac in acuerdos:
        sintesisURL = "https://www.dgepj.cjf.gob.mx/siseinternet/Actuaria/VerAcuerdo.aspx?"
        sintesisURL += "listaAcOrd=" + ac['parametros'][1]
        sintesisURL += "&listaCatOrg=" + ac['parametros'][0]
        sintesisURL += "&listaNeun=" + ac['parametros'][2]
        sintesisURL += "&listaAsuId=" + ac['parametros'][3]
        sintesisURL += "&listaExped=" + ac['parametros'][6]
        sintesisURL += "&listaFAuto=" + ac['parametros'][4][0:10]
        sintesisURL += "&listaFPublicacion=" + ac['parametros'][5][0:10]

        htmlsintesis = statusJuiciosFederales(sintesisURL)

        htmls = bs4.BeautifulSoup(htmlsintesis)
        sinstesistxt = htmls.find(
            'span', {
                'id': 'lblAcuerdo',
            })

        ac['url'] = sintesisURL

        txtsintesis = sinstesistxt.get_text()
        txtsintesis = txtsintesis.replace('\n', ' ')
        txtsintesis = txtsintesis.replace('   ', '')
        ac['acuerdo'] = txtsintesis

    return acuerdos


"""
  "parametros": [
     0       "10", -----> listaCatOrg*
    1      "2", ----> listaAcOrd *
      2      "26276852", ---> listaNeun*
      3      "1", ----> AsuId*
      4      "10/01/2020 12:00:00 a.m.", ----> listaFAuto*
       5     "13/01/2020 12:00:00 a.m.", --->  FPublicacion
       6     "1/2020" ---> listaExped*
        ]
"""


def validarJuicioFederal(dataflag):
    # Validar expediente
    sql = "SELECT COUNT(1) AS BIT FROM juicios_federales "
    sql += " WHERE juicios_federales.n_exp = '" + str(dataflag['n_exp'])
    sql += "' AND juicios_federales.t_ast = " + str(dataflag['t_ast'])
    sql += " AND juicios_federales.id_org = " + str(dataflag['id_org'])
    sql += " AND juicios_federales.cir_id = " + str(dataflag['cir_id'])
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    if rv["BIT"] == 0:
        return False
    return True


def validarAcuerdosFederales(url):
    # Validar expediente
    sql = "SELECT COUNT(1) AS BIT FROM acuerdos_juicios_federales "
    sql += "WHERE url = '" + str(url)
    sql += "'"
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    if rv["BIT"] == 0:
        return False
    return True


def statusJuiciosFederales(url):
    with requests.Session() as s:
        response = s.get(url)
        # TODO check other status??? timeouts...
        if response.status_code == 200:
            return response.content
        if response.status_code == 500:
            sleep(1)
            return statusJuiciosFederales(url)
        return None


def informacionJuicioAcuerdo(data):
    sql = "select  juicios_federales.id as id_juicio_federal,"
    sql += "circuitos_federales.NOM_CIR as circuitos_NOM_CIR,"
    sql += "circuitos_federales.NOM_LARGO as circuitos_NOM_LARGO,"
    sql += "juicios_federales.n_exp,"
    sql += "juicios_federales.Quejoso_Actor_Recurrente_Concursada,"
    sql += "juicios_federales.Tercero_Interesado_Demandado_Acreedor,"
    sql += "juicios_federales.Autoridades,"
    sql += "juzgados_federales.nombre_juzgado,"
    sql += "tipo_de_juicios_federales.nombre_tipo_juicio "
    sql += "From juicios_federales "
    sql += "INNER JOIN circuitos_federales on circuitos_federales.c_id = juicios_federales.cir_id "
    sql += "INNER JOIN juzgados_federales on juzgados_federales.org_id = juicios_federales.id_org "
    sql += "INNER JOIN tipo_de_juicios_federales on tipo_de_juicios_federales.t_ast = juicios_federales.t_ast "
    sql += " WHERE juicios_federales.n_exp = '" + str(data['n_exp'])
    sql += "' AND juicios_federales.t_ast = " + str(data['t_ast'])
    sql += " AND juicios_federales.id_org = " + str(data['id_org'])
    sql += " AND juicios_federales.cir_id = " + str(data['cir_id'])
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    return rv


def correosLigadosJuiciosFederales(id_juicio_federal):
    # Correos juicios federales
    sql = "SELECT email "
    sql += "FROM abogados_responsables_juicios_federales "
    sql += "WHERE id_juicio_federal  = " + str(id_juicio_federal)
    cur, response = db_connect(sql)
    rv = cur.fetchall()
    return rv


def listaCorreosLigador(id_juicio_federal):
    lista = []
    for correo in correosLigadosJuiciosFederales(id_juicio_federal):
        lista.append(correo["email"])
    return lista


def informacionAcuerdosFederales(id_juicio_federal):
    sql = "SELECT * "
    sql += "FROM acuerdos_juicios_federales "
    sql += "WHERE id_juicio_federal  = " + str(id_juicio_federal)
    sql += " ORDER BY Fecha_de_publicacion DESC"
    cur, response = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["Fecha_de_publicacion"] = r["Fecha_de_publicacion"].strftime('%Y-%m-%d')
    for r in rv:
        r["Fecha_del_Auto"] = r["Fecha_del_Auto"].strftime('%Y-%m-%d')
    return rv


def insertarAcuerdosDB(dataExp):

    for data in dataExp:

        dataInsert = get_acuerdos(data)
        rv = informacionJuicioAcuerdo(data)

        id_juicio_federal = rv["id_juicio_federal"]
        values = ""
        acuerdos = []

        for datain in dataInsert:

            if validarAcuerdosFederales(datain["url"]) is False:

                Fecha_del_Auto = datain["Fecha_del_Auto"].split('-')
                datain["Fecha_del_Auto"] = Fecha_del_Auto[2] + "-" + Fecha_del_Auto[1] + "-" + Fecha_del_Auto[0]
                Fecha_de_publicacion = datain["Fecha_de_publicacion"].split('-')
                datain["Fecha_de_publicacion"]   = Fecha_de_publicacion[2] + "-" + Fecha_de_publicacion[1] + "-" + Fecha_de_publicacion[0]

                values += "( " + str(id_juicio_federal) + ",'" + str(datain["Fecha_de_publicacion"]) + "',"
                values += " '" + str(datain["Fecha_del_Auto"]) + "','" + str(datain["Tipo_Cuaderno"]) + "',"
                values += " '" + str(datain["acuerdo"]) + "','" + str(datain["url"]) + "'),"
                acuerdos.append(datain)

        if len(values) > 0:

            values = values[:-1]
            sql = "INSERT INTO "
            sql += "acuerdos_juicios_federales (id_juicio_federal,Fecha_de_publicacion, "
            sql += "Fecha_del_Auto,Tipo_Cuaderno,acuerdo,url)"
            sql += "VALUES " + values
            db_connect(sql)

            rv["acuerdos"] = acuerdos
            rv["tipo"] = data['tipo']
            rv["emails"] = listaCorreosLigador(id_juicio_federal)
            sendMulti(rv)


def eliminarCorreosAbogadosFederales(
    # Eliminar abogados reponsables
        id_juicio_federal, listaCorreoAbogadosFederalesElimar):
    data = "("
    for CorreoAbogadoFederales in listaCorreoAbogadosFederalesElimar:
        data += "'" + CorreoAbogadoFederales + "', "
    data = data[:-2]
    data += ")"
    sql = "DELETE from abogados_responsables_juicios_federales WHERE email IN "
    sql += data
    sql += " AND id_juicio_federal = " + str(id_juicio_federal)
    db_connect(sql)


def eliminarAcuerdosFederales(id_juicio_federal):
    # eliminar acuerdos locales
    sql = "DELETE FROM acuerdos_juicios_federales where id_juicio_federal = "
    sql += str(id_juicio_federal)
    __, response = db_connect(sql)

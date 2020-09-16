import bs4
import requests
from time import sleep
from api.utils.mail.service import sendMulti
from api.utils.db import db_connect
from datetime import datetime


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
    data = data[:-2]

    sql = "INSERT INTO abogados_responsables_juicios_federales"
    sql += " (id_juicio_federal, email) VALUES"
    sql += data
    db_connect(sql)


def get_acuerdos(data):
    # GET Acuerdos -PUBLICO- mods al b_federals
    response = {}
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
        response["acuerdos"] = []
        response["sentencias"] = []
        return response

    soup = bs4.BeautifulSoup(html)
    select = soup.find(
            'table', {
                'id': 'grvAcuerdos',
            })
    if select is None:
        response["acuerdos"] = []
        response["sentencias"] = []
        return response
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
                acuerdo[titulos[v]] = href.split(',')
            else:
                acuerdo[titulos[v]] = ac_data[v].text
        acuerdos.append(acuerdo)

    for ac in acuerdos:
        ac['No'] = ac['No'].replace('\n', '')

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
    tabletacuerdos = soup.find(
            'table', {
                'id': 'grvReporteSentencias',
            })
    if select is None:
        response["acuerdos"] = acuerdos
        response["sentencias"] = []
        return response
    tablaproceso = tabletacuerdos.findAll('tr')

    titulosAcuerdos = [
        "asunto",
        "fecha_ingreso",
        "tema",
        "archivo"
    ]
    sentencias = []
    for a in tablaproceso[1:]:
        ac_data = a.findAll('td')
        sentencia = {}
        for v in range(len(titulosAcuerdos)):
            if v == len(titulosAcuerdos) - 1:
                link = ac_data[v].findAll('a')
                onclick = link[0].get('onclick')
                onclick = onclick.replace('AbrirVentana(', '')
                onclick = onclick.replace(");", '')
                onclick = onclick.replace('\"', '')
                sentencia[titulosAcuerdos[v]] = onclick.split(',')
            else:
                sentencia[titulosAcuerdos[v]] = ac_data[v].text
        sentencias.append(sentencia)
    for ac in sentencias:
        ac['asunto'] = ac['asunto'].replace('\n', '')
        ac['fecha_ingreso'] = ac['fecha_ingreso'].replace('\n', '')
        ac['tema'] = ac['tema'].replace('\n', '')
        ac['tema'] = ac['tema'].replace('\n\n', '')
        ac['archivo'] = ac['archivo'][0].replace("'", '')
    response["acuerdos"] = acuerdos
    response["sentencias"] = sentencias
    return response

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


def validarSentenciasFederales(archivo):
    # Validar expediente
    sql = "SELECT COUNT(1) AS BIT FROM sentencias_federales "
    sql += "WHERE archivo = '" + str(archivo)
    sql += "'"
    cur, __ = db_connect(sql)
    rv = cur.fetchone()
    if rv["BIT"] == 0:
        return False
    return True


def statusJuiciosFederales(url):
    flag = 5    # intentos
    with requests.Session() as s:
        response = s.get(url)
        if response.status_code == 200:
            return response.content
        if flag > 0:
            sleep(flag)
            flag -= 1
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


def informacionSentenciasFederales(id_juicio_federal):
    sql = "SELECT * "
    sql += "FROM sentencias_federales "
    sql += "WHERE id_juicio_federal  = " + str(id_juicio_federal)
    sql += " ORDER BY fecha_ingreso DESC"
    cur, response = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["fecha_ingreso"] = r["fecha_ingreso"].strftime('%Y-%m-%d')
    return rv


def insertarAcuerdosDB(dataExp):
    for data in dataExp:
        scrapper = get_acuerdos(data)
        dataInsert = scrapper["acuerdos"]
        dataSentencias = scrapper["sentencias"]
        rv = informacionJuicioAcuerdo(data)
        id_juicio_federal = rv["id_juicio_federal"]
        values = ""
        valuesSentencias = ""
        acuerdos = []
        sentencias = []

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
            if any([
                rv['tipo'] == 'a_j_f',
                rv['tipo'] == 'd_j_f',
                rv['tipo'] == 'u_j_f']
                    ):
                sendMulti(rv)

        for datain in dataSentencias:
            if validarAcuerdosFederales(datain["archivo"]) is False:
                fecha_ingreso = datain["fecha_ingreso"].split('/')
                datain["fecha_ingreso"] = fecha_ingreso[2] + "-" + fecha_ingreso[1] + "-" + fecha_ingreso[0]
                valuesSentencias += "( " + str(id_juicio_federal) + ",'" + str(datain["asunto"]) + "',"
                valuesSentencias += " '" + str(datain["fecha_ingreso"]) + "','" + str(datain["tema"]) + "',"
                valuesSentencias += " '" + str(datain["archivo"]) + "'),"
                sentencias.append(datain)
        if len(valuesSentencias) > 0:
            valuesSentencias = valuesSentencias[:-1]
            sql = "INSERT INTO "
            sql += "sentencias_federales (id_juicio_federal,asunto, "
            sql += "fecha_ingreso,tema,archivo)"
            sql += "VALUES " + valuesSentencias
            db_connect(sql)


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


def eliminarSentenciasFederales(id_juicio_federal):
    # eliminar acuerdos locales
    sql = "DELETE FROM sentencias_federales where id_juicio_federal = "
    sql += str(id_juicio_federal)
    __, response = db_connect(sql)


def urlFederales(data):
    t_ast = data['t_ast']
    id_org = data['id_org']
    n_exp = data['n_exp']

    b_url = 'https://www.dgepj.cjf.gob.mx/'
    b_url += 'siseinternet/reportes/vercaptura.aspx?'
    form = f'tipoasunto={t_ast}'
    form += f'&organismo={id_org}'
    form += f'&expediente={n_exp}'
    return b_url + form


def sqlEnviarCorreoFederal():
    dataMail = []
    fechasql = datetime.strftime(
        datetime.now(),
        '%Y-%m-%d'
    )
    # fechasql = "2020-02-25"
    sql = "SELECT email as emails FROM usuarios "
    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = [r["emails"]]
    for r in rv:
        r["acuerdos"] = acuerdosObjetosSqlFederales(r["emails"][0], fechasql)
    for data in rv:
        if len(data["acuerdos"]) > 0:
            dataMail.append(data)
    for datal in dataMail:
        datal['tipo'] = 'daily_j_f'
        sendMulti(datal)


def acuerdosObjetosSqlFederales(email, fecha):
    sql = "SELECT juicios_federales.n_exp, "
    sql += "circuitos_federales.NOM_CIR, "
    sql += "circuitos_federales.NOM_LARGO, "
    sql += "juzgados_federales.nombre_juzgado, "
    sql += "tipo_de_juicios_federales.nombre_tipo_juicio, "
    sql += "acuerdos_juicios_federales.Fecha_de_publicacion, "
    sql += "acuerdos_juicios_federales.acuerdo "
    sql += "FROM  usuarios  "
    sql += "INNER JOIN abogados_responsables_juicios_federales ON abogados_responsables_juicios_federales.email = usuarios.email "
    sql += "INNER JOIN juicios_federales ON juicios_federales.id = abogados_responsables_juicios_federales.id_juicio_federal "
    sql += "INNER JOIN circuitos_federales ON circuitos_federales.c_id = juicios_federales.cir_id "
    sql += "INNER JOIN juzgados_federales ON juzgados_federales.org_id = juicios_federales.id_org "
    sql += "INNER JOIN tipo_de_juicios_federales ON tipo_de_juicios_federales.t_ast = juicios_federales.t_ast "
    sql += "INNER JOIN acuerdos_juicios_federales ON acuerdos_juicios_federales.id_juicio_federal = juicios_federales.id "
    sql += "WHERE usuarios.email = '" + str(email) + "'"
    sql += "AND acuerdos_juicios_federales.Fecha_de_publicacion = '" + str(fecha) + "'"
    sql += "GROUP BY acuerdos_juicios_federales.acuerdo, acuerdos_juicios_federales.Fecha_de_publicacion  "
    cur, response = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["Fecha_de_publicacion"] = r["Fecha_de_publicacion"].strftime('%Y-%m-%d')
    return rv

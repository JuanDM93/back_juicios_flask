from flask_mail import Mail, Message
from . import m_help


mail = Mail()


def search_msg(data):
    if data['tipo'] == 'a_j_l':
        return m_help.ms_actual_local(data)

    if data['tipo'] == 'a_j_f':
        return m_help.ms_actual_fed(data)

    if data['tipo'] == 'n_j_l':
        return m_help.ms_nuevo_local(data)


def sendMulti(data):
    subject, message = search_msg(data)
    with mail.connect() as conn:
        for user in data['emails']:
            msg = Message(
                recipients=[user],
                subject=subject,
                body=message,
            )
            conn.send(msg)


"""
rv = [
  {
    "tipo": a_j_l,
    "actor": "ACTO",
    "acuerdos": [
      {
        "descripcion": "Jiménez Leija Steisi Deniss vs. Díaz Ortiz Naely Juriko Controversias \ndel Orden Familiar 1 Acdo. Núm. Exp. 379/2020",
        "fecha": "Sun, 02 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "González Zavala María Eva vs. Fuentes Sosa José Alfredo y González \nEligio Ana Lizbet Controversias del Orden Familiar 1 Acdo. Núm. \nExp. 379/2020",
        "fecha": "Mon, 03 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Alcántara Alcántara José Adelaido Sucesorio Familiar 1 Acdo. \nNúm. Exp. 379/2020",
        "fecha": "Tue, 04 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Alarcón Hernández Cersar Daniel vs. Hernández Monroy Guadalupe \nExh. Familiar 1 Acdo. en Exhorto. Núm. Exp. 379/2020",
        "fecha": "Wed, 05 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Jiménez Leija Steisi Deniss vs. Díaz Ortiz Naely Juriko Controversias \ndel Orden Familiar 1 Acdo. Núm. Exp. 379/2020",
        "fecha": "Thu, 06 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Ramírez Tena Giovanni Ezequiel. (su Suc) Sucesorio Familiar 1 \nAcdo. Núm. Exp. 379/2020",
        "fecha": "Sun, 09 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Vargas Peñaloza Gabriela vs. Sergio Martínez Téllez Controversias \ndel Orden Familiar 1 Acdo. Núm. Exp. 379/2020",
        "fecha": "Mon, 10 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Urrea Campaña Rosa Isela vs. Manuel Gerardo Berthier Delgado \nEspecial Familiar 1 Acdo. Núm. Exp. 379/2020",
        "fecha": "Tue, 11 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Vargas Peñaloza Gabriela vs. Sergio Martínez Téllez Controversias \ndel Orden Familiar 1 Acdo. Núm. Exp. 379/2020",
        "fecha": "Wed, 12 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Engrandes Galván Néstor vs. Sara Cleotilde Pantoja Álvarez \nEspecial Familiar Expdllo. 1 Acdo. Núm. Exp. 379/2020",
        "fecha": "Thu, 13 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "del Orden Familiar Principal 1 Acdo. Núm. Exp. 379/2020",
        "fecha": "Sun, 16 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Serreno Chino Filogonio vs. Ferrer Flores Julieta Controversias del \nOrden Familiar 1 Acdo. Núm. Exp. 379/2020",
        "fecha": "Mon, 17 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Haro Sedeño Gabriela vs. Mesa Cruz Miguel Mauricio Controversias \ndel Orden Familiar Principal 1 Acdo. Núm. Exp. 379/2020",
        "fecha": "Tue, 18 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "López Pérez Leticia vs. Martha Lydia Luna Hernández Ord. Civil \nPrevención 1 Acdo. Núm. Exp. 379/2020",
        "fecha": "Wed, 19 Aug 2020 00:00:00 GMT"
      },
      {
        "descripcion": "Rojas Martínez Lydia y vs. Rojas Martínez María de Lourdes \ny Otros Juris. Voluntaria Civil Desechado 1 Acdo. Núm. \nExp. 379/2020",
        "fecha": "Thu, 20 Aug 2020 00:00:00 GMT"
      }
    ],
    "demandado": "DEMA",
    "emails": [
      {
        "email": "ricaror@hotmail.com"
      }
    ],
    "expediente": "379/2020",
    "id_juicio_local": 105,
    "juzgado": "PRIMERO DE LO CIVIL"
  },
]

<p><strong>VARIABLE JUZGADO&nbsp;</strong></p>
<p><strong>N<b>&uacute;mero</b><span>&nbsp;de&nbsp;</span><b>expediente: </b></strong>Variable expediente</p>
<p><strong>Actor: </strong>Variable expediente</p>
<p><strong>Demandado: </strong>Variable demandado</p>
<p style="text-align: center;"><strong>Acuerdos</strong></p>
<p style="text-align: justify;"><strong>Variable fecha: </strong>Variable descripcion</p>
"""


# este metodo esta en route_helpers
import api.utils.route_helpers as rh
from datetime import (datetime, timedelta)
from api.utils.db import db_connect


def sqlenviarcorreo(data):
    fechasql = datetime.strftime(
        datetime.now() - timedelta(days=1),
        '%Y-%m-%d'
    )
    sql = ""
    if(len(data) > 1):
        sql = "SELECT juicios_locales.numero_de_expediente as expediente, "
        sql += "juzgados_locales.nombre as juzgado,"
        sql += "juicios_locales.actor, juicios_locales.demandado, "
        sql += "juicios_locales.id as id_juicio_local "
        sql += "FROM acuerdos_locales INNER JOIN juicios_locales "
        sql += "ON juicios_locales.id = acuerdos_locales.id_juicio_local "
        sql += "INNER JOIN juzgados_locales "
        sql += "ON juzgados_locales.id = juicios_locales.id_juzgado_local "
        sql += "WHERE  acuerdos_locales.fecha = '" + fechasql + "'"

        cur, __ = db_connect(sql)
        rv = cur.fetchall()
        for r in rv:
            r["emails"] = rh.correosLigadosJuiciosLocales(r["id_juicio_local"])
        for r in rv:
            r["acuerdos"] = rh.acuerdoslocalesdiarios(r["id_juicio_local"])
        return rv

    sql = "select juicios_locales.numero_de_expediente as expediente, "
    sql = "juzgados_locales.nombre as juzgado, juicios_locales.actor,"
    sql += "juicios_locales.demandado, juicios_locales.id "
    sql += "as id_juicio_local FROM juicios_locales "
    sql += " INNER JOIN juzgados_locales ON juzgados_locales.id"
    sql += " = juicios_locales.id_juzgado_local "
    sql += " WHERE juicios_locales.numero_de_expediente = '"
    sql += str(data[0]["expediente"])
    sql += "' AND juicios_locales.id_juzgado_local = "
    sql += str(data[0]["id_juzgado_local"])

    cur, __ = db_connect(sql)
    rv = cur.fetchall()
    for r in rv:
        r["emails"] = rh.correosLigadosJuiciosLocales(r["id_juicio_local"])
    for r in rv:
        r["acuerdos"] = rh.acuerdosHistoricos(r["id_juicio_local"])
    return rv

## TODO 
# mailinfo

from api.db import db_connect


def ms_actual_local(data):
    """
    data['id_juzgado_local']
    data['numero_de_expediente']
    data['actor']
    data['demandado']
    data['tipo']

    templar_acrulocal.html
    """
    msg = f"{data['actor']} ha actualizado su juicio local"
    sub = f"{data['numero_de_expediente']}"
    return sub, msg

def ms_actual_fed(data):
    """
    data['id_juzgado_local']
    data['numero_de_expediente']
    data['actor']
    data['demandado']
    data['tipo']
    """
    msg = f"{data['actor']} ha actualizado su juicio local"
    sub = f"{data['numero_de_expediente']}"
    return sub, msg

def ms_nuevo_local(data):
    """
    data['id_juzgado_local']
    data['numero_de_expediente']
    data['actor']
    data['demandado']
    data['tipo']
    """
    msg = f"{data['actor']} ha actualizado su juicio local"
    sub = f"{data['numero_de_expediente']}"
    return sub, msg

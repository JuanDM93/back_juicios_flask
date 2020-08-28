# TODO
# mailinfo


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


def ms_nuevo_usuario(data):
    msg = f'<p><strong>Bienvenido {data["apellido_paterno"]} {data["apellido_materno"]}  {data["nombre"]} </strong></p>'
    msg += '<p><strong>Datos de usuario</strong></p>'
    msg += f'<p><strong>Despacho: </strong>{data["nombre_despacho"]}</p>'
    msg += f'<p><strong>Nombre: </strong>{data["apellido_paterno"]} {data["apellido_materno"]}  {data["nombre"]}</p>'
    msg += f'<p><strong>Usuario: </strong>{data["email"]}</p>'
    msg += f'<p><strong>Contrase&ntilde;a:</strong>&nbsp;{data["password"]}</p>'
    sub = "Usted ha sido dado de alta como nuevo usuario"
    return sub, msg


def ms_actualizar_usuario(data):
    msg = f'<p><strong>Actualizacion de perfil {data["apellido_paterno"]} {data["apellido_materno"]}  {data["nombre"]} </strong></p>'
    msg += '<p><strong>Datos de usuario</strong></p>'
    msg += f'<p><strong>Despacho: </strong>{data["nombre_despacho"]}</p>'
    msg += f'<p><strong>Nombre: </strong>{data["apellido_paterno"]} {data["apellido_materno"]}  {data["nombre"]}</p>'
    msg += f'<p><strong>Usuario: </strong>{data["email"]}</p>'
    if data['newPwd'] is True:
        msg += f'<p><strong>Contrase&ntilde;a:</strong>&nbsp;{data["password"]}</p>'
    sub = "Usted ha actualizado su usuario"
    return sub, msg


def ms_eliminar_usuario(data):
    msg = f'<p><strong>Usted ha sido dado de baja del sistema {data["apellido_paterno"]} {data["apellido_materno"]}  {data["nombre"]} </strong></p>'
    sub = "Usted ha sido dado de baja del sistema"
    return sub, msg

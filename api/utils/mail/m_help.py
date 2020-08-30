# TODO
# mailinfo


def ms_actual_local(data):
    """
msg = f"<p><strong>VARIABLE JUZGADO&nbsp;</strong></p>"
<p><strong>N<b>&uacute;mero</b><span>&nbsp;de&nbsp;</span><b>expediente: </b></strong>Variable expediente</p>
<p><strong>Actor: </strong>Variable expediente</p>
<p><strong>Demandado: </strong>Variable demandado</p>
<p style="text-align: center;"><strong>Acuerdos</strong></p>
<p style="text-align: justify;"><strong>Variable fecha: </strong>Variable descripcion</p>
    """
    sub = f'Alta de Juicio en {data["juzgado"]} con expediente {data["expediente"]}'
    msg = f'<p><strong>{data["juzgado"]}</strong></p>'
    msg += f'<p><strong>N<b>&uacute;mero</b><span>&nbsp;de&nbsp;</span><b>expediente: </b></strong>{data["expediente"]}</p>'
    msg += f'<p><strong>Actor:  </strong>{data["actor"]}</p>'
    msg += f'<p><strong>Demandado: </strong>{data["demandado"]}</p>'
    msg += '<p><strong>Acuerdos</strong></p>'
    for acuerd in data["acuerdos"]:
        msg += f'<p><strong>{acuerd["fecha"]}: </strong>{acuerd["descripcion"]}</p>'

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

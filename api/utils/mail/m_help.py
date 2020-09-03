# TODO
# mailinfo


def ms_actual_local(data):

    sub = f'Alta de Juicio en {data["juzgado"]} con expediente {data["expediente"]}'
    msg = f'<p><strong>{data["juzgado"]}</strong></p>'
    msg += f'<p><strong>N<b>&uacute;mero</b><span>&nbsp;de&nbsp;</span><b>expediente: </b></strong>{data["expediente"]}</p>'
    msg += f'<p><strong>Actor:  </strong>{data["actor"]}</p>'
    msg += f'<p><strong>Demandado: </strong>{data["demandado"]}</p>'
    msg += '<p><strong>Acuerdos</strong></p>'
    for acuerd in data["acuerdos"]:
        msg += f'<p><strong>{acuerd["fecha"]}: </strong>{acuerd["descripcion"]}</p>'

    return sub, msg


def ms_actualizacion_local(data):
    sub = f'Actualizacion de Juicio en {data["juzgado"]} con expediente {data["expediente"]}'
    msg = f'<p><strong>{data["juzgado"]}</strong></p>'
    msg += f'<p><strong>N<b>&uacute;mero</b><span>&nbsp;de&nbsp;</span><b>expediente: </b></strong>{data["expediente"]}</p>'
    msg += f'<p><strong>Actor:  </strong>{data["actor"]}</p>'
    msg += f'<p><strong>Demandado: </strong>{data["demandado"]}</p>'
    msg += '<p><strong>Acuerdos</strong></p>'
    for acuerd in data["acuerdos"]:
        msg += f'<p><strong>{acuerd["fecha"]}: </strong>{acuerd["descripcion"]}</p>'

    return sub, msg


def ms_delet_local(data):

    sub = f'Eliminación de Juicio en {data["juzgado"]} con expediente {data["expediente"]}'
    msg = f'<p><strong>Se elimno Juicio en {data["juzgado"]} con expediente {data["expediente"]}</strong></p>'

    return sub, msg


def ms_actual_fed(data):

    sub = f'Alta de Juicio Federal en {data["circuitos_NOM_LARGO"]} '
    sub += f'{data["circuitos_NOM_CIR"]} '
    sub += f'{data["nombre_juzgado"]} '
    sub += f'{data["nombre_tipo_juicio"]} '
    sub += f'con expediente {data["n_exp"]} '
    msg = f'<p><strong>{data["circuitos_NOM_LARGO"]} {data["circuitos_NOM_CIR"]}</strong></p>'
    msg += f'<p><strong>{data["nombre_juzgado"]}</strong></p>'
    msg += f'<p><strong>{data["nombre_tipo_juicio"]}</strong></p>'
    msg += f'<p><strong>N<b>&uacute;mero</b><span>&nbsp;de&nbsp;</span><b>expediente: </b></strong>{data["n_exp"]}</p>'
    msg += f'<p><strong>Quejoso/Actor/Recurrente/Concursada: </strong>{data["Quejoso_Actor_Recurrente_Concursada"]}</p>'
    msg += f'<p><strong>Tercero Interesado/Demandado/Acreedor: </strong>{data["Tercero_Interesado_Demandado_Acreedor"]}</p>'
    msg += f'<p><strong>Autoridades: </strong>{data["Autoridades"]}</p>'

    for acuerd in data["acuerdos"]:
        msg += f'<p><strong>No de Acuerdo: </strong>{acuerd["No"]}</p>'
        msg += f'<p><strong>Fecha del Auto: </strong>{acuerd["Fecha_del_Auto"]}</p>'
        msg += f'<p><strong>Tipo Cuaderno: </strong>{acuerd["Tipo_Cuaderno"]}</p>'
        msg += f'<p><strong><span>Fecha de publicaci&oacute;n</span>: </strong>{acuerd["Fecha_de_publicacion"]}</p>'
        msg += f'<p><strong>Acuerdo: </strong>{acuerd["acuerdo"]}</p>'

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

# TODO
# mailinfo


def ms_actual_local(data):

    sub = f'Alta de Juicio Local en {data["juzgado"]} con expediente {data["expediente"]}'
    msg = f'<p>Se acaba de agregar el siguiente asunto a tus juicios asignados:</p>'
    msg += f'<strong>{data["juzgado"]}</strong><br>'
    msg += f'<strong>N<b>&uacute;mero</b><span>&nbsp;de&nbsp;</span><b>expediente: </b></strong>{data["expediente"]}<br>'
    msg += f'<strong>Actor:  </strong>{data["actor"]}<br>'
    msg += f'<strong>Demandado: </strong>{data["demandado"]}<br>'
    """
    for acuerd in data["acuerdos"]:
        msg += f'<p><strong>{acuerd["fecha"]}: </strong>{acuerd["descripcion"]}</p>'
        """
    return sub, msg


def ms_actualizacion_local(data):
    sub = f'Actualización de Juicio Local en {data["juzgado"]} con expediente {data["expediente"]}'
    msg = f'<p>Se acaba de modificar el siguiente asunto:</p>'
    msg += f'<strong>{data["juzgado"]}</strong><br>'
    msg += f'<strong>N<b>&uacute;mero</b><span>&nbsp;de&nbsp;</span><b>expediente: </b></strong>{data["expediente"]}<br>'
    msg += f'<strong>Actor:  </strong>{data["actor"]}<br>'
    msg += f'<strong>Demandado: </strong>{data["demandado"]}<br>'
    """
    for acuerd in data["acuerdos"]:
        msg += f'<p><strong>{acuerd["fecha"]}: </strong>{acuerd["descripcion"]}</p>'
        """
    return sub, msg


def daily_j_l(data):
    sub = 'Actualización de Juicios Locales'
    msg = f'<p>Acuerdo(s) publicado(s) el día de hoy:</p>'
    msg += '<table width="100%" border="1" cellpadding="0" cellspacing="0" bordercolor="#000000">'
    msg += '<tr><th style="background-color: #424242; color: white;">Juzgado</th>'
    msg += '<th style="background-color: #424242; color: white;">Fecha</th>'
    msg += '<th style="background-color: #424242; color: white;">No de Expediente</th>'
    msg += '<th style="background-color: #424242; color: white;">Acuerdo</th></tr>'
    for acuerd in data["acuerdos"]:
        msg += "<tr>"
        msg += f'<td>{acuerd["nombre_juzgado"]}</td>'
        msg += f'<td>{acuerd["fecha"]}</td>'
        msg += f'<td>{acuerd["numero_de_expediente"]}</td>'
        msg += f'<td>{acuerd["descripcion"]}</td>'
        msg += "</tr>"
    return sub, msg


def daily_j_f(data):
    sub = 'Actualización de Juicios Federales'
    msg = f'<p>Acuerdo(s) publicado(s) el día de hoy:</p>'
    msg += '<table width="100%" border="1" cellpadding="0" cellspacing="0" bordercolor="#000000">'
    msg += '<tr>'
    
    
    msg += '<th style="background-color: #424242; color: white;">Quejoso/Actor/Recurrente/Concursada</th>'
    msg += '<th style="background-color: #424242; color: white;">Tercero Interesado/Demandado/Acreedor</th>'
    msg += '<th style="background-color: #424242; color: white;">Juzgado</th>'
    msg += '<th style="background-color: #424242; color: white;">No de Expediente</th>'
    msg += '<th style="background-color: #424242; color: white;">Tipo de Juicio</th>'
    msg += '<th style="background-color: #424242; color: white;">Fecha de publicación</th>'
    msg += '<th style="background-color: #424242; color: white;">Acuerdo</th></tr>'
    for acuerd in data["acuerdos"]:
        msg += "<tr>"
        
        msg += f'<td>{acuerd["Quejoso_Actor_Recurrente_Concursada"]}</td>'
        msg += f'<td>{acuerd["Tercero_Interesado_Demandado_Acreedor"]}</td>'
        msg += f'<td>{acuerd["nombre_juzgado"]}</td>'
        msg += f'<td>{acuerd["n_exp"]}</td>'
        msg += f'<td>{acuerd["nombre_tipo_juicio"]}</td>'
        msg += f'<td>{acuerd["Fecha_de_publicacion"]}</td>'        
        msg += f'<td>{acuerd["acuerdo"]}</td>'
        msg += "</tr>"
    return sub, msg


def ms_delet_local(data):
    sub = f'Eliminación de Juicio en {data["juzgado"]} con expediente {data["expediente"]}'
    msg = f'<p><strong>Se elimino Juicio en {data["juzgado"]} con expediente {data["expediente"]}</strong></p>'

    return sub, msg


def ms_delet_Federal(data):
    sub = f'Eliminación de Juicio Federal en {data["NOM_LARGO"]} '
    sub += f' {data["NOM_CIR"]}'
    sub += f' {data["nombre_juzgado"]}'
    sub += f' {data["nombre_tipo_juicio"]}'
    sub += f'con expediente {data["n_exp"]}'
    msg = f'<p><strong>Se elimino Juicio Federal en {data["NOM_LARGO"]}'
    msg += f' {data["NOM_CIR"]}'
    msg += f' {data["nombre_juzgado"]}'
    msg += f' {data["nombre_tipo_juicio"]}'
    msg += f' con expediente {data["n_exp"]}</strong></p>'

    return sub, msg


def ms_actual_fed(data):
    sub = f'Alta de Juicio Federal en {data["circuitos_NOM_LARGO"]} '
    sub += f'{data["circuitos_NOM_CIR"]} '
    sub += f'{data["nombre_juzgado"]} '
    sub += f'{data["nombre_tipo_juicio"]} '
    sub += f'con expediente {data["n_exp"]} '
    msg = f'<p>Se acaba de agregar el siguiente asunto a tus juicios asignados:<br>'
    msg += f'<strong>{data["circuitos_NOM_LARGO"]} {data["circuitos_NOM_CIR"]}</strong><br>'
    msg += f'<strong>{data["nombre_juzgado"]}</strong><br>'
    msg += f'<strong>{data["nombre_tipo_juicio"]}</strong><br>'
    msg += f'<strong>N<b>&uacute;mero</b><span>&nbsp;de&nbsp;</span><b>expediente: </b></strong>{data["n_exp"]}<br>'
    msg += f'<strong>Quejoso/Actor/Recurrente/Concursada: </strong>{data["Quejoso_Actor_Recurrente_Concursada"]}<br>'
    msg += f'<strong>Tercero Interesado/Demandado/Acreedor: </strong>{data["Tercero_Interesado_Demandado_Acreedor"]}<br>'
    """
    for acuerd in data["acuerdos"]:
        msg += f'<p><strong>No de Acuerdo: </strong>{acuerd["No"]}</p>'
        msg += f'<p><strong>Fecha del Auto: </strong>{acuerd["Fecha_del_Auto"]}</p>'
        msg += f'<p><strong>Tipo Cuaderno: </strong>{acuerd["Tipo_Cuaderno"]}</p>'
        msg += f'<p><strong><span>Fecha de publicaci&oacute;n</span>: </strong>{acuerd["Fecha_de_publicacion"]}</p>'
        msg += f'<p><strong>Acuerdo: </strong>{acuerd["acuerdo"]}</p>'
        """
    return sub, msg


def ms_actualizar_fed(data):
    sub = f'Actualización de Juicio en Federal en {data["circuitos_NOM_LARGO"]} '
    sub += f'{data["circuitos_NOM_CIR"]} '
    sub += f'{data["nombre_juzgado"]} '
    sub += f'{data["nombre_tipo_juicio"]} '
    sub += f'con expediente {data["n_exp"]} '
    msg = f'Se acaba de modificar el siguiente asunto:<br>'
    msg += f'<strong>{data["circuitos_NOM_LARGO"]} {data["circuitos_NOM_CIR"]}</strong><br>'
    msg += f'<strong>{data["nombre_juzgado"]}</strong><br>'
    msg += f'<strong>{data["nombre_tipo_juicio"]}</strong><br>'
    msg += f'<strong>N<b>&uacute;mero</b><span>&nbsp;de&nbsp;</span><b>expediente: </b></strong>{data["n_exp"]}<br>'
    msg += f'<strong>Quejoso/Actor/Recurrente/Concursada: </strong>{data["Quejoso_Actor_Recurrente_Concursada"]}<br>'
    msg += f'<strong>Tercero Interesado/Demandado/Acreedor: </strong>{data["Tercero_Interesado_Demandado_Acreedor"]}<br>'
    msg += f'<strong>Autoridades: </strong>{data["Autoridades"]}<br>'

    """
    for acuerd in data["acuerdos"]:
        msg += f'<p><strong>No de Acuerdo: </strong>{acuerd["No"]}</p>'
        msg += f'<p><strong>Fecha del Auto: </strong>{acuerd["Fecha_del_Auto"]}</p>'
        msg += f'<p><strong>Tipo Cuaderno: </strong>{acuerd["Tipo_Cuaderno"]}</p>'
        msg += f'<p><strong><span>Fecha de publicaci&oacute;n</span>: </strong>{acuerd["Fecha_de_publicacion"]}</p>'
        msg += f'<p><strong>Acuerdo: </strong>{acuerd["acuerdo"]}</p>'
        """
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

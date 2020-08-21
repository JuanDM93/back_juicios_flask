from flask_mail import Mail, Message


mail = Mail()

def search_msg(data):

    from . import m_help

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

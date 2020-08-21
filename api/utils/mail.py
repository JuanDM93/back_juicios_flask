from flask_mail import Mail, Message


mail = Mail()

def search_msg():

    from m_help import *

    if data['tipo'] is 'a_j_l':
        return ms_actual_local(data)

    if data['tipo'] is 'a_j_f':
        return ms_actual_fed(data)
        
    if data['tipo'] is 'n_j_l':
        return ms_nuevo_local(data)


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

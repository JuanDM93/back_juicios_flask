from flask import current_app
from flask_mail import Mail, Message


def init_mail():
    return Mail(current_app)

def sendMail(text, sender, recipients=[]): 
    mail = init_mail()
    msg = Message(
        text,
        sender = sender,
        recipients = recipients) 
    msg.body = 'Hello Flask message sent from Flask-Mail'
    mail.send(msg) 
    return 'Sent'

def sendMulti(users):
    mail = init_mail()
    with mail.connect() as conn:
        for user in users:
            message = '...'
            subject = "hello, %s" % user.name
            msg = Message(
                recipients=[user.email],
                body=message,
                subject=subject
            )
            conn.send(msg)
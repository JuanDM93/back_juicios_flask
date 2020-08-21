from flask_mail import Mail, Message


mail = Mail()

def sendMail(recipients=[]):
    subject = 'Testin'
    message = 'Hello Flask message sent from Flask-Mail'
    msg = Message(
                recipients=recipients,
                body=message,
                subject=subject
            )
    mail.send(msg)
    return f'Sent to: {recipients}'

def sendMulti(users):
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

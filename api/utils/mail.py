from flask_mail import Message


def sendMail(mail, text, sender, recipients=[]): 
    msg = Message(
        text,
        sender = sender,
        recipients = recipients) 
    msg.body = 'Hello Flask message sent from Flask-Mail'
    mail.send(msg) 
    return 'Sent'


def sendMulti(mail, users):
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
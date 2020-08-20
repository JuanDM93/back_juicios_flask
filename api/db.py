from flask_mysqldb import MySQL


db = MySQL()


def db_connect(sql=None):
    cur = db.connection.cursor()
    if sql is not None:
        #app.logger.info(sql) 
        result = cur.execute(sql)
        db.connection.commit()
    return cur, result
from flask_mysqldb import MySQL
from flask import current_app


def init_db():
    return MySQL(current_app)


def db_connect(db, sql=None):
    cur = db.connection.cursor()
    if sql is not None:
        #app.logger.info(sql) 
        result = cur.execute(sql)
        db.connection.commit()
        return result
    return cur, result
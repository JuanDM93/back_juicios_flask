from flask_mysqldb import MySQL


def db_init(app):
    return MySQL(app)


def db_connect(db, sql=None):
    cur = db.connection.cursor()
    if sql is not None:
        #app.logger.info(sql) 
        result = cur.execute(sql)
        db.connection.commit()
        return result
    return cur, result
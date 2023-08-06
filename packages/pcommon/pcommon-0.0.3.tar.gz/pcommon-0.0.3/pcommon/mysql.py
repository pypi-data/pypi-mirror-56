import pymysql


class MySQL:
    connection = None
    cursor = None
    logger = None

    def __init__(self, db):
        self.connection = pymysql.connect(host = db.get('HOST'), port = db.get('PORT'), user = db.get('USER'),
                                          password = db.get('PASSWORD'), db = db.get('NAME'),
                                          charset = 'utf8')
        self.cursor = self.connection.cursor(cursor = pymysql.cursors.DictCursor)

    def query(self, sql, args = None):
        self.cursor.execute(sql, args)
        self.connection.close()
        res = self.cursor.fetchall()
        return res

    def exec(self, sql, args = None):
        self.cursor.execute(sql, args)
        self.connection.commit()
        self.connection.close()

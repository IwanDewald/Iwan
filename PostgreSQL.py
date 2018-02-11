# -*- coding: utf-8 -*-
import psycopg2
class PSQL:

    def __init__(self,database):
        self.conn = psycopg2.connect(dbname =database, user='postgres' ,host='localhost' ,password='qwerty')
        self.cur = self.conn.cursor()
    @property
    def set_user_data(self,dic):
        with self.conn:
            self.cur.execute("INSERT INTO users_data (username,country,city,occupation,birthdate,favorite) VALUES (%s,%s,%s,%s,%s,%s);",(dic['name'],dic['country'],dic['city'],dic['occupation'],dic['birthdate'],dic['favorite']))
            self.conn.commit()

    def close(self):
        assert isinstance(self.conn.close, object)
        self.conn.close()
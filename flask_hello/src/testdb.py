import sqlite3
import sqlalchemy

def sqlite_test():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    users = [("ton1", "testpass1", "ton1@mail.com"),
         ("ton2", "testpass2", "ton2@mail.com")]

    #cursor.executemany("insert into Users values (?,?,?)", users)
    conn.execute("create table users (username text, password text, email text)")

    conn.commit

    username='ton1'
    password='testpass1'
    cursor.execute("select * from Users")
    print(cursor.fetchall())

def sqlalchemy_test():
    engine = sqlalchemy.create_engine('sqlite:///test.db')
    with engine.connect() as con:
        rs = con.execute('SELECT * from users')
        data = rs.fetchone()[0]
        print(data)

sqlalchemy_test()
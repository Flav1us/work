import sqlite3

def containsUser(username):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("select username from Users where username=?", [(username)])
    res = cursor.fetchall().__len__() > 0
    conn.commit()
    conn.close()
    return res

def createUser(username, password, email):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("insert into Users values (?, ?, ?)", (username, password, email))
    conn.commit()
    conn.close()
    return 1

def areValidCredentials( username, password):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("select * from Users where username=? and password=?", (username, password))
    res = cursor.fetchall().__len__() > 0
    conn.commit()
    conn.close()
    return res

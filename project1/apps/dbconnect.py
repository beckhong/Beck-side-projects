import MySQLdb


def dbconnect():
    connect = MySQLdb.connect(host='127.0.0.1',
                              user='root')

    cursor = connect.cursor()

    return cursor, connect


def register(user, passwd, host='127.0.0.1'):
    
    connect = MySQLdb.connect(host=host,
                              user=user,
                              passwd=passwd)
    cursor = connect.cursor()
    return cursor, connect
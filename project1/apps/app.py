from flask import Flask, jsonify
from dbconnect import dbconnect


apps = Flask(__name__)


def read_sql_file(sql_path):
    '''
    Read mysql command lines in mysql file.
    
    args:
        sql_path: string, the *.sql file path.

    return:
        command_list: list, the mysql command lines.
    '''
    command_collect = []
    for line in open(sql_path):
        line = line.replace('\n', '')
        find_empty = line.replace(' ', '')
        if find_empty != '' and line[:2] != '--':
            command_collect += line
    command_str = ''.join(command_collect)
    command_list = [query+';' for query in command_str.split(';')[:-1]]
    return command_list


@apps.route('/')
def home():
    '''
    My first flask website.
    '''
    return 'Hello! My name is beck.'


@apps.route('/test-connection/')
def connectMySQLTest():
    '''
    Check mysql server is connected.
    '''
    try:
        cursor, connect = dbconnect()
        return 'Connecting mysql server~'
    except Exception as e:
        return str(e)

            
@apps.route('/bookshop/', methods=['POST', 'GET'])
def user_bookshop():
    '''
    Insert bookshop data to mysql database and output all books in website.
    '''
    try:
        cursor, connect = dbconnect()
    except Exception as e:
        return str(e)

    # create book_shop table
    query_list = read_sql_file("./apps/MySQL/book_shop.sql")

    for query in query_list:
        cursor.execute(query)
        if "SHOW TABLES;" in query:
            tables = cursor.fetchall()
            print(tables)
            if ("books",) in tables:
                break

    select_query = "SELECT * FROM books;"
    cursor.execute(select_query)
    res = cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    
    return jsonify({'content': field_names, 'books': res})


if __name__ == '__main__':
    apps.run(host='0.0.0.0', port=8086, debug=True)

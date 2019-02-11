import MySQLdb
from flask import Flask, jsonify
from flask_restful import Resource, Api


apps = Flask(__name__)
api = Api(apps)
connect = MySQLdb.connect(host='127.0.0.1',
                          user='root')
# connect = MySQLdb.connect(host='127.0.0.1',
#                           user='root',
#                           passwd="")

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


def query_result(query, cursor):
    '''Using MySQL command to get values.
    '''
    cursor.execute(query)
    values = cursor.fetchall()
    return values


class MySQLQuery(Resource):
    '''MySQL query api. '''
    def get(self, query):
        cursor = connect.cursor()
        cursor.execute("USE book_shop;")
        if 'USE' in query:
            return "Cannot use USE method, only USE book_shop."
        if 'INSERT' in query:
            cursor.execute(query)
            connect.commit()
            return query + " is successful!"

        results = query_result(query, cursor)
        return results

api.add_resource(MySQLQuery, '/bookshop/<string:query>')

@apps.route('/')
def home():
    '''
    My first flask website.
    '''
    return 'Hello! My name is beck.'

            
@apps.route('/bookshop/', methods=['POST', 'GET'])
def user_bookshop():
    '''
    Insert bookshop data to mysql database and output all books in website.
    '''
    cursor = connect.cursor()
    # check database name book_shop is existence
    databases = query_result("SHOW DATABASES;", cursor)
    if ("book_shop",) not in databases:
        # table books must be created
        query_list = read_sql_file("./apps/MySQL/book_shop.sql")
        for query in query_list:
            cursor.execute(query)
        connect.commit()
    else:
        cursor.execute("USE book_shop;")

    try:
        res = query_result("SELECT * FROM books;", cursor)
        field_names = [i[0] for i in cursor.description]
    except MySQLdb._exceptions.ProgrammingError:
        return "Table 'book_shop.books' doesn't exist!"

    return jsonify({'content': field_names, 'books': res})


@apps.route('/bookshop/reset/', methods=['POST', 'GET'])
def reset_bookshop():
    '''
    Reset bookshop items.
    '''
    cursor = connect.cursor()
    try:
        cursor.execute("DROP DATABASE book_shop;")
    except MySQLdb._exceptions.OperationalError:
        pass
    query_list = read_sql_file("./apps/MySQL/book_shop.sql")
    for query in query_list:
        cursor.execute(query)
    connect.commit()
    return "Reset bookshop is done!"


if __name__ == '__main__':
    apps.run(host='0.0.0.0', port=8086, debug=True)

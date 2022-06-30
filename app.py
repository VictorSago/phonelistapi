from flask import *
import datetime
from sqlite3 import Error
import sqlite3


# TODO refactor + cleanup

db_file = "phone.db"
tablename = "phonelist"

def get_connection(dbfile):
    conn = None
    try:
        conn = sqlite3.connect(dbfile)
    except Error as e:
        print(e)
    return conn

def read_phonelist(conn):
    statement = f"SELECT * FROM {tablename};"
    cur = conn.cursor()
    cur.execute(statement)
    rows = cur.fetchall()
    cur.close()
    return rows

def read_phone(conn, name):
    cur = conn.cursor()
    statement = f"SELECT phone FROM {tablename} WHERE name = :name;"
    cur.execute(statement, {"name": name})
    rows = cur.fetchall()
    cur.close()
    return rows

def read_name(conn, phone):
    cur = conn.cursor()
    statement = f"SELECT name FROM {tablename} WHERE phone = :phone;"
    cur.execute(statement, {"phone": phone})
    rows = cur.fetchall()
    cur.close()
    return rows

def add_phone(conn, name, phone):
    cur = conn.cursor()
    statement = f"INSERT INTO {tablename} (name, phone) VALUES (:name, :phone);"
    cur.execute(statement, {"name": name, "phone": phone})
    cur.close()

def delete_phone(conn, name):
    statement = f"DELETE FROM {tablename} WHERE name = :name"
    cur = conn.cursor()
    cur.execute(statement, {"name": name})
    cur.close()

def save_phonelist(conn):
    try:
        conn.commit()
    except Error as e:
        print("No changes!")
        print(e)


app = Flask(__name__)

@app.route("/")
def start():
    connection = get_connection(db_file)
    now = datetime.datetime.now()
    current_date = [str(now.year), str(now.month), str(now.day)]
    if len(current_date[1]) < 2:
        current_date[1] = '0' + current_date[1]
    if len(current_date[2]) < 2:
        current_date[2] = '0' + current_date[2]
    smart = read_phonelist(connection)
    save_phonelist(connection)
    connection.close()
    return render_template('list.html', list=smart, date=current_date)

@app.route("/delete")
def delete_func():
    connection = get_connection(db_file)
    name=request.args['name']
    delete_phone(connection, name)
    save_phonelist(connection)
    connection.close()
    return render_template('delete.html', name=name)

@app.route("/insert")
def insert_func():
    connection = get_connection(db_file)
    name=request.args['name']
    phone=request.args['phone']
    add_phone(connection, name, phone)
    save_phonelist(connection)
    connection.close()
    return render_template('insert.html', name=name, phone=phone)

@app.route("/api")
def api_func():
    connection = get_connection(db_file)
    args=request.args
    action = args.get('action', default="Bad action", type=str)
    ret = None
    if action == "Bad action":
        ret = render_template('api_usage.html', action=action)
    elif action == 'phone':
        name = args.get('name', default="No name", type=str)
        if name == "No name":
            ret = render_template('api_usage.html', action=action)
        else:
            phone = read_phone(connection, name)
            if len(phone) < 1:
                ret = "Not Found"
            else:
                ret = phone[0][0]
    elif action == 'name':
        phone = args.get('phone', default="No phone", type=str)
        if phone == "No phone":
            ret = render_template('api_usage.html', action=action)
        else:
            if len(name) < 1:
                ret = "Not Found"
            else:
                ret = name[0][0]
    else:
        ret = f"Unknown action: '{action}'"
    connection.close()
    return ret
    

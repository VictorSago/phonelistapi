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
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonelist;")
    rows = cur.fetchall()
    cur.close()
    return rows

def read_phone(conn, name):
    cur = conn.cursor()
    #print(f"SELECT phone FROM phonelist WHERE name = '{name}';")            #TODO cleanup diagnostics
    cur.execute(f"SELECT phone FROM phonelist WHERE name = '{name}';")
    rows = cur.fetchall()
    cur.close()
    return rows

def read_name(conn, phone):
    cur = conn.cursor()
    #print(f"SELECT name FROM phonelist WHERE phone = '{phone}';")           #TODO cleanup diagnostics
    cur.execute(f"SELECT name FROM phonelist WHERE phone = '{phone}';")
    rows = cur.fetchall()
    cur.close()
    return rows

def add_phone(conn, name, phone):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO phonelist VALUES ('{name}', '{phone}');")
    cur.close()

def delete_phone(conn, name):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM phonelist WHERE name = '{name}';")
    cur.close()

def save_phonelist(conn):
    cur = conn.cursor()
    try:
        cur.execute("COMMIT;")
    except:
        print("No changes!")
    cur.close()


app = Flask(__name__)

@app.route("/")
def start():
    #conn = sqlite3.connect("phone.db")
    connection = get_connection(db_file)
    now = datetime.datetime.now()
    current_date = [str(now.year%100), str(now.month), str(now.day)]
    if len(current_date[1])<2:
        current_date[1] = '0'+current_date[1]
    if len(current_date[2])<2:
        current_date[2] = '0'+current_date[2]
    smart = read_phonelist(connection)
    save_phonelist(connection)
    connection.close()
    return render_template('list.html', list=smart, date=current_date)

@app.route("/delete")
def delete_func():
    #conn = sqlite3.connect("phone.db")
    connection = get_connection(db_file)
    name=request.args['name']
    delete_phone(connection, name)
    save_phonelist(connection)
    connection.close()
    return render_template('delete.html', name=name)

@app.route("/insert")
def insert_func():
    #conn = sqlite3.connect("phone.db")
    connection = get_connection(db_file)
    name=request.args['name']
    phone=request.args['phone']
    add_phone(connection, name, phone)
    save_phonelist(connection)
    connection.close()
    return render_template('insert.html', name=name, phone=phone)

@app.route("/api")
def api_func():
    #conn = sqlite3.connect("phone.db")
    connection = get_connection(db_file)
    args=request.args
    action = args.get('action', default="Bad action", type=str)
    if action == "Bad action":
        connection.close()
        return render_template('api_usage.html', action=action)
    if action == 'phone':
        name = args.get('name', default="No name", type=str)
        if name == "No name":
            connection.close()
            return render_template('api_usage.html', action=action)
        phone = read_phone(connection, name)
        connection.close()
        if len(phone) < 1:
            return "Not Found"
        return phone[0][0]
    elif action == 'name':
        phone = args.get('phone', default="No phone", type=str)
        if phone == "No phone":
            connection.close()
            return render_template('api_usage.html', action=action)
        name = read_name(connection, phone)
        connection.close()
        if len(name) < 1:
            return "Not Found"
        return name[0][0]
    else:
        connection.close()
        return f"Unknown action: '{action}'"
    


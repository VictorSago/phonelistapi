from flask import *
import datetime
import sqlite3


# TODO refactor + cleanup

def read_phonelist(C):
    cur = C.cursor()
    cur.execute("SELECT * FROM phonelist;")
    rows = cur.fetchall()
    cur.close()
    return rows

def read_phone(C, name):
    cur = C.cursor()
    print(f"SELECT phone FROM phonelist WHERE name = '{name}';")            #TODO cleanup diagnostics
    cur.execute(f"SELECT phone FROM phonelist WHERE name = '{name}';")
    rows = cur.fetchall()
    cur.close()
    return rows

def read_name(C, phone):
    cur = C.cursor()
    print(f"SELECT name FROM phonelist WHERE phone = '{phone}';")           #TODO cleanup diagnostics
    cur.execute(f"SELECT name FROM phonelist WHERE phone = '{phone}';")
    rows = cur.fetchall()
    cur.close()
    return rows

def add_phone(C, name, phone):
    cur = C.cursor()
    cur.execute(f"INSERT INTO phonelist VALUES ('{name}', '{phone}');")
    cur.close()

def delete_phone(C, name):
    cur = C.cursor()
    cur.execute(f"DELETE FROM phonelist WHERE name = '{name}';")
    cur.close()

def save_phonelist(C):
    cur = C.cursor()
    try:
        cur.execute("COMMIT;")
    except:
        print("No changes!")
    cur.close()


app = Flask(__name__)

@app.route("/")
def start():
    conn = sqlite3.connect("phone.db")
    now = datetime.datetime.now()
    D = [str(now.year%100), str(now.month), str(now.day)]
    if len(D[1])<2:
        D[1] = '0'+D[1]
    if len(D[2])<2:
        D[2] = '0'+D[2]
    smart = read_phonelist(conn)
    save_phonelist(conn)
    return render_template('list.html', list=smart, date=D)

@app.route("/delete")
def delete_func():
    conn = sqlite3.connect("phone.db")
    name=request.args['name']
    delete_phone(conn, name)
    save_phonelist(conn)
    return render_template('delete.html', name=name)

@app.route("/insert")
def insert_func():
    conn = sqlite3.connect("phone.db")
    name=request.args['name']
    phone=request.args['phone']
    add_phone(conn, name, phone)
    save_phonelist(conn)
    return render_template('insert.html', name=name, phone=phone)

@app.route("/api")
def api_func():
    conn = sqlite3.connect("phone.db")
    args=request.args
    print("Api_func: args:", args)                                          #TODO cleanup diagnostics
    action = args.get('action', default="Bad action", type=str)
    if action == "Bad action":
        return render_template('api_usage.html', action=action)
    if action == 'phone':
        name = args.get('name', default="No name", type=str)
        if name == "No name":
            return render_template('api_usage.html', action=action)
        phone = read_phone(conn, name)
        print("Api_func-phone:", phone)                                     #TODO cleanup diagnostics
        if len(phone) < 1:
            return "Not Found"
        return phone[0][0]
    elif action == 'name':
        phone = args.get('phone', default="No phone", type=str)
        if phone == "No phone":
            return render_template('api_usage.html', action=action)
        name = read_name(conn, phone)
        print("Api_func-name:", name)                                       #TODO cleanup diagnostics
        if len(name) < 1:
            return "Not Found"
        return name[0][0]
    else:
        return f"Unknown action: '{action}'"


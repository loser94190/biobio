from flask import Flask, render_template, request, url_for,flash
import sqlite3
import os.path

#radul e mare mafiot
#cel mai mare mafiot e chiar radul
#rada rada bio bio
def connect_db():
    return sqlite3.connect('big_database.db')


def create_tab(restaurant_name):
    conn = connect_db()
    query_cursor = conn.cursor()
    query_cursor.execute('CREATE TABLE ' + restaurant_name + '(id INT PRIMARY KEY AUTOINCREMENT, food TEXT, price DOUBLE, weight INT, tip TEXT)')
    conn.commit()


def insert_in_table(table_name, i_food, i_price, i_weight, i_tip):
    conn = connect_db()
    query_cursor = conn.cursor()
    query_cursor.execute('INSERT INTO ' + table_name  + ' (id,food,price,weight,tip)' + 'VALUES' + '(?,?,?,?)', (i_food, i_price, i_weight, i_tip))
    conn.commit()


app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "big_database.db")
db_rest_path = os.path.join(BASE_DIR, "restaurant_master.db")


@app.route('/')
def form():
    return render_template('form_submit.html')


'''
@app.route('/hello/', methods=['POST'])
def hello():
    food = request.form['mancare']
    number = request.form['numar_pers']
    food2 = food.split(',')
    return render_template('form_action_2.html', food=food2, number=number)
'''

@app.route('/form_submit', methods=['POST', 'GET'])
def search_by_input():
    count = 0
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    string1 = request.form['mancare']
    nr_pers = request.form['numar_pers']
    list1 = string1.split(',')
    list1_len = len(list1)
    rest_list = ['gicahagi']
    good_rest_list = []
    for r in rest_list:
        r_returned = curs.execute("SELECT food FROM " + r )
        r_items = r_returned.fetchall()
        temp_list = []
        for k in range(len(r_items)):
            temp_list.append(''.join(r_items[k]))       # for-ul asta transforma r_items, care e lista de tuple intr-o lista de strings (temp_list)
        for i in range(list1_len):
            if list1[i] in temp_list:
                count += 1
            else:
                pass
        if count == list1_len:
            good_rest_list.append(r)
    return render_template('form_action_2.html', lista_rest = good_rest_list)


@app.route('/add_rest', methods=['POST', 'GET'])
def add_rest():
    if request.method == 'POST':
        conn = sqlite3.connect(db_rest_path)
        query_cursor = conn.cursor()
        r_name = request.form['restaurant_name']
        coord_1 = request.form['coord1']
        coord_2 = request.form['coord2']
        query_cursor.execute("INSERT INTO big_restaurant(nume,coord1,coord2) VALUES(?,?,?,?)", (None, r_name, coord_1, coord_2))
        conn.commit()
    return render_template('add_rest.html')


@app.route('/inputs', methods=['POST', 'GET'])
def inputs():
    if request.method == 'POST':
        conn = sqlite3.connect('big_database.db')
        curs = conn.cursor()
        rezultat = curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=" + "'" + request.form['restaurant_name'] + "'" + ";")
        if rezultat.fetchone():
            rest_name = request.form['restaurant_name']
            mancare = request.form['food']
            nume_mancare = request.form['food_name']
            greutate = request.form['food_weight']
            pret = request.form['price']
            curs.execute('INSERT INTO ' + rest_name + '(food, price, weight, tip) VALUES(?,?,?,?)', (nume_mancare, pret, greutate, mancare))
            conn.commit()
        else:
            curs.execute('CREATE TABLE ' + request.form['restaurant_name'] + '(id INT PRIMARY KEY, food TEXT, price DOUBLE, weight INT, tip INT)')
            conn.commit()
            rest_name = request.form['restaurant_name']
            mancare = request.form['food']
            nume_mancare = request.form['food_name']
            greutate = request.form['food_weight']
            pret = request.form['price']
            curs.execute('INSERT INTO ' + rest_name + '(food, price, weight, tip) VALUES(?,?,?,?)', (nume_mancare, pret, greutate, mancare))
            conn.commit()
    return render_template('inputs.html')


@app.route('/list', methods=['POST', 'GET'])
def list():
    if request.method == 'POST':
        conn = sqlite3.connect('big_database.db')
        curs = conn.cursor()
        table_name = request.form['table_name']
        if len(table_name):
            rezultat = curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=" + "'" + table_name + "'" + ";")
            if rezultat.fetchone():
                table_value = curs.execute("SELECT * FROM " + table_name)
                value=table_value.fetchall()
                return render_template('list.html',table_result=value,increment=len(value))
        return render_template('list.html', table_name='', increment=0)
    if request.method == 'GET':
        return render_template('list.html', table_name='', increment=0)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080 ,debug=True)

    app.run(debug=True)
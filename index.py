from flask import Flask, render_template,url_for,redirect,request,session
#Create mysql connector to server database
import mysql.connector as mysql
# File and Directory
import os
# Hash Function
import hashlib
import random
import datetime

conn = mysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'n.0818570429',
    port = 3306,
    database = 'project_mdt'
)

app = Flask(__name__)
template_folder = os.path.join(os.path.dirname(__file__), "templates/")
app.static_folder = 'static'
app.static_url_path = '/static'

app.secret_key = "Web Project" #can name anything

#size not ocer 2MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 

#picture folder
UPLOAD_PICTURE = os.path.join(os.path.dirname(__file__), "static\picture")

@app.route('/', methods=["GET","POST"])
def index_check():
    session['user'] = ''
    session['audit'] = False
    return render_template('login.html')

@app.route('/register', methods=["GET","POST"])
def register():
    return render_template('register.html')

@app.route('/validate-register', methods=["GET","POST"])
def validate_register():
    email = request.form['email']
    user = request.form['user']
    password = request.form['password']
    #cfpassword = request.form['cfpassword']

    if email !='' and user !='':
        encypt_passwd = hashlib.md5(password.encode()).hexdigest()
        conn.reconnect()
        cur = conn.cursor()
        sql_insert = '''
            INSERT INTO username(username,email,password,audit)
            VALUES(%s, %s, %s, %s)
        '''
        val = (user, email, encypt_passwd, 1) #tuple
        cur.execute(sql_insert, val)
        conn.commit()
        conn.close()

        return render_template('login.html')
    else:
        return redirect('/register')

@app.route('/login', methods=["GET","POST"])
def login():
    return redirect('/')

@app.route('/validate-login', methods=["GET", "POST"])
def validate_login():
    user = request.form['user']
    password = request.form['password']
    try:
        if user !="" and password !="":
            conn.reconnect()
            cur = conn.cursor()
            sql = '''
                SELECT password FROM username
                WHERE username=%s and audit=1
            '''
            val = (user,) #tuple
            cur.execute(sql, val)
            data = cur.fetchone() #1 record ('werwerwerwerwerw','dadasdasdasd') <- dat[0]
            conn.close()

            encrpt_password = hashlib.md5(password.encode()).hexdigest()
            if encrpt_password == data[0]:
                session['user'] = user
                session['audit'] = True    
                return redirect('/index')
            else:
                return redirect('/login')

        else:
            return redirect('/login')
    except:
        return redirect('/login')

@app.route('/index', methods=["GET","POST"])
def add_data():
    conn.reconnect()
    cur = conn.cursor()
    sql = '''
        SELECT cloth_name,price,file_location,tag
        FROM clothes
        ORDER BY ID
        '''
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return render_template('index.html', clothes=data)

@app.route('/cart', methods=["GET","POST"])
def cart():
    username = session['user']
    cloth_name = request.form['cloth_name']
    price = request.form['price']
    file_location = request.form['file_location'] 

    conn.reconnect()
    cur = conn.cursor()
    sql = '''
        SELECT username,cloth_name,price,quantity,id_cart
        FROM cart
        WHERE username=%s
        '''
    val = (username,)
    cur.execute(sql,val)
    data = cur.fetchall()
    conn.close()
    create_new_id_cart = True
    for value in data:
        if username == value[0] and cloth_name == value[1]:
            sql = '''
                UPDATE cart SET quantity=%s
                WHERE id_cart=%s 
            '''
            val = (value[3]+1,value[4])
            conn.reconnect()
            cur = conn.cursor()
            cur.execute(sql,val)
            conn.commit()
            conn.close()
            create_new_id_cart = False

    if create_new_id_cart:
        conn.reconnect()
        cur = conn.cursor()
        sql_insert = '''
            INSERT INTO cart(username,cloth_name,price,quantity,file_location)
            VALUES(%s, %s, %s, %s, %s)
        '''
        val = (username, cloth_name, price, 1,file_location) #tuple
        cur.execute(sql_insert, val)
        conn.commit()
        conn.close()

    conn.reconnect()
    cur = conn.cursor()
    sql = '''
        SELECT username, cloth_name, price, quantity, file_location, price*quantity  AS total_price
        FROM cart
        WHERE username=%s
    '''
    val = (username,)
    cur.execute(sql,val)
    data = cur.fetchall()
    conn.close()

    subtotal = 0
    for value in data:
        subtotal = subtotal+value[5]

    return render_template('cart.html', cart = data,subtotal =subtotal)

@app.route('/cart-minus/<clothe>', methods=["GET","POST"])
def cart_minus(clothe):
    username = session['user']
    cloth_name = clothe
    conn.reconnect()
    cur = conn.cursor()
    sql = '''
        SELECT username,cloth_name,price,quantity,id_cart
        FROM cart
        WHERE username=%s
        '''
    val = (username,)
    cur.execute(sql,val)
    data = cur.fetchall()
    conn.close()
    create_new_id_cart = True
    for value in data:
        if username == value[0] and cloth_name == value[1]:
            print(22222222222)
            sql = '''
                UPDATE cart SET quantity=%s
                WHERE id_cart=%s 
            '''
            if value[3] >=0:
                print(1111111111)
                val = (value[3]-1,value[4])
            conn.reconnect()
            cur = conn.cursor()
            cur.execute(sql,val)
            conn.commit()
            conn.close()
            create_new_id_cart = False

    conn.reconnect()
    cur = conn.cursor()
    sql = '''
        SELECT username, cloth_name, price, quantity, file_location, price*quantity  AS total_price
        FROM cart
        WHERE username=%s
    '''
    val = (username,)
    cur.execute(sql,val)
    data = cur.fetchall()
    conn.close()
    
    subtotal = 0
    for value in data:
        subtotal = subtotal+value[5]

    return render_template('cart.html', cart = data,subtotal =subtotal)

@app.route('/cart-plus/<clothe>', methods=["GET","POST"])
def cart_plus(clothe):
    username = session['user']
    cloth_name = clothe
    conn.reconnect()
    cur = conn.cursor()
    sql = '''
        SELECT username,cloth_name,price,quantity,id_cart
        FROM cart
        WHERE username=%s
        '''
    val = (username,)
    cur.execute(sql,val)
    data = cur.fetchall()
    conn.close()
    create_new_id_cart = True
    for value in data:
        if username == value[0] and cloth_name == value[1]:
            print(22222222222)
            sql = '''
                UPDATE cart SET quantity=%s
                WHERE id_cart=%s 
            '''
            if value[3] >=0:
                print(1111111111)
                val = (value[3]+1,value[4])
            conn.reconnect()
            cur = conn.cursor()
            cur.execute(sql,val)
            conn.commit()
            conn.close()
            create_new_id_cart = False

    conn.reconnect()
    cur = conn.cursor()
    sql = '''
        SELECT username, cloth_name, price, quantity, file_location, price*quantity  AS total_price
        FROM cart
        WHERE username=%s
    '''
    val = (username,)
    cur.execute(sql,val)
    data = cur.fetchall()
    conn.close()
    
    subtotal = 0
    for value in data:
        subtotal = subtotal+value[5]

    return render_template('cart.html', cart = data,subtotal =subtotal)

@app.route('/cart-delete/<clothe>', methods=["GET","POST"])
def cart_delete(clothe):
    username = session['user']

    conn.reconnect()
    cur = conn.cursor()
    sql = 'DELETE FROM cart WHERE cloth_name=%s'
    val = (clothe,)
    cur.execute(sql, val)
    conn.commit()
    conn.close()

    conn.reconnect()
    cur = conn.cursor()
    sql = '''
        SELECT username, cloth_name, price, quantity, file_location, price*quantity  AS total_price 
        FROM cart
        WHERE username=%s
    '''
    val = (username,)
    cur.execute(sql,val)
    data = cur.fetchall()
    conn.close()
    
    subtotal = 0
    for value in data:
        subtotal = subtotal+value[5]

    return render_template('cart.html', cart = data,subtotal =subtotal)

@app.route('/logout', methods=["GET","POST"])
def log_out():
    session.pop('user', None)
    session.pop('audit', None)
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
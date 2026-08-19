from flask import Flask ,render_template ,redirect , request
import mysql.connector

app = Flask(__name__)

def db_connector():
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '',
        database = 'bank_management'
    )

    return db

@app.route('/')
def admin():
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def dashboard():
    return render_template('admin_dashboard.html')

@app.route('/customer_management')
def customer_management():
    return render_template('customer_management.html')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')


@app.route('/admin_log',methods=['post'])
def admin_log():
    email = request.form['email']
    password = request.form['password']

    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = 'select * from admin_log where email = %s and password = %s'
    values = (email,password)
    cursor.execute(query,values)
    info = cursor.fetchone()

    if info["email"] is None:
        return render_template('/admin_login.html', error = 'Email or Password Invalid')

    if email == info['email']:
        return redirect ('/admin_dashboard')

@app.route('/customer_management_created', methods=['post'])
def customer_management_created():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    pancard = request.form['pancard']
    ifsc = request.form['ifsc']
    aadhaar = request.form['aadhaar'] 
    address = request.form['address']

    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = ("insert into customer_management(firstname,lastname,phone,email,pancard,ifsc,aadhaar,address) values( %s ,%s ,%s ,%s ,%s ,%s,%s,%s)")
    values = (firstname,lastname,phone,email,pancard,ifsc,aadhaar,address)

    cursor.execute(query,values)
    db.commit()

    return redirect('/customer_management_table')

@app.route('/customer_management_table')
def customer_table():
    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = 'select * from customer_management'

    cursor.execute(query)
    customers = cursor.fetchall()

    return render_template('customer_management_table.html', customers = customers)

@app.route('/customer_edit/<id>')
def customer_edit(id):
    db=db_connector()
    cursor = db.cursor(dictionary=True )

    query = 'select * from customer_management where id=%s'
    values = (id,)
    cursor.execute(query,values)

    customer = cursor.fetchone()

    return render_template('/customer_edit.html' ,customer = customer)

@app.route('/update_customer/<id>',methods=['post'])
def update_customer(id):
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    pancard = request.form['pancard']
    ifsc = request.form['ifsc']
    aadhaar = request.form['aadhaar'] 
    address = request.form['address']

    db = db_connector()
    cursor = db.cursor(dictionary = True)
    
    query = 'update customer_management set firstname=%s,lastname=%s,phone=%s,email=%s,pancard=%s,ifsc=%s,aadhaar=%s,address=%s where id = %s'
    values = (firstname,lastname,phone,email,pancard,ifsc,aadhaar,address,id)
    cursor.execute(query,values)

    db.commit()
    return redirect('/customer_management_table')


@app.route('/delete_customer/<id>')
def delete_customer(id):
    print(id)
    db=db_connector()
    cursor = db.cursor()

    query = 'update customer_management set status = 0 where id = %s'
    values = (id,)
    print(query,values)
    cursor.execute(query,values)

    db.commit()

    return redirect('/customer_management_table')

@app.route('/active_customer/<id>')
def active_customer(id):
    db=db_connector()
    cursor = db.cursor()

    query = 'update customer_management set status = 1 where id = %s'
    values = (id,)
    cursor.execute(query,values)

    db.commit()

    return redirect('/customer_management_table')

@app.route('/account_creation')
def account_creation():

    db = db_connector()
    cursor = db.cursor(dictionary=True)

    query = "SELECT id, firstname, lastname FROM customer_management"
    cursor.execute(query)

    customers = cursor.fetchall()

    return render_template('account_creation.html',customers=customers)

if __name__ == '__main__':
    app.run(debug=True)
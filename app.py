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

@app.route('/account_creation')
def account_creation():
    return render_template('account_creation.html')

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
    fistname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    pancard = request.form['pancard']
    ifsc = request.form['ifsc']
    address = request.form['address']

    db = db.connector()
    cursor = db.cursor(dictionary = True)

    query ("insert into customer_management(firstname,lastname,phone,email,pancard,ifsc,address) values( %s ,%s ,%s ,%s ,%s ,%s,%s)")
    values = (firstname,lastname,phone,email,pancard,ifsc,address)

    cursor.execute(query,values)
    db.commit()

    return redirct('/customer_managment')

if __name__ == '__main__':
    app.run(debug=True)
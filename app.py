from flask import Flask ,render_template ,redirect , request
import random
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

@app.route('/transaction_request')
def transaction_request():
    return render_template('transaction_request.html')


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
    db=db_connector()
    cursor = db.cursor()

    query = 'update customer_management set status = 0 where id = %s'
    values = (id,)
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

@app.route('/create_account',methods=['post'])
def create_account():
    customer_id = request.form['customer_id']
    account_type = request.form['account_type']
    balance = request.form['balance']


    account_number=random.randint(10**6,10**7-1)
    account_num=f"19715{account_number}"

    db = db_connector()
    cursor = db.cursor()

    query = 'insert into accounts(customer_id,account_type,balance,account_number) values(%s,%s,%s,%s)'
    values = (customer_id,account_type,balance,account_num)
    cursor.execute(query,values)

    db.commit()

    return redirect('/account_table')

@app.route('/account_table')
def account_table():
    db=db_connector()
    cursor = db.cursor(dictionary = True)

    query = ('select * from accounts')
    cursor.execute(query)

    accounts = cursor.fetchall()

    return render_template('account_table.html',accounts = accounts)

@app.route('/account_detail/<customer_id>')
def account_detail(customer_id):
    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = 'select c.firstname,c.lastname,c.phone,c.email,c.pancard,c.aadhaar,c.ifsc,c.address,a.account_number,a.account_type,a.balance from customer_management as c inner join accounts as a on c.id=a.customer_id where c.id =%s'
    values = (customer_id,)
    cursor.execute(query,values)

    customer = cursor.fetchone()

    return render_template('account_detail.html' ,customer=customer)

@app.route('/account_edit/<customer_id>')
def account_edit(customer_id):
    db=db_connector()
    cursor = db.cursor(dictionary=True )

    query = 'select * from accounts where customer_id=%s'
    values = (customer_id,)
    cursor.execute(query,values)
    account = cursor.fetchone()

    customer_query = "SELECT id, firstname, lastname FROM customer_management where id =%s"
    customer_value = (customer_id, )
    cursor.execute(customer_query,customer_value)
    customer = cursor.fetchone()

    return render_template('account_edit.html' ,account = account ,customer = customer)

@app.route('/update_account',methods=['post'])
def update_account():
    account_type = request.form['account_type']
    balance = request.form['balance']

    db = db_connector()
    cursor = db.cursor()

    query = 'update accounts set account_type = %s ,balance =%s'
    values = (account_type,balance)
    cursor.execute(query,values)
    db.commit()

    return redirect('/account_table')

@app.route('/account_delete/<id>')
def account_delete(id):
    db=db_connector()
    cursor = db.cursor()

    query = 'update accounts set status = 0 where id = %s'
    values = (id,)
    cursor.execute(query,values)

    db.commit()

    return redirect('/account_table')

@app.route('/account_active/<id>')
def account_active(id):
    db=db_connector()
    cursor = db.cursor()

    query = 'update accounts set status = 1 where id = %s'
    values = (id,)
    cursor.execute(query,values)

    db.commit()

    return redirect('/account_table')

@app.route('/request_form',methods =['post'])
def request_form():
    account_number = request.form['account_number']
    account_type = request.form['account_type']
    ifsc = request.form['ifsc']
    transaction_type = request.form['transaction_type']
    amount = request.form['amount']

    db=db_connector()
    cursor = db.cursor()
    
    query = 'insert into transaction_request(account_number,account_type,ifsc,transaction_type,amount) values (%s,%s,%s,%s,%s)'
    values = (account_number.account_type,ifsc,transaction_type,amount)
    cursor.execute(query,values)

    db.commit()

    return render_template ('transaction_request.html')

@app.route('/transaction')
def transaction():
    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = 'select * from transaction_request where status = 1'
    cursor.execute(query)

    transactions = cursor.fetchall()

    return render_template('transaction.html', transactions = transactions)

@app.route('/approve_request/<account_number>')
def approve_request(account_number):
    db = db_connector()
    cursor = db.cursor(dictionary = True)

    balance_query = 'select balance from accounts where account_number = %s'
    balance_values = (account_number, )
    cursor.execute(balance_query,balance_values)

    account =cursor.fetchone()

    query = 'select * from transaction_request where account_number = %s'
    values = (account_number, )
    cursor.execute(query,values)

    data = cursor.fetchone()

    if data.transaction_type == 'withdraw':
        balance = account.balance - data.amount
    else :
        balance = account.balance +data.amount

    
            



if __name__ == '__main__':
    app.run(debug=True)
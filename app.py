from flask import Flask ,render_template ,redirect , request ,session
import random
import mysql.connector
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "your_secret_key"

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
    return render_template('login/login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/commission')
def commission():
    return render_template('admin/commission/index.html')

@app.route('/create_customer')
def create_customer():
    return render_template('admin/customer_managment/create.html')

@app.route('/cus_dashboard')
def cus_dashboard():
    id = session['id']

    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = 'select * from accounts where customer_id = %s'
    values = (id,)
    cursor.execute(query,values)

    customer = cursor.fetchone()
    cursor.close()

    return render_template('customer/dashboard.html', customer = customer )

@app.route('/transaction_request')
def transaction_request():
    return render_template('customer/transaction_request.html')


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

    if info:
        session['email'] = info['email']
        session['role'] = 'admin'
        return redirect('/dashboard')

    cus_query = 'select * from customer_management where email = %s and password = %s'
    cus_values = (email,password)
    cursor.execute(cus_query,cus_values)
    cus_info = cursor.fetchone()

    if cus_info:
        session['email'] = cus_info['email']
        session['role'] = 'customer'
        session['id']=cus_info['id']
        return redirect('/cus_dashboard')
    else :
        return redirect('/')

@app.route('/customer_management_table')
def customer_table():
    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = 'select * from customer_management'

    cursor.execute(query)
    customers = cursor.fetchall()

    return render_template('admin/customer_management/table.html', customers = customers)

@app.route('/customer_management_created', methods=['post'])
def customer_management_created():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    password = request.form['password']
    phone = request.form['phone']
    email = request.form['email']
    pancard = request.form['pancard']
    ifsc = request.form['ifsc']
    aadhaar = request.form['aadhaar'] 
    address = request.form['address']

    db = db.connector()
    cursor = db.cursor(dictionary = True)

    query = ("insert into customer_management(firstname,lastname,password,phone,email,pancard,ifsc,aadhaar,address) values( %s,%s ,%s ,%s ,%s ,%s ,%s,%s,%s)")
    values = (firstname,lastname,password,phone,email,pancard,ifsc,aadhaar,address)

    cursor.execute(query,values)
    db.commit()

    return redirect('/customer_management_table')


@app.route('/customer_edit/<id>')
def customer_edit(id):
    db=db_connector()
    cursor = db.cursor(dictionary=True )

    query = 'select * from customer_management where id=%s'
    values = (id,)
    cursor.execute(query,values)

    customer = cursor.fetchone()

    return render_template('admin/customer_management/edit.html' ,customer = customer)

@app.route('/update_customer/<id>',methods=['post'])
def update_customer(id):
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    password = request.form['password']
    phone = request.form['phone']
    email = request.form['email']
    pancard = request.form['pancard']
    ifsc = request.form['ifsc']
    aadhaar = request.form['aadhaar'] 
    address = request.form['address']

    db = db_connector()
    cursor = db.cursor(dictionary = True)
    
    query = 'update customer_management set firstname=%s,lastname=%s,password=%s,phone=%s,email=%s,pancard=%s,ifsc=%s,aadhaar=%s,address=%s where id = %s'
    values = (firstname,lastname,password,phone,email,pancard,ifsc,aadhaar,address,id)
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

@app.route('/account_table')
def account_table():
    db=db_connector()
    cursor = db.cursor(dictionary = True)

    query = ('select * from accounts')
    cursor.execute(query)

    accounts = cursor.fetchall()

    return render_template('admin/account_creation/table.html',accounts = accounts)


@app.route('/account_creation')
def account_creation():

    db = db_connector()
    cursor = db.cursor(dictionary=True)

    query = "SELECT id, firstname, lastname FROM customer_management"
    cursor.execute(query)

    customers = cursor.fetchall()

    return render_template('admin/account_creation/create.html',customers=customers)

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


@app.route('/account_detail/<customer_id>')
def account_detail(customer_id):
    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = 'select c.firstname,c.lastname,c.phone,c.email,c.pancard,c.aadhaar,c.ifsc,c.address,a.account_number,a.account_type,a.balance from customer_management as c inner join accounts as a on c.id=a.customer_id where c.id =%s'
    values = (customer_id,)
    cursor.execute(query,values)

    customer = cursor.fetchone()

    return render_template('admin/account_creation/detail.html' ,customer=customer)

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

    return render_template('admin/account_creation/edit.html' ,account = account ,customer = customer)

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
    transaction_type = request.form['transaction_type']
    amount = request.form['amount']

    db=db_connector()
    cursor = db.cursor(dictionary = True)

    check_query = 'select * from accounts where account_number = %s and account_type = %s '
    check_values = (account_number,account_type)
    cursor.execute(check_query,check_values)

    check = cursor.fetchone()

    customer_id = check['customer_id']

    if check:

        query = 'insert into transaction_request(customer_id,account_number,account_type,transaction_type,amount) values (%s,%s,%s,%s,%s)'
        values = (customer_id,account_number,account_type,transaction_type,amount)
        cursor.execute(query,values)

        db.commit()

        return render_template ('customer/transaction_request.html')

    else:
        return render_template('customer/transaction_request.html', error = 'Invalid account number or account type ')

@app.route('/transaction_table')
def transaction():
    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = 'select * from transaction_request where status = 1'
    cursor.execute(query)

    transactions = cursor.fetchall()

    return render_template('admin/transaction/table.html', transactions = transactions)



@app.route('/approve_request/<id>')
def approve_request(id):
    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = 'select * from transaction_request where id = %s'
    values = (id, )
    cursor.execute(query,values)

    data = cursor.fetchone()

    amount = data['amount']

    account_number = data['account_number']

    balance_query = 'select balance from accounts where account_number = %s'
    balance_values = (account_number, )
    cursor.execute(balance_query,balance_values)

    account =cursor.fetchone()

    balance = account['balance']

    wallet_query = 'select * from bank_wallet'
    cursor.execute(wallet_query)

    bank_wallet = cursor.fetchone()

    wallet_id = bank_wallet['id']
    wallet = bank_wallet['wallet']

    commission_query = 'select * from commission'
    cursor.execute(commission_query)

    commission = cursor.fetchone()

    percentage = commission['percentage']
    flat = commission['flat']

    if data['transaction_type'] == 'withdraw' :
        balance = balance - amount

        if percentage != 0 :
            per_amount = amount * (percentage / 100)
            wallet += per_amount

        if flat !=0 :
            flat_amount = amount - flat
            wallet += flat
    elif data['transaction_type'] == 'deposite':
        balance = balance + amount
        if wallet >= amount:
             wallet -= amount

    update_query = 'update accounts set balance = %s where account_number = %s'
    update_values = (balance,account_number)
    cursor.execute(update_query,update_values)

    approve = 2
    status_query = 'update transaction_request set approvel_status=%s where id=%s'
    status_values = (approve,id)
    cursor.execute(status_query,status_values)

    add_query = 'update bank_wallet set wallet = %s where id=%s'
    add_values = (wallet,wallet_id) 
    cursor.execute(add_query,add_values)

    db.commit()

    return redirect('/transaction_table')
        
@app.route('/denied_request/<id>')
def denied_request(id):
    db = db_connector()
    cursor = db.cursor()
    denied = 3
    query = 'update transaction_request set approvel_status = %s  where id = %s'
    values = (denied,id)
    cursor.execute(query,values)

    db.commit()

    return redirect('/transaction_table')

@app.route('/commission_index',methods = ['post'])
def commission_index():
    percentage = request.form['percentage_value']
    flat = request.form['flat_value']

    db = db_connector()
    cursor = db.cursor(dictionary = True)

    query = 'select * from commission'
    cursor.execute(query)

    
    select = cursor.fetchone()
    print(select)

    value = 0


    if not select:       
        if percentage:
            new_per_query = 'insert into commission(percentage) values(%s)'
            new_per_values = (percentage,)
            cursor.execute(new_per_query,new_per_values)

        if flat:
            new_flat_query = 'insert into commission(flat) values(%s)'
            new_flat_values = (flat,)
            cursor.execute(new_flat_query,new_flat_values)

    else :
        id = select['id']

        if percentage:
            per_query = 'update commission set percentage = %s, flat = %s where id = %s'
            per_values = (percentage,value,id)
            cursor.execute(per_query,per_values)

        if flat:
            flat_query = 'update commission set flat = %s ,percentage = %s where id =%s'
            flat_values = (flat,value,id)
            cursor.execute(flat_query,flat_values)


    db.commit()

    return redirect('/commission')

@app.route('/customer_transaction')
def customer_transaction():
    db = db_connector()
    cursor = db.cursor(dictionary = True)

    id = session['id']

    query = 'select * from accounts where customer_id =%s'
    values = (id,)
    cursor.execute(query,values)

    account = cursor.fetchone()

    account_number = account['account_number']

    check_query = 'select * from transaction_request where account_number = %s'
    check_value = (account_number,)
    cursor.execute(check_query,check_value)

    transactions = cursor.fetchall()

    return render_template('customer/transaction.html', transactions = transactions)

if __name__ == '__main__':
    app.run(debug=True)
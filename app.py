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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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
        return redirect ('/dashboard')


if __name__ == '__main__':
    app.run(debug=True)
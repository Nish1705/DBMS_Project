from flask import Flask,request,redirect,url_for, render_template
from flask_mysqldb import MySQL





app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] ='user'

mysql = MySQL(app=app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('TestFrontend.html')

@app.route('/registerRes')
def backtoreg():
    return redirect(url_for('signup'))


@app.route('/registerRes', methods=['POST', 'GET'])

def login():
    username       = request.form['user']
    email          = request.form['email']
    password       = request.form['pswd']

    # TODO: save the registration data to a database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `test1` (Username, Password, Email) VALUES (%s, %s, %s);",(username,password,email))

    mysql.connection.commit()

    # cur.execute("SELECT * `test1` (Username, Password, Email) VALUES (%s, %s, %s);",(username,password,email))

    return "Registration Successful"

@app.route('/recipients', methods=['POST', 'GET'])
def recipients():
    cur = mysql.connection.cursor()
    cur.execute("select * from test1")
    record = cur.fetchall()
    
        


    return render_template('recipients.html',record=record)

if __name__ == '__main__':
    app.run(debug = True)

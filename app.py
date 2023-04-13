from flask import Flask,request,redirect,url_for, render_template,flash
from flask_mysqldb import MySQL





app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] ='user'

mysql = MySQL(app=app)
# hello

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerRes', methods=['POST', 'GET'])
def registration():
    name       = request.form['name']
    address       = request.form['address']
    email          = request.form['email']
    contact       = request.form['contact']
    username       = request.form['username']
    password       = request.form['pswd']

    # TODO: save the registration data to a database
    cur = mysql.connection.cursor()
    cur.execute("select username from recipients;")
    x = cur.fetchall()
    flag=0
    
    for i in x:
        if(i[0]==username):
            flag=1
        else:
            continue
    if(flag==0):
        cur.execute("INSERT INTO `recipients` (name,address,email,contact,username, password) VALUES (%s, %s, %s,%s, %s, %s)",(name,address,email,contact,username,password))
    else:
        return flash("Username Taken Try something else",category=Warning)
    mysql.connection.commit()
    cur.close()
    # cur.execute("SELECT * `test1` (Username, Password, Email) VALUES (%s, %s, %s);",(username,password,email))

    return redirect(url_for('register'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('TestFrontend.html')

# @app.route('/registerRes')
# def backtoreg():
#     return redirect(url_for('signup'))


@app.route('/loginRes', methods=['POST'])

def login():
    username       = request.form['user']
    password       = request.form['pswd']
    # TODO: save the registration data to a database
    cur = mysql.connection.cursor()

    sql = "SELECT password from recipients where username = %s"
    cur.execute(sql, (username,))
    record = cur.fetchall()
    cur.close()

    if(password==record[0][0]):
        return "Login Successful"
    else:
        return "Login Failed"
    


    




    # cur.execute("INSERT INTO `test1` (Username, Password, Email) VALUES (%s, %s, %s);",(username,password,email))

    # mysql.connection.commit()

    # # cur.execute("SELECT * `test1` (Username, Password, Email) VALUES (%s, %s, %s);",(username,password,email))

    # return "Registration Successful"

@app.route('/recipients', methods=['POST', 'GET'])
def recipients():
    cur = mysql.connection.cursor()
    cur.execute("select * from recipients")
    record = cur.fetchall()
    cur.close()

    return render_template('recipients.html',record=record)












if __name__ == '__main__':
    app.run(debug = True)

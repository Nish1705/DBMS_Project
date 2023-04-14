from flask import Flask,request,redirect,url_for, render_template,flash,session
from flask_mysqldb import MySQL





app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] ='user'
app.config['SECRET_KEY']='mykey'
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
    type       = request.form['type']
    username       = request.form['username']
    password       = request.form['pswd']

    # TODO: save the registration data to a database
    cur = mysql.connection.cursor()
    cur.execute("create database if not exists `user`")
    cur.execute("create table if not exists `recipients` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `type` varchar(30) not null, `username` varchar(20) primary key, `password` varchar(20) not null)")
    cur.execute("create table if not exists `donors` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `type` varchar(30) not null, `username` varchar(20) primary key, `password` varchar(20) not null)")
    cur.execute("select username from recipients")
    x = cur.fetchall()
    flag=False
    for i in x:
        if(str(i[0]).lower()==username.lower()):
            flag=True
        else:
            continue
    cur.execute("select username from donors")
    y = cur.fetchall()
    
    for i in y:
        if(str(i[0]).lower()==username.lower()):
            flag=True
        else:
            continue

    if(flag==False):
        if (type.lower() == 'recipient'):
            cur.execute("INSERT INTO `recipients` (name,address,email,contact,type,username, password) VALUES (%s, %s, %s,%s, %s, %s, %s)",(name,address,email,contact, type, username,password))
        elif (type.lower() == 'donor'):
            cur.execute("INSERT INTO `donors` (name,address,email,contact,type,username, password) VALUES (%s, %s, %s,%s, %s, %s, %s)",(name,address,email,contact, type, username,password))
        else:
            flash("Please Enter Correct Type of User(Donor or Recipient)")
    else:
        flash("Username Taken Try something else")
        # return redirect(url_for('register'))
    mysql.connection.commit()
    cur.close()
    # cur.execute("SELECT * `test1` (Username, Password, Email) VALUES (%s, %s, %s);",(username,password,email))

    return render_template('register.html',name=name,username="",email=email,contact=contact,type = type,address=address,flag=flag)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('register.html')

@app.route('/signin')
def signin():
    return render_template('login.html')


# @app.route('/registerRes')
# def backtoreg():
#     return redirect(url_for('signup'))

'''Recipients Section starts'''

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        name       = request.form['name']
        address       = request.form['address']
        email          = request.form['email']
        contact       = int(request.form['phnumber'])
        type = 'Recipient'
        username       = request.form['username']
        password       = request.form['pswd']
        cur = mysql.connection.cursor()
        cur.execute("create database if not exists `user`")
        cur.execute("create table if not exists `recipients` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `type` varchar(30) not null,`username` varchar(20) primary key, `password` varchar(20) not null)")
        
        cur.execute("select username from recipients")
        x = cur.fetchall()
        flag=False
        
        for i in x:
            if(str(i[0]).lower()==username.lower()):
                flag=True
            else:
                continue
        cur.execute("select username from donors")
        y = cur.fetchall()
    
        for i in y:
            if(str(i[0]).lower()==username.lower()):
                flag=True
            else:
                continue
        if(flag==False):
            cur.execute("INSERT INTO `recipients` (name,address,email,contact,type,username, password) VALUES (%s, %s, %s, %s,%s, %s, %s)",(name,address,email,contact,type,username,password))
        else:
            flash("Username Taken Try something else")
            # return redirect(url_for('register'))
        mysql.connection.commit()
        cur.close()
        
    return redirect(url_for('recipients'))

@app.route('/edit', methods= ['POST','GET'])
def edit():
    if request.method == 'POST':
        username = request.form['id']
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("update recipients set name=%s,email=%s,contact = %s,address=%s where username=%s",(name,email,contact,address,username))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('recipients'))



# @app.route('/edit', methods= ['POST','GET'])
# def edit():
#     if request.method == 'POST':
#         username = request.form['id']
#         name = request.form['name']
#         email = request.form['email']
#         contact = request.form['contact']
#         address = request.form['address']

#         cur = mysql.connection.cursor()
#         cur.execute("update recipients set name=%s,email=%s,contact = %s,address=%s where username=%s",(name,email,contact,address,username))
#         mysql.connection.commit()
#         cur.close()

#         return redirect(url_for('recipients'))



@app.route('/loginRes', methods=['POST'])
def login():
    username       = request.form['user']
    password       = request.form['pswd']
    # TODO: save the registration data to a database
    cur = mysql.connection.cursor()
    cur.execute("create database if not exists `user`")

    cur.execute("create table if not exists `recipients` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `username` varchar(20) primary key, `password` varchar(20) not null)")
     
    sql = "SELECT password from recipients where username = %s"
    cur.execute(sql, (username,))
    record = cur.fetchall()
    if(len(record)==0):
        flash("User doesn't exist!\nPlease enter Correct Username")
        return redirect(url_for('signin'))
    if(password==record[0][0]):
    
        cur.execute("create table if not exists `logs` (`username` varchar(20) primary key, `password` varchar(20) not null)")
        cur.execute("INSERT INTO `logs` VALUES (%s, %s);",(username,password))

        flash("Successfully Logged in")
        return  redirect(url_for('index'))

    else:
        flash("Login Failed! Access Denied.")
        return redirect(url_for('signin'))

    # mysql.connection.commit()

    # # cur.execute("SELECT * `test1` (Username, Password, Email) VALUES (%s, %s, %s);",(username,password,email))


@app.route('/recipients', methods=['POST', 'GET'])
def recipients():
    cur = mysql.connection.cursor()
    cur.execute("create database if not exists `user`")

    cur.execute("create table if not exists `recipients` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `username` varchar(20) primary key, `password` varchar(20) not null)")

    cur.execute("select * from recipients")
    record = cur.fetchall()
    cur.close()

    return render_template('recipients.html',record=record)


@app.route('/delete/<string:username_data>', methods=['GET'])
def delete(username_data):

    cur = mysql.connection.cursor()

    cur.execute("delete from recipients where username=%s",(username_data,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('recipients'))



'''Recipient section ends'''



'''Donor section starts'''


@app.route('/insertdonor', methods = ['POST'])
def insertdonor():
    if request.method == "POST":
        name       = request.form['name']
        address       = request.form['address']
        email          = request.form['email']
        contact       = int(request.form['phnumber'])
        type =          'Donor'
        username       = request.form['username']
        password       = request.form['pswd']
        cur = mysql.connection.cursor()
        cur.execute("create database if not exists `user`")
        cur.execute("create table if not exists `donors` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `type` varchar(30) not null,`username` varchar(20) primary key, `password` varchar(20) not null)")
        
        cur.execute("select username from donors")
        x = cur.fetchall()
        flag=False
        
        for i in x:
            if(str(i[0]).lower()==username.lower()):
                flag=True
            else:
                continue

        cur.execute("select username from recipients")

        y = cur.fetchall()
        
        for i in y:
            if(str(i[0]).lower()==username.lower()):
                flag=True
            else:
                continue



        if(flag==False):
            cur.execute("INSERT INTO `donors` (name,address,email,contact,type,username, password) VALUES (%s, %s, %s, %s,%s, %s, %s)",(name,address,email,contact,type,username,password))
        else:
            flash("Username Taken Try something else")
            # return redirect(url_for('register'))
        mysql.connection.commit()
        cur.close()
        
    return redirect(url_for('donors'))



@app.route('/deletedonors/<string:username_data>', methods=['GET'])
def deletedonors(username_data):

    cur = mysql.connection.cursor()

    cur.execute("delete from donors where username=%s",(username_data,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('donors'))

@app.route('/donors', methods = ['POST', 'GET'])
def donors():
    cur = mysql.connection.cursor()
    cur.execute("create database if not exists `user`")

    cur.execute("create table if not exists `donors` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `username` varchar(20) primary key, `password` varchar(20) not null)")

    cur.execute("select * from donors")
    record = cur.fetchall()
    cur.close()

    return render_template('donors.html',record=record)


@app.route('/editdonors', methods= ['POST','GET'])
def editdonors():
    if request.method == 'POST':
        username = request.form['id']
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("update donors set name=%s,email=%s,contact = %s,address=%s where username=%s",(name,email,contact,address,username))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('donors'))


'''Donor section ends'''




if __name__ == '__main__':
    app.run(debug = True)
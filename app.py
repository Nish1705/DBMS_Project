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
    cur.execute("create table if not exists `recipients` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `username` varchar(20) primary key, `password` varchar(20) not null)")

    cur.execute("select username,email from recipients;")
    x = cur.fetchall()
    flag=False
    sameemail=False
    cur.execute("create table if not exists `recipients` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `type` varchar(30) not null, `username` varchar(20) primary key, `password` varchar(20) not null)")
    cur.execute("create table if not exists `donors` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `type` varchar(30) not null, `username` varchar(20) primary key, `password` varchar(20) not null)")
    cur.execute("select username,email from recipients")
    x = cur.fetchall()
    cur.execute("select username,email from donors")
    y = cur.fetchall()
    flag=False
    sameemail=False
    for i in x:
        if(str(i[0]).lower()==username.lower() or str(i[1]).lower()==email.lower()):
            if(str(i[0]).lower()==username.lower()):

                flag=True
                break
            else:
                sameemail=True
                break
        else:
            continue
    for i in y:
        if(str(i[0]).lower()==username.lower() or str(i[1]).lower()==email.lower()):
            if(str(i[0]).lower()==username.lower()):

                flag=True
                break
            else:
                sameemail=True
                break
        else:
            continue
 

    if(flag==False):
        if(sameemail):
            flash("You have already an existing account by this email! ")
            flash("Try logging in or use another email to register! ")
        else:

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
def home():
    cur = mysql.connection.cursor()
    cur.execute("create database if not exists `user`")








    #----------------------------------------TABLES-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    
    cur.execute("create table if not exists `donors` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `type` varchar(30) not null, `username` varchar(20) primary key, `password` varchar(20) not null)")
    cur.execute("create table if not exists `recipients` (`name` varchar(30) not null, `address` varchar(30) not null, `email` varchar(30) unique not null, `contact` varchar(10) not null, `type` varchar(30) not null, `username` varchar(20) primary key, `password` varchar(20) not null)")
    cur.execute("create table if not exists `all_users` (`user_id` int AUTO_INCREMENT primary key, `username` varchar(20) not null unique, `password` varchar(20) not null, `email` varchar(30) unique, `type` varchar(30))")
    cur.execute("create table if not exists `logs` (`username` varchar(20) , `password` varchar(20) not null, `type` varchar(30),`login_date` DATE DEFAULT CURRENT_DATE())")

    cur.execute("create table if not exists food_items (food_category varchar(20) primary key, quantity int check (quantity <= 100))")
    sql_requests = '''CREATE TABLE IF NOT EXISTS `requests` (
                      request_id INT AUTO_INCREMENT PRIMARY KEY,
                      username VARCHAR(20) NOT NULL,
                      food_category VARCHAR(20) NOT NULL,
                      quantity INT,
                      title VARCHAR(40),
                      request_date DATE DEFAULT CURRENT_DATE(),
                      remarks VARCHAR(50),
                      status VARCHAR(10),
                      FOREIGN KEY (username) REFERENCES recipients(username),
                      FOREIGN KEY (food_category) REFERENCES food_items(food_category)
    )         
    '''
    cur.execute(sql_requests)
    sql_donations = '''CREATE TABLE IF NOT EXISTS donations (
                        donation_id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(20) NOT NULL,
                        food_category VARCHAR(20) NOT NULL,
                        quantity INT,
                        title VARCHAR(40),
                        description VARCHAR(70),
                        donation_date DATE DEFAULT CURRENT_DATE(),
                        pickup VARCHAR(30),
                        remarks VARCHAR(50),
                        FOREIGN KEY (username) REFERENCES donors(username),
                        FOREIGN KEY (food_category) REFERENCES food_items(food_category)
                        )'''
    
    # -------------------------------------------TABLES END----------------------------------------------------

   
   
   
   
   
   
   
   
   
    #----------------------------------------TRIGGERS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    cur.execute(sql_donations)
    sql = '''CREATE TRIGGER if not exists add_user_after_insertdonors
                AFTER INSERT ON donors
                FOR EACH ROW
                BEGIN
                    INSERT INTO all_users (username, password,email,type)
                    VALUES (NEW.username, NEW.password, NEW.email, 'Donor');
                END;'''
    cur.execute(sql)
    mysql.connection.commit()
    cur.close()
    cur = mysql.connection.cursor()
    sql_recipient = '''CREATE TRIGGER if not exists add_user_after_insertrecipients
                        AFTER INSERT ON recipients
                        FOR EACH ROW
                        BEGIN
                            INSERT INTO all_users (username, password,email,type)
                            VALUES (NEW.username, NEW.password, NEW.email, 'Recipient');
                        END;'''
    cur.execute(sql_recipient)
    mysql.connection.commit()
    

    sql_before_delete = '''CREATE TRIGGER if not exists delete_donor_trigger
                            BEFORE DELETE ON donors
                            FOR EACH ROW 
                            BEGIN
                            DELETE FROM all_users WHERE username = OLD.username;
                            END;'''
    cur.execute(sql_before_delete)

    mysql.connection.commit()
    sql_after_delete = '''CREATE TRIGGER if not exists delete_recipient_trigger
                            AFTER DELETE ON recipients
                            FOR EACH ROW 
                            BEGIN
                                DELETE FROM all_users WHERE username = OLD.username;
                            END;'''
    
    
    cur.execute(sql_after_delete)
    mysql.connection.commit()

    sql_after_update_rec = '''CREATE OR REPLACE TRIGGER update_recipient_trigger
                            AFTER UPDATE ON recipients
                            FOR EACH ROW 
                            BEGIN
                                UPDATE all_users 
                                SET email = NEW.email
                                WHERE username = OLD.username
                                
                                ;
                            END;'''
    
    
    cur.execute(sql_after_update_rec)
    mysql.connection.commit()

    sql_after_update_don = '''
                            CREATE OR REPLACE TRIGGER update_donor_trigger
                            AFTER UPDATE ON donors
                            FOR EACH ROW 
                            BEGIN
                                UPDATE all_users 
                                SET email = NEW.email
                                WHERE username = OLD.username;
                            END;
                            '''
    

    
    
    cur.execute(sql_after_update_don)
    mysql.connection.commit()


    sql_before_insert_donations = '''CREATE OR REPLACE TRIGGER `before_insert_donations` BEFORE INSERT ON `donations` FOR EACH ROW BEGIN DECLARE total_qty INT; SELECT quantity INTO total_qty FROM food_items WHERE food_category = NEW.food_category; IF (NEW.quantity + total_qty) > 100 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Donation quantity cannot exceed 100 units for this food category.'; END IF; END'''
    cur.execute(sql_before_insert_donations)
    mysql.connection.commit()

    sql_before_insert_requests = '''
CREATE OR REPLACE TRIGGER `before_insert_requests_trigger` BEFORE INSERT ON `requests`
 FOR EACH ROW BEGIN
    DECLARE request_status VARCHAR(20);
    
    SET request_status = check_request_status(NEW.food_category, NEW.quantity);
    
    SET NEW.status = request_status;
END
'''
    cur.execute(sql_before_insert_requests)
    mysql.connection.commit()

    sql_update_food_items_after_donation = '''CREATE OR REPLACE TRIGGER update_food_items_quantity_after_donation AFTER INSERT ON donations
                                                FOR EACH ROW
                                                BEGIN
                                                    UPDATE food_items
                                                    SET quantity = quantity + NEW.quantity
                                                    WHERE food_category = NEW.food_category;
                                                END;'''
    
    cur.execute(sql_update_food_items_after_donation)
    mysql.connection.commit()


# -----------------------------------------TRIGGERS END----------------------------------------------------------------------------------------
















# ---------------------------------------PROCEDURES START---------------------------------------------------------------------------------------------------

    procedure1='''
CREATE OR REPLACE PROCEDURE `process_requests`()
BEGIN
  DECLARE done INT DEFAULT 0;
  DECLARE foodCat VARCHAR(20);
  DECLARE requestedQuantity INT;
  DECLARE foodQuantity INT;
  DECLARE id INT;
  DECLARE cur CURSOR FOR SELECT request_id,food_category, quantity FROM requests WHERE status <> 'Completed';
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
  
  START TRANSACTION;
  

  OPEN cur;
  
  read_loop: LOOP
    FETCH cur INTO id,foodCat,requestedQuantity;
    IF done THEN
      LEAVE read_loop;
    END IF;
    
    SELECT quantity INTO foodQuantity FROM food_items WHERE food_category = foodCat;
    
   
    IF foodQuantity >= requestedQuantity THEN
      UPDATE food_items SET quantity = foodQuantity - requestedQuantity WHERE food_category = foodCat;
      UPDATE requests SET status = 'Completed' WHERE food_category = foodCat AND request_id=id;
      
    ELSE

      UPDATE requests SET status = 'Pending' WHERE food_category = foodCat AND request_id=id;
    END IF;
  END LOOP;
  
  CLOSE cur; COMMIT;

END
'''

    cur.execute(procedure1)
    mysql.connection.commit()

    procedure2 = '''
    CREATE OR REPLACE PROCEDURE insert_food_items()
BEGIN
    -- Check if the food items already exist
    IF NOT EXISTS(SELECT * FROM food_items WHERE food_category IN ('canned', 'produce', 'meat', 'dairy', 'grains')) THEN
        -- Insert the new rows
        INSERT INTO food_items (food_category, quantity) VALUES ('canned', 0), ('produce', 0), ('meat', 0), ('dairy', 0), ('grains', 0);
    END IF;
END;
'''
    cur.execute(procedure2)
    mysql.connection.commit()


    procedure3 = '''CREATE OR REPLACE PROCEDURE `count_donors_recipients`(
    OUT total_donors INT,
    OUT total_recipients INT
)
BEGIN
    DECLARE done BOOLEAN DEFAULT FALSE;
    
    DECLARE current_type VARCHAR(20);
    DECLARE donor_count INT DEFAULT 0;
    DECLARE recipient_count INT DEFAULT 0;
    DECLARE cur CURSOR FOR SELECT type FROM all_users;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO current_type;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        IF current_type = 'donor' THEN
            SET donor_count = donor_count + 1;
        ELSEIF current_type = 'recipient' THEN
            SET recipient_count = recipient_count + 1;
        END IF;
        
    END LOOP;
    
    CLOSE cur;
    
    SET total_donors = donor_count;
    SET total_recipients = recipient_count;
    
    COMMIT;
END'''


    cur.execute(procedure3)
    mysql.connection.commit()


    procedure4 = '''CREATE OR REPLACE PROCEDURE `insert_request`(
    IN p_username VARCHAR(20),
    IN p_food_cat VARCHAR(20),
    IN p_quant INT,
    IN p_title VARCHAR(40),
    IN p_remarks VARCHAR(50)
)
BEGIN
    INSERT INTO `requests` (
        `username`,
        `food_category`,
        `quantity`,
        `title`,
        `remarks`
    ) VALUES (
        p_username,
        p_food_cat,
        p_quant,
        p_title,
        p_remarks
    );
END'''


    cur.execute(procedure4)
    mysql.connection.commit()


    procedure5 = '''CREATE OR REPLACE PROCEDURE insert_donation (
  IN p_username VARCHAR(20),
  IN p_food_category VARCHAR(20),
  IN p_quantity INT,
  IN p_title VARCHAR(40),
  IN p_description VARCHAR(70),
  IN p_pickup VARCHAR(30),
  IN p_remarks VARCHAR(50)
)
BEGIN
  INSERT INTO `donations` (username, food_category, quantity, title, description, pickup, remarks) 
  VALUES (p_username, p_food_category, p_quantity, p_title, p_description, p_pickup, p_remarks);
END'''


    cur.execute(procedure5)
    mysql.connection.commit()
# ----------------------------------PROCEDURES END-------------------------------------------------------------













# =================================FUNCTIONS START-------------------------------------------------------------

    check_request_status = '''
CREATE OR REPLACE FUNCTION `check_request_status`(p_food_category VARCHAR(255), p_quantity INT) RETURNS varchar(20) CHARSET utf8mb4 COLLATE utf8mb4_general_ci
BEGIN
    DECLARE total_qty INT;
    DECLARE request_status VARCHAR(20);
    
    SELECT quantity INTO total_qty FROM food_items WHERE food_category = p_food_category;
    
    IF (p_quantity >= total_qty) THEN
        SET request_status = 'Pending';
    ELSE
        SET request_status = 'Completed';
        UPDATE food_items SET quantity = total_qty - p_quantity WHERE food_category = p_food_category;
    END IF;
    
    RETURN request_status;
END
    '''
    cur.execute(check_request_status)
    mysql.connection.commit()

    max_donations_function='''CREATE OR REPLACE FUNCTION max_donations() RETURNS VARCHAR(30)
BEGIN
    DECLARE max_username VARCHAR(20);
    DECLARE max_donations INT;
    DECLARE max_name VARCHAR(30);
    
    SELECT username, SUM(quantity) INTO max_username, max_donations
    FROM donations
    GROUP BY username
    ORDER BY max_donations DESC
    LIMIT 1;
    
    SELECT name INTO max_name
    FROM donors
    WHERE username = max_username;
    
    RETURN max_name;
END'''
    cur.execute(max_donations_function)
    mysql.connection.commit()

    max_donation_by_category_function = '''CREATE OR REPLACE FUNCTION `top_donations_by_category`(`category` VARCHAR(20)) RETURNS int(11)
BEGIN
  DECLARE donor_name VARCHAR(20);
  DECLARE total_donations INT DEFAULT 0;
  DECLARE done BOOLEAN DEFAULT FALSE;
  DECLARE cur CURSOR FOR SELECT username FROM donors;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
  
  CREATE TEMPORARY TABLE IF NOT EXISTS temp_table (username VARCHAR(20), total_donated INT);
  
  OPEN cur;
  read_loop: LOOP
    FETCH cur INTO donor_name;
    IF done THEN
      LEAVE read_loop;
    END IF;
    
    INSERT INTO temp_table (username, total_donated)
    SELECT username, SUM(quantity)
    FROM donations
    WHERE username = donor_name AND food_category = category
    GROUP BY username;
    
    SELECT SUM(total_donated) INTO total_donations FROM temp_table;
    
  END LOOP;
  
  CLOSE cur;
  

  
  RETURN total_donations;
END'''

    cur.execute(max_donation_by_category_function)
    mysql.connection.commit()

    max_donor_by_category_function='''
CREATE OR REPLACE FUNCTION `max_donations_by_category_donor_username`(`category_name` VARCHAR(20)) RETURNS varchar(20) CHARSET utf8mb4 COLLATE utf8mb4_general_ci
BEGIN
  DECLARE max_donations INT;
  DECLARE donor_name VARCHAR(20);
  
  SELECT username, SUM(quantity) AS total_donated
  INTO donor_name, max_donations
  FROM donations
  WHERE food_category = category_name
  GROUP BY username
  ORDER BY total_donated DESC
  LIMIT 1;
  
  RETURN donor_name;
END
'''

    cur.execute(max_donor_by_category_function)
    mysql.connection.commit()

    count_complete = '''
CREATE OR REPLACE FUNCTION `completed_requests`() RETURNS INT
BEGIN
	DECLARE DONE INT;
	SELECT COUNT(*) INTO DONE FROM `requests` WHERE status='Completed';
	RETURN DONE;
END
'''
    cur.execute(count_complete)
    mysql.connection.commit()

    count_pending = '''
CREATE OR REPLACE FUNCTION `pending_requests`() RETURNS INT
BEGIN
	DECLARE DONE INT;
	SELECT COUNT(*) INTO DONE FROM `requests` WHERE status='Pending';
	RETURN DONE;
END
'''
    cur.execute(count_pending)
    mysql.connection.commit()



# ---------------------------------------FUNCTIONS END--------------------------------------------------------------------












    cur.close()
    return render_template('Landing.html')

@app.route('/admin')
def index():
    cur = mysql.connection.cursor()
    # Call the function
    cur.execute("select max_donations()")
    max_don  = cur.fetchall()
    cur.close()

    total_donors=total_recipients=0
# Call the stored procedure
    cur = mysql.connection.cursor()
    cur.callproc('count_donors_recipients',[total_donors,total_recipients])

    # Get the results from the OUT parameters
    results = cur.fetchone()
    # total_donors = results[0]
    # total_recipients = results[1]
    cur.close()
    cur = mysql.connection.cursor()

    highest_donors=[]
    cur.execute("select max_donations_by_category_donor_username(%s)",('grains',))
    try:
        a  = cur.fetchall()[0][0]
    except:
        a="No Donation Yet"
    highest_donors.append(a)
    cur.execute("select max_donations_by_category_donor_username(%s)",('produce',))
    try:
        e  = cur.fetchall()[0][0]
    except:
        e="No Donation Yet"
    cur.execute("select max_donations_by_category_donor_username(%s)",('meat',))
    try:
        d  = cur.fetchall()[0][0]
    except:
        d= "No Donation Yet"
    cur.execute("select max_donations_by_category_donor_username(%s)",('dairy',))
    try:
        c  = cur.fetchall()[0][0]
    except:
        c="No Donation Yet"
    cur.execute("select max_donations_by_category_donor_username(%s)",('canned',))
    try:
        b  = cur.fetchall()[0][0]
    except:
        b="No Donation Yet"

    # Call function to know how many requests are pending
    cur.execute("select pending_requests()")
    pending = cur.fetchall()
    # Call function to know how many requests are completed
    cur.execute("select completed_requests()")
    complete =  cur.fetchall()

    cur.close()
    
    return render_template('index.html',max_donation=max_don[0][0],a = a, b=b, c=c, d=d, e=e,pending=pending[0][0],complete=complete[0][0])

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
        
        cur.execute("select username,email from recipients")
        x = cur.fetchall()
        cur.execute("select username,email from donors")
        y = cur.fetchall()


        flag=False
        sameemail=False

        # Username duplication Prevention
        for i in x:
            if(str(i[0]).lower()==username.lower() or str(i[1]).lower()==email.lower()):
                if(str(i[0]).lower()==username.lower()):

                    flag=True
                    break
                else:
                    sameemail=True
                    break
            else:
                continue
        for i in y:
            if(str(i[0]).lower()==username.lower() or str(i[1]).lower()==email.lower()):
                if(str(i[0]).lower()==username.lower()):

                    flag=True
                    break
                else:
                    sameemail=True
                    break
            else:
                continue
        if(flag==False):
            if(sameemail):
                flash("You have already an existing account by this email! Try logging in or use another email!")
            else:    
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
        name =     request.form['name']
        email =    request.form['email']
        contact  = request.form['contact']
        address =  request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("update recipients set name=%s,email=%s,contact = %s,address=%s where username=%s",(name,email,contact,address,username))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('recipients'))





@app.route('/loginRes', methods=['POST'])
def login():
    username       = request.form['user']
    password       = request.form['pswd']
    # TODO: save the registration data to a database
    cur = mysql.connection.cursor()
     
    sql = "SELECT password,type from all_users where username = %s"
    
    cur.execute(sql, (username,))

    record = cur.fetchall()

    if(len(record)==0 ):

        flash("User doesn't exist!  Please enter Correct Username")
        return redirect(url_for('signin'))
    
    
    if(password==record[0][0]):
            
        cur.execute("INSERT INTO `logs`(username,password,type) VALUES (%s, %s,%s)",(username,password,record[0][1]))
        mysql.connection.commit()
        cur.close()

        if(record[0][1]=='Recipient'):
            flash("Successfully Logged in !!🤯")
            return  redirect(url_for('recipientdash',username=username))
        
        else:
            flash("Successfully Logged in !!🤯")
            return  redirect(url_for('donordash',username=username))

    
    elif(password != record[0][0]):
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


@app.route('/recipientdash/<string:username>')
def recipientdash(username):
    return render_template('recipientdash.html',username=username)

@app.route('/recipientprofile/<string:username_data>', methods= ['GET'])
def recipientprofile(username_data):
    cur = mysql.connection.cursor()
    sql = "select * from recipients where username = %s"
    username = (username_data, )
    cur.execute(sql, username)
    record = cur.fetchall()
    return render_template('recipientprofile.html', record = record,username=username_data)


@app.route('/editrecipientprofile', methods= ['POST','GET'])
def editrecipientprofile():
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

        return redirect(url_for('recipientprofile', username_data = username))




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
        
        cur.execute("select username,email from donors")
        x = cur.fetchall()
        cur.execute("select username,email from recipients")

        y = cur.fetchall()
        
        flag=False
        sameemail=False
        for i in x:
            if(str(i[0]).lower()==username.lower() or str(i[1]).lower()==email.lower()):
                if(str(i[0]).lower()==username.lower()):

                    flag=True
                    break
                else:
                    sameemail=True
                    break
            else:
                continue

        for i in y:
            if(str(i[0]).lower()==username.lower() or str(i[1]).lower()==email.lower()):
                if(str(i[0]).lower()==username.lower()):

                    flag=True
                    break
                else:
                    sameemail=True
                    break
            else:
                continue

        if(flag==False):
            if(sameemail):
                flash("You have already an existing account by this email! Try logging in or use another email!")

            else:
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

@app.route('/donorprofile/<string:username_data>', methods= ['GET'])
def donorprofile(username_data):
    cur = mysql.connection.cursor()
    sql = "select * from donors where username = %s"
    username = (username_data, )
    cur.execute(sql, username)
    record = cur.fetchall()
    return render_template('donorprofile.html', record = record,username=username_data)

@app.route('/editdonorprofile', methods= ['POST','GET'])
def editdonorprofile():
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

        return redirect(url_for('donorprofile', username_data = username))

'''Donor section ends'''


'''Donation section begins'''

@app.route('/donations/<string:username>')
def my_donations(username):
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT  title, quantity, food_category, donation_date FROM donations WHERE username = %s;",(username,))
    record = cur.fetchall()
    cur.close()
    return render_template('donations.html',record=record, username=username)

@app.route('/all_donations/')
def all_donations():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT  title, quantity, food_category, donation_date,username FROM donations")
    record = cur.fetchall()
    cur.close()
    return render_template('all_donations.html',record=record)



@app.route('/add_donation/<string:username_>')
def add_donations(username_):

    return render_template('add_donations.html', username = username_)

@app.route('/donordash/<string:username>')
def donordash(username):
    return render_template('donordash.html',username=username)

@app.route('/insertdonation/<string:username>', methods = ['GET', 'POST'])
def insertdonation(username):
    if request.method == 'POST':
        food_cat = request.form.get('food_cat')
        quantity = request.form.get('donate_qty')
        title =  request.form.get('donation_title')
        description = request.form.get('description')
        pickup = request.form.get('donation_pickup')
        remarks = request.form.get('donation_remarks')
        quant = (quantity,)
        cur = mysql.connection.cursor()
        try:

            cur.execute("call insert_donation(%s, %s, %s, %s, %s, %s, %s)", (username, food_cat, quant, title, description, pickup, remarks))
            cur.execute("CALL process_requests();")
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            flash(e)

        return render_template('donordash.html',username=username)





'''Donation section ends'''
'''Request Section Starts'''


@app.route('/requests/<string:username>')
def my_requests(username):
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT  title, quantity, food_category, request_date,username,status FROM requests WHERE username = %s;",(username,))
    record = cur.fetchall()
    cur.close()

    return render_template('requests.html',record=record, username=username)

@app.route('/all_requests')
def all_requests():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT  title, quantity, food_category, request_date,username,status FROM requests")
    record = cur.fetchall()
    cur.close()

    return render_template('all_requests.html',record=record)








@app.route('/add_requests/<string:username_>')
def add_requests(username_):

    return render_template('add_requests.html', username = username_)

@app.route('/insertrequest/<string:username>', methods = ['GET', 'POST'])
def insertrequest(username):
    if request.method == 'POST':
        food_cat = request.form.get('food_cat')
        quantity = request.form.get('request_qty')
        title =  request.form.get('request_title')
        remarks = request.form.get('request_remarks')
        quant = (quantity,)
        cur = mysql.connection.cursor()
        try:

            
            cur.execute("call insert_request(%s, %s, %s, %s, %s)" (username, food_cat, quant, title, remarks))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            flash(e)

        return render_template('recipientdash.html',username=username)





'''Admin Verification'''

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/adminCheck',methods=['GET','POST'])
def adminCheck():
    password       = request.form['pswd']

    if(password == 'qwertyuiop'):

        return render_template('index.html')

    else:
        flash("Wrong Password!😒 Access Denied 🥺")
        return redirect('/adminlogin')
    

'''testing avoid backtrack'''

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
'''All Users display'''

@app.route('/allusers',methods=['GET','POST'])
def allusers():
    cur = mysql.connection.cursor()
    cur.execute("select * from all_users")
    record = cur.fetchall()
    cur.close()

    return render_template('allusers.html',record=record)

@app.route('/Inventory',methods=['GET','POST'])
def inventory():
    cur = mysql.connection.cursor()
    cur.execute("select * from food_items")
    record = cur.fetchall()
    cur.close()

    return render_template('inventory.html',record=record)


if __name__ == '__main__':
    hehe=True
    app.run(debug = True)
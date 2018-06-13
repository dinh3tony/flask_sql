from flask import Flask, render_template, request, redirect, session, flash 
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt  
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = connectToMySQL('logindb')
app.secret_key="Hard"

@app.route('/')
def index():
    if "fname" not in session:
        session["fname"] = ""
    if "lname" not in session:
        session["lname"] = ""
    if "pass" not in session:
        session["pass"] = ""
    if "confirm" not in session:
        session["confirm"] = ""
    if "email" not in session:
        session["email"] = ""
    return render_template("login.html")

@app.route('/create', methods=['POST'])
def create():
    all_emails = mysql.query_db("SELECT email FROM users")
    if len(request.form["fname"]) < 1:
        flash("First name cannot be blank!",'fname')
    elif str.isalpha(request.form["fname"]) == False:
        flash("Invalid First Name, Letters Only", 'fname')
    else: 
        session["fname"] = request.form["fname"]

    if len(request.form["lname"]) < 1:
        flash("Last name cannot be blank",'lname')
    elif str.isalpha(request.form["lname"]) == False:
        flash("Invalid Last Name, Letters Only",'lname')
    else:
        session["lname"] = request.form['lname']

    if len(request.form["email"]) < 1:
        flash("Your email cannot be blank!",'email')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!",'email')
    else:
        for i in range(len(all_emails)):
            if request.form["email"] in all_emails[i]["email"]:
                flash("This email already exists", 'email')
                break
        

    if len(request.form["pass"]) < 8:
        flash("Password is not long enough!",'pass')
    else: 
        session["pass"] = request.form["pass"]

    if len(request.form["confirm"]) < 8:
        flash("Confirmation is not long enough!", 'confirm')
    else: 
        session["confirm"] = request.form["confirm"]
    



    if '_flashes' in session.keys():
        return redirect('/')
    else:
        session["email"] = request.form["email"]
        pw_hash = bcrypt.generate_password_hash(request.form['pass'])  
        flash("Congrats! You made an account!", 'success')
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email_address)s, %(password)s);"
        data = {
                'first_name': request.form['fname'],
                'last_name': request.form['lname'],
                'email_address': request.form['email'],
                'password': pw_hash
                }
        mysql.query_db(query, data)
        return redirect('/success')

@app.route('/login', methods=['POST'])
def login():
    if len(request.form["boob"]) < 1:
        flash("Your email cannot be blank!",'boob')
    elif not EMAIL_REGEX.match(request.form['boob']):
        flash("Invalid Email Address!",'boob')

    if len(request.form["chick"]) < 8:
        flash("Password is not long enough!",'chick')

    query = "SELECT id, first_name, email, password FROM users WHERE email = %(email_address)s;"
    data = { "email_address" : request.form["boob"] }
    result = mysql.query_db(query, data)
    if result:
        # print("Result of 0", result[0])
        if bcrypt.check_password_hash(result[0]['password'], request.form['chick']):
            session['userid'] = result[0]['id']
            session['fname'] = result[0]['first_name']
            session['logged.in'] = True
            return redirect('/success')
    flash("You could not be logged in. Wrong Email/Password.")
    return redirect("/")
    

@app.route('/success')
def success():
    return render_template('created.html')

@app.route('/clear')
def clear():
    session['logged.in'] = False
    session.clear()
    flash("You have been logged out")
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
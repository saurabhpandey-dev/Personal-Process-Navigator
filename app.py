from flask import Flask, render_template,request,redirect,session
from cs50 import SQL
import os

app = Flask(__name__)
app.secret_key = 'Shri Shri Shri 1008 Saurabh Prashad Ganguli Ji Maharaj' # create the session id
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")  # this line for get the path from anywhere
 
db = SQL(f'sqlite:///{db_path}')  # database add command

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# this route for calling ther user login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')

    user_exist = db.execute('select * from users where email = ?',email) # to yha pe list of dictonary return kar rha hai 
    if user_exist and len(user_exist) > 0:
        store_email = user_exist[0]['email'] # index 0 pe kyu ki ek hi dict ayi hai aur uska key hai 'email' 
        store_pass = user_exist[0]['password'] # dict ka key hai 'password'
        if store_email == email and store_pass == password:  
            session['email'] = store_email
            return render_template('dashboard.html',user = user_exist[0]) # ye se ham user ka basic data bhejenge 
    else: # if email or password mismatched got print the error 
        return render_template('login.html', error = 'Email and Password not exist') 
    


# this route for calling the user register page
@app.route('/register')
def register():
    return render_template('register.html')

# this route for get the data from register page and fatch the db and store the data into the table 
@app.route('/create_user', methods = ['POST']) # using the 'POST' method for not showing data on url
def create_user():
    name = request.form.get('name') # get the name
    email = request.form.get('email') # get the email
    number = request.form.get('phone') # get the number
    password = request.form.get('password') # get the password

    user_exist = db.execute('select * from users where email = ?',email) # sql cammand for check USER table have the email id or not
    # if the user email exist return to the register for the another try for register
    if len(user_exist)>0: 
        return render_template('register.html',error = 'Email alredy exits')
    
    # if email is not exits on the user table all values got stord
    db.execute('insert into users (name, email, phone, password) values (?, ?, ?, ?)',name,email,number,password)
    # sql cammand for insert user data to the database user table
    return render_template('login.html') # after inserting data go to the login page for login

# this route for calling the process page
@app.route('/process')
def process():
    return render_template('process.html')

# this route for calling the process details page
@app.route('/process_detail')
def process_detail():
    return render_template('process_details.html')

# this route for calling the upload page
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/profile')
def profile():
    email = session.get('email')
    user_data = db.execute('SELECT * FROM users WHERE email = ?', email)
    return render_template('profile.html',user = user_data)

@app.route('/change_password',methods = ['post'])
def change_password():
    email = session['email']
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    user = db.execute('SELECT * FROM users WHERE email = ?', email)
    if not user:
        return redirect('/login')
    # 3. Check karo ki form wala old password, database wale password se match karta hai ya nahi
    if user[0]['password'] != old_password:
        return render_template('profile.html', user=user[0], error='Incorrect old password!')
    # 4. Agar sab theek hai, toh naya password update kar do
    db.execute('UPDATE users SET password = ? WHERE email = ?', new_password, email)
    # Success message ke sath profile page par bhej do
    return render_template('profile.html', user=user[0], success='Password changed successfully!')

if __name__ == '__main__':
    app.run(debug=True) 
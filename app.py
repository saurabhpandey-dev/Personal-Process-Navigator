from flask import Flask, render_template,request

app = Flask(__name__)

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

# this route for calling the user register page
@app.route('/register')
def register():
    return render_template('register.html')
if __name__ == '__main__':
    app.run(debug=True) 
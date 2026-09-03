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

if __name__ == '__main__':
    app.run(debug=True) 
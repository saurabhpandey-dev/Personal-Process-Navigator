from flask import Flask, render_template,request,redirect,session,jsonify,url_for
from cs50 import SQL
import os
import google.generativeai as genai
from datetime import datetime
import uuid
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'Shri Shri Shri 1008 Saurabh Prashad Ganguli Ji Maharaj' # create the session id
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")  # this line for get the path from anywhere
BASE_VAULT_DIR = 'static/uploads/vault'

db = SQL(f'sqlite:///{db_path}')  # database add command

# Gemini API Key Configuretion  
# (apni API key yahan direct daali hai ya environment variable use kar sakte hain)
genai.configure(api_key="AAPKI_GEMINI_API_KEY_YAHAN_AAYEGI") # yha pe maine api key dali hai jo ki  'genai.configure' is funtion
# add hogi 


@app.route('/')
def index():
    return render_template('index.html')

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

# Dashboard route: Ye check karega ki user login hai ya nahi, tabhi khulega
@app.route('/dashboard',methods = ["GET",'POST'])
def dashboard():
    # Agar session me email nahi hai, matlab user ne login nahi kiya
    if 'email' not in session:
        return redirect('/login')  # Toh seedha login page par bhej do
    
    # Session se email nikal kar database se user ka saara data fetch karenge
    email = session['email']
    user_data = db.execute('SELECT * FROM users WHERE email = ?', email)
    
    # Safety check: agar user database me nahi mila toh session clear karke login par bhejo
    if not user_data:
        session.clear()
        return redirect('/login')

    # User ka data dashboard template ko bhej denge
    return render_template('dashboard.html', user=user_data[0])

# this route is for logout the user and and the session
@app.route('/logout')
def logout(): # Logout route: Session clear karke login page par bhejne ke liye
    session.clear()# Ye session ka saara data mita dega
    return redirect('/login')

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

# this is the route for the changing the password
@app.route('/change_password',methods = ['POST'])
def change_password():
    email = session['email']
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    user = db.execute('SELECT * FROM users WHERE email = ?', email)
    if user[0]['password'] != old_password:
        return render_template('profile.html', user=user[0], error='Incorrect old password!')
    # 4. Agar sab theek hai, toh naya password update kar do
    db.execute('UPDATE users SET password = ? WHERE email = ?', new_password, email)
    # Success message ke sath profile page par bhej do
    return render_template('profile.html', user=user[0], success='Password changed successfully!')


# ye function ai ko fatch karegi 
def fetch_process_data_from_ai(process_name):
    """
    Yeh ek custom function hai jo naye process ka naam input leta hai,
    Gemini AI ko request bhejta hai, aur wahan se JSON data nikal kar return karta hai.
    """
    
    # Gemini ka sabse fast aur text-based tasks ke liye behtareen model select kiya ja raha hai.
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Yahan hum AI ko strict instructions (prompt) de rahe hain ki hame data kis format me chahiye.
    #PROMPT for the search actual data
    prompt = f"""
    You are an expert government compliance and documentation assistant. 
    Provide the details for the process: "{process_name}".
    
    You MUST return the response strictly as a valid JSON object with the following keys and structure:
    {{
      "process_name": "{process_name}",
      "description": "A short 1-2 line description of what this process is.",
      "category": "Choose one: Government, Financial, Legal, or Student",
      "total_steps": 3,
      "requirements": [
        {{"name": "Document Name 1", "description": "Short description of why it is needed"}},
        {{"name": "Document Name 2", "description": "Short description"}}
      ]
    }}
    Do not include any extra text, markdown formatting like ```json, or explanation outside the JSON.
    """
    
    # try-except block ka use error handling ke liye kiya jata hai taaki 
    # agar internet ya API me koi dikkat aaye toh app crash na ho.
    try:
        # model.generate_content() prompt ko AI ke paas bhejta hai aur response generate karta hai.
        response = model.generate_content(prompt)
        
        # response.text se AI ka diya hua text nikalte hain aur .strip() se aage-piche ke extra spaces hata dete hain.
        text_response = response.text.strip()
        
        # Agar AI galti se markdown formatting (jaise ```json ... ```) laga de, toh hum use slice karke saaf kar dete hain.
        if text_response.startswith("```json"):
            text_response = text_response[7:-3].strip()
        elif text_response.startswith("```"):
            text_response = text_response[3:-3].strip()
            
        # json.loads() text/string ko Python Dictionary me badal deta hai taaki hum keys ke zariye data access kar sakein.
        data = json.loads(text_response)
        
        # Parsed data ko function ke bahar return kar dete hain.
        return data
        
    except Exception as e:
        # Agar koi bhi error aata hai (jaise internet nahi hai ya AI down hai), toh yeh block chalega.
        print(f"AI Error: {e}")
        
        # Fallback data: Agar AI fail ho jaye, toh app ko chalane ke liye ek default dictionary return kar dete hain.
        return {
            "process_name": process_name,
            "description": f"Standard workflow for {process_name}.",
            "category": "General",
            "total_steps": 3,
            "requirements": [
                {"name": "Identity Proof", "description": "Standard ID document"},
                {"name": "Application Form", "description": "Filled form"}
            ]
        }

# this is route for the search process and create the new process
@app.route('/search_or_create_process', methods = ['POST'])
def search_or_create_process():
    process_name = request.form.get('process_name','').strip()

    # agar user ne bina likhe search button bda diya to process_list pe chala jaiga
    if not process_name:
        return redirect(url_for('process'))
    
    # Database me check kar rahe hain ki kya yeh process pehle se database me maujood hai ya nahi.
    existing = db.execute('select * from processes where lower(name) like ?', ('%' + process_name.lower() + '%',))
    # lower(name) ka use isliye kiya hai taaki uppercase/lowercase ki koi problem na ho.

    if existing: # Agar database me process pehle se mil jata hai
        # naya AI call karne ki zaroorat nahi hai seedha purane process ki ID utha kar uske detail page par redirect kar dega
        return render_template('process_details.html',process_id=existing[0]['id'])
    
    # Agar process database me nahi mila, toh upar banaye gaye 
    # function ko call karke Gemini AI api se naya data fetch karo.
    ai_generated_data = fetch_process_data_from_ai(process_name)

    # AI se mile hue data ko main 'processes' table me insert karna
    
    new_process_id  = db.execute(
        "INSERT INTO processes (name, description, category, total_steps) VALUES (?, ?, ?, ?)",
        ai_generated_data['process_name'], ai_generated_data['description'], ai_generated_data['category'], ai_generated_data['total_steps']
    )
    
    # AI dwara diye gaye saare required documents par ek loop chala rahe hain taaki unhe ek-ek karke save kiya ja sake.
    for req in ai_generated_data['requirements']:
        # Har ek document ko 'process_requirements' table me insert kar rahe hain, jiska relation upar wali process ID se hai.
        db.execute(
            "INSERT INTO process_requirements (process_id, document_name, description, is_required) VALUES (?, ?, ?, ?)",
            new_process_id, req['name'], req['description'], 1
        )
                   
    # Sabhi cheezein database me successfully save hone ke baad, user ko seedha naye process ke detail page par redirect kar do.
    return render_template('process_details.html', process_id=new_process_id)
    

# this route for save the dacument in the saperate folder    
@app.route('/upload_vault_doc', methods=['POST'])
def upload_vault_doc():
    # 1. Current logged-in user ki ID session se nikalna
    user_id = session.get('user_id', 1) 
    
    # 2. Database se us user ki details (name, email) lena taaki folder name me use kar sakein
    user_data = db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
    if not user_data:
        return redirect(url_for('login'))
        
    user = user_data[0]
    
    # Folder name ke liye safe string banana (jaise: 1_rahul@gmail.com_rahul_kumar)
    safe_email = user['email'].strip().lower().replace('@', '_at_').replace('.', '_')
    safe_name = secure_filename(user['name'].strip().lower().replace(' ', '_'))
    user_folder_name = f"{user['id']}_{safe_email}_{safe_name}"
    
    # 3. Form se document type aur file lena
    document_type = request.form.get('document_type') # Jaise: 'Aadhaar Card'
    file = request.files.get('document_file')
    
    if not document_type or not file or file.filename == '':
        return redirect(request.referrer)
        
    # 4. Document type ka subfolder banana (jaise: 'aadhaar_card')
    safe_doc_folder = document_type.strip().lower().replace(' ', '_')
    
    # Final target folder path: static/uploads/vault/1_rahul_gmail_com_rahul/aadhaar_card/
    target_folder = os.path.join(BASE_VAULT_DIR, user_folder_name, safe_doc_folder)
    os.makedirs(target_folder, exist_ok=True)
    
    # 5. Unique filename generate karna (Timestamp + UUID)
    original_name = secure_filename(file.filename)
    ext = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else 'jpg'
    clean_base_name = secure_filename(original_name.rsplit('.', 1)[0])
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    unique_filename = f"{timestamp}_{unique_id}_{clean_base_name}.{ext}"
    
    # 6. File ko server par save karna
    full_file_path = os.path.join(target_folder, unique_filename)
    file.save(full_file_path)
    
    # Database me save karne ke liye relative path
    db_path = f"uploads/vault/{user_folder_name}/{safe_doc_folder}/{unique_filename}"
    
    # 7. Check karo kya is user ka yeh document pehle se database me hai?
    existing_record = db.execute(
        "SELECT * FROM user_vault WHERE user_id = ? AND document_type = ?", 
        (user_id, document_type)
    )
    
    if existing_record:
        # Agar pehle se hai, toh naye path se UPDATE kar do (Purani file replace ho jayegi)
        db.execute(
            "UPDATE user_vault SET file_path = ?, original_name = ?, uploaded_at = CURRENT_TIMESTAMP WHERE user_id = ? AND document_type = ?",
            (db_path, original_name, user_id, document_type)
        )
    else:
        # Agar pehli baar daal raha hai, toh INSERT kar do
        db.execute(
            "INSERT INTO user_vault (user_id, document_type, original_name, file_path) VALUES (?, ?, ?, ?)",
            (user_id, document_id if 'document_id' in locals() else None, original_name, db_path) # Adjust as per your columns
        )
        
    return redirect(request.referrer)

# Helper function jo check karega ki user ne specific document vault me upload kiya hai ya nahi
# 1. Yeh function define karein (routes ke aas-pass ya kahin bhi)
def get_user_vault_doc(user_id, document_type):
    if not user_id:
        return None
    record = db.execute(
        "SELECT * FROM user_vault WHERE user_id = ? AND document_type = ?",
        (user_id, document_type)
    )
    return record[0] if record else None

# 2. Isko Flask me global template function ke taur par register kar dein
app.add_template_global(get_user_vault_doc, 'get_user_vault_doc')

if __name__ == '__main__':
    app.run(debug=True) 
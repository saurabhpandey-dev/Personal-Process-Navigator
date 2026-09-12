from flask import Flask, render_template,request,redirect,session,jsonify,url_for
from cs50 import SQL
import os
# import google.generativeai as genai
from google import genai
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
#genai.configure(api_key="AQ.Ab8RN6Icj1Fg_MAWdE7Zv18un_u1Rhapp-_ZMz2cVbGfofUnVA") # yha pe maine api key dali hai jo ki  'genai.configure' is funtion
# add hogi 

# Genai API Key Configuretion
# client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6Icj1Fg_MAWdE7Zv18un_u1Rhapp-_ZMz2cVbGfofUnVA"))
client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6Icj1Fg_MAWdE7Zv18un_u1Rhapp-_ZMz2cVbGfofUnVA"))

@app.route('/')
def index():
    return render_template('index.html')

# this route for calling ther user login page
@app.route('/login')
def login():
    return render_template('login.html')

# this route for login the user
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
            user_id = session.get('user_id', 1)
            return render_template('dashboard.html',user = user_exist[0]) # ye se ham user ka basic data bhejenge 
    # if email or password mismatched got print the error 
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
@app.route('/process/<int:process_id>')
def process_detail(process_id):
    # Process ki details database se fetch karo
    process_list = db.execute("SELECT * FROM processes WHERE id = ?", process_id)
    if not process_list:
        return redirect(url_for('process'))
    process = process_list[0]
    
    # Is process ke saare required documents fetch karo
    requirements = db.execute("SELECT * FROM process_requirements WHERE process_id = ?", process_id)
    
    # Template render karte waqt process aur requirements dono pass karo
    return render_template('process_details.html', process=process, requirements=requirements)

# this route for calling the upload page
# Yeh route dynamic document upload page ko render karta hai. 
# URL se process_name aur doc (document type) ko capture karke template par pass karta hai.
@app.route('/upload')
def upload():
    process_name = request.args.get('process', 'General Process')
    document_type = request.args.get('doc', 'General Document')
    return render_template('upload.html', process_name=process_name, document_type=document_type)

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
    prompt = f"""
You are an expert real-world process and documentation research assistant.

The user wants to use the Personal Process Navigator application to understand and complete this process:

PROCESS NAME:
"{process_name}"

Your task is to generate a COMPLETE, PRACTICAL and REAL-WORLD representation of this process.

IMPORTANT:
- Do NOT give only 1 or 2 generic documents.
- Identify ALL commonly required documents/information that a real applicant may need.
- Include documents related to identity, address, financial information, eligibility, business/student information, photographs, forms, certificates, declarations, authorization, or other relevant requirements ONLY when actually applicable.
- Do NOT invent documents just to increase the list.
- Distinguish between mandatory and optional/supporting documents.
- Requirements may vary depending on applicant type, state, authority, organization or specific situation.
- Provide a COMPLETE step-by-step workflow.
- Do NOT limit the workflow to 3 steps.
- Usually provide around 6-12 meaningful steps.
- The steps must be logically ordered.
- The process should be understandable to a non-technical user.

DOCUMENT REQUIREMENTS:
For every relevant document provide:
- name
- description
- is_required (1 for commonly mandatory, 0 for optional/supporting)

STEP REQUIREMENTS:
For every step provide:
- step_number
- step_name
- description

RETURN ONLY VALID JSON.

Use exactly this JSON structure:

{{
    "process_name": "{process_name}",
    "description": "Short but accurate description of the process.",
    "category": "Choose the most appropriate category: Government, Financial, Legal, Student, Business, or Other",
    "requirements": [
        {{
            "name": "Document name",
            "description": "Why it is required and any important condition.",
            "is_required": 1
        }}
    ],
    "steps": [
        {{
            "step_number": 1,
            "step_name": "Step name",
            "description": "Clear explanation of what the user needs to do."
        }}
    ]
}}

QUALITY RULES:
1. Output actual requirements relevant to "{process_name}".
2. Do not use generic placeholders.
3. Do not assume every process requires Aadhaar or PAN.
4. Do not add irrelevant documents.
5. If a document is required only in a particular situation, mark it optional.
6. Include important official/application forms when applicable.
7. Include verification, submission and completion/follow-up steps.
8. Never fabricate official fees, deadlines, eligibility rules, document names or authority requirements.
9. Keep the information suitable for an educational/demo application.
10. Return JSON only.
"""

    try:
        # Naye google-genai SDK ka correct syntax
        response = client.models.generate_content(
            model='gemini-3.6-flash', # Aap gemini-2.0-flash ya gemini-1.5-flash bhi use kar sakte hain
            contents=prompt
        )

        text_response = response.text.strip()

        # Agar AI markdown code block return kare
        if text_response.startswith("```json"):
            text_response = text_response[7:-3].strip()
        elif text_response.startswith("```"):
            text_response = text_response[3:-3].strip()

        data = json.loads(text_response)
        return data

    except Exception as e:
        print(f"AI Error: {e}")
        return None
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
        process = existing[0]

        requirements = db.execute(
            'SELECT * FROM process_requirements WHERE process_id = ?',
            process['id']
        )
        return render_template('process_details.html',process=process,requirements=requirements)
    
    # Agar process database me nahi mila, toh upar banaye gaye 
    # function ko call karke Gemini AI api se naya data fetch karo.
    #  Agar process database me nahi mila,
    # toh AI se naya process data fetch karo
    ai_generated_data = fetch_process_data_from_ai(process_name)

    # Smart Fix: Steps ki ginti khud nikal lein taaki KeyError na aaye
    total_steps_count = len(ai_generated_data.get('steps', []))

    # if Ai se data nhi mila to ye pass ho jaiga 
    if not ai_generated_data:
        return render_template(
            'process.html',
            error='Process data could not be generated. Please try again.'
        )

    # AI se mile data ko processes table me insert karna
    new_process_id  = db.execute(
        "INSERT INTO processes (name, description, category, total_steps) VALUES (?, ?, ?, ?)",
        ai_generated_data['process_name'], 
        ai_generated_data['description'],
        ai_generated_data['category'], 
        total_steps_count
    )
    
    # Requirements save karna
    # AI dwara diye gaye saare required documents par ek loop chala rahe hain taaki unhe ek-ek karke save kiya ja sake.
    for req in ai_generated_data.get('requirements', []):
        # Har ek document ko 'process_requirements' table me insert kar rahe hain, jiska relation upar wali process ID se hai.
        db.execute(
            "INSERT INTO process_requirements (process_id, document_name, description, is_required) VALUES (?, ?, ?, ?)",
            new_process_id,
            req['name'],
            req['description'],
            req.get('is_required', 1)
                    )
                   
    # Steps save karna
    # jo bhi steps ai se mile hai unhe process_steps table me save karna 
    for step in ai_generated_data.get('steps', []):
        db.execute(
            """
            INSERT INTO process_steps
            (process_id, step_number, step_name, description)
            VALUES (?, ?, ?, ?)
            """,
            new_process_id,
            step['step_number'],
            step['step_name'],
            step['description']
        )

    # Sabhi cheezein database me successfully save hone ke baad, user ko seedha naye process ke detail page par redirect kar do.
    return redirect(url_for('process_detail', process_id=new_process_id))
    

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
            (user_id, document_type, original_name, db_path) 
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
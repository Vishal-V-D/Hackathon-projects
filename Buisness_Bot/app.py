from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from pymongo import MongoClient
import google.generativeai as genai
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '29581649c765e92a1aa408a1f4fb7f0c'  # Replace with your generated secret key
app.config['SESSION_TYPE'] = 'mongodb'  # Use MongoDB for session management

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
db_name = 'my_custom_db'        # Your custom database name
collection_name = 'users'       # Your custom collection name for storing user data
session_collection = 'sessions' # Collection name for storing session data

db = client[db_name]  # Connect to your custom database
app.config['SESSION_MONGODB'] = client
app.config['SESSION_MONGODB_DB'] = db_name
app.config['SESSION_MONGODB_COLLECT'] = session_collection

# Initialize session with the app
Session(app)

model = genai.GenerativeModel('gemini-pro')
genai.configure(api_key="AIzaSyAjNeEJiHqD6iCvnmThYPGDVO8-nwxF6XM")

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            prompt = request.form['prompt']
            question = prompt
            response = model.generate_content(question)

            # Store the user's question in their session
            session['last_question'] = question

            if response.text:
                return response.text
            else:
                return "Sorry, but I think Gemini didn't want to answer that!"
        except Exception as e:
            return "Sorry, but Gemini didn't want to answer that!"

    return render_template('index.html', **locals())

### Add the User Registration, Login, and Logout Code Here ###

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        if db.users.find_one({'username': username}):
            return "User already exists. Please log in."

        # Create a new user with hashed password
        hashed_password = generate_password_hash(password, method='sha256')
        db.users.insert_one({'username': username, 'password': hashed_password})

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check user credentials
        user = db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            # Store the user's username in the session
            session['username'] = username
            return redirect(url_for('index'))
      
        return "Invalid username or password. Please try again."
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove user session
    session.pop('username', None)
    return redirect(url_for('index'))

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

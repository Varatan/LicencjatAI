from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv
import os
from generation import Generator
import json
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SESSION_KEY') # Set a secret key for session management
generator = Generator()

@app.route("/")
def index():
    names_list = session.pop('names_list', [])  # Retrieve names_list from session or default to empty list
    loading = False
    return render_template("index.html", list=names_list, loading=loading)

@app.route("/generate", methods=["POST"])
def generate():
    race = request.form.get('race')
    gender = request.form.get('gender')
    print(race,' ',gender)
    names = generator.GenerateNames(race, gender)
    names_parsed = json.loads(names)
    names_list = names_parsed['names']
    session['names_list'] = names_list  # Store names_list in session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

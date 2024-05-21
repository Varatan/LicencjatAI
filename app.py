from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv
from params import params
import os
from generation import Generator
import json
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SESSION_KEY') # Set a secret key for session management
generator = Generator()

paramsNames = list(params.keys())

@app.route("/")
def redirect_to_names():
    return redirect(url_for('names_index'))

@app.route("/names")
def names_index():
    names_list = session.pop('names_list', [])  # Retrieve names_list from session or default to empty list
    loading = False
    return render_template("index.html", list=names_list, loading=loading, params=params, paramsNames=paramsNames)

@app.route("/generate", methods=["POST"])
def generate():
    race = request.form.get('race')
    gender = request.form.get('gender')
    alignment = request.form.get('alignment')
    profession = request.form.get('profession')
    tone = request.form.get('tone')
    culture = request.form.get('culture')
    lastName = request.form.get('last name')
    nickName = request.form.get('nickname')

    names = generator.GenerateNames(race, gender, alignment, profession, tone, culture, lastName, nickName)
    names_parsed = json.loads(names)
    names_list = names_parsed['names']
    session['names_list'] = names_list  # Store names_list in session
    return redirect(url_for('names_index'))

if __name__ == '__main__':
    app.run(debug=True)

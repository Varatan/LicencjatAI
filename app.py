from flask import Flask, render_template, redirect, url_for, request, session
from dotenv import load_dotenv
from datetime import datetime
from params import params
import os
import dbOps
from generation import Generator

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SESSION_KEY') # Set a secret key for session management
generator = Generator()
paramsNames = list(params.keys())
sites=['Names', 'Stats', 'Info']
currentYear = datetime.now().year

@app.route("/")
def redirect_to_names():
    return redirect(url_for('names'))

@app.route("/names")
def names():
    names_list = session.pop('names_list', []) 
    current = session.pop('current', [])
    loading = False
    currentSite = "Names"
    return render_template("names.html", list=names_list, loading=loading, params=params, paramsNames=paramsNames, current = current, sites=sites, currentSite = currentSite, currentYear=currentYear)

@app.route("/info")
def info():
    currentSite="Info"
    return render_template("info.html",sites=sites, currentSite = currentSite, currentYear=currentYear)

@app.route("/stats") # temporary
def stats():
    return redirect(url_for('names'))

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

    current = {
    'race': race,
    'gender': gender,
    'alignment':alignment,
    'profession': profession,
    'tone': tone,
    'culture': culture,
    'last name': lastName,
    'nickname': nickName
}
    
    conn = dbOps.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO requests (race, gender, alignment, profession, tone, culture, last_name, nickname)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (race, gender, alignment, profession, tone, culture, lastName, nickName))
    lastId = cursor.lastrowid
    conn.commit()
    conn.close()

    names = generator.GenerateNames(race, gender, alignment, profession, tone, culture, lastName, nickName,lastId)
    names_list = names['names']
    session['names_list'] = names_list  # Store names_list in session
    session['current'] = current



    return redirect(url_for('names'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, request, session,jsonify
from dotenv import load_dotenv
from datetime import datetime
from collections import Counter
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
    paramsNames = list(params.keys())
    names_list = session.pop('names_list', []) 
    current = session.pop('current', [])
    loading = False
    currentSite = "Names"
    return render_template("names.html", list=names_list, loading=loading, params=params, paramsNames=paramsNames, current = current, sites=sites, currentSite = currentSite, currentYear=currentYear)

@app.route("/info")
def info():
    currentSite="Info"
    return render_template("info.html",sites=sites, currentSite = currentSite, currentYear=currentYear)

@app.route("/stats")
def stats():
    currentSite="Stats"
    for i in range(len(paramsNames)):
        paramsNames[i] = paramsNames[i].capitalize()

    conn = dbOps.get_db_connection()
    cursor = conn.cursor()
    queries = cursor.execute(''f'SELECT id from requests order by id desc limit 1''').fetchone()
    names = cursor.execute(''f'SELECT id from responses order by id desc limit 1''').fetchone()
    conn.close()
    queries = queries[0]
    names = names[0]

    #print("Names: ", names," Queries: ", queries)
    return render_template("stats.html",sites=sites, currentSite = currentSite, currentYear=currentYear, paramsNames=paramsNames, names=names, queries=queries)

@app.route('/params')
def parameters():
    value = request.args.get('param').lower().replace(" ", "_")
    #print(value)
    conn = dbOps.get_db_connection()
    cursor = conn.cursor()
    requests = cursor.execute(''f'SELECT {value}, count({value}) as count FROM requests group by {value}''').fetchall()
    conn.close()
    requests_data = [dict(row) for row in requests]

    for item in requests_data:
        if item[f'{value}'] == '':
            item[f'{value}'] = 'Empty'

    #print("requests_data:", requests_data)
    valueHeader = value.capitalize()
    chart_data = [[valueHeader,'Count']]
    for row in requests_data:
        chart_data.append([row[f'{value}'], row['count']])

    return jsonify(chart_data)

@app.route("/letters")
def letters():
    race = request.args.get('race')
    print("Race: ",race)
    conn = dbOps.get_db_connection()
    cursor = conn.cursor()
    names = cursor.execute(''f'SELECT name FROM responses join requests on responses.requestID = requests.id where race = "{race}"''').fetchall()
    conn.close()
    
    names_list = [name[0] for name in names]
    print("Names list: ",names_list)
    
    # Convert all names to uppercase and concatenate them into a single string
    all_names = ''.join(names_list).upper()

    # Count occurrences of each letter
    letter_counts = Counter(all_names)

    # Prepare data as a list of tuples for Google Charts
    chart_data = [('Letter', 'Count')]  # Adding headers for Google Charts
    chart_data.extend([(letter, count) for letter, count in sorted(letter_counts.items(), key=lambda item: item[1], reverse=True) if letter not in [' ', "'", '-']])

    print("Chart data:", chart_data)
    return jsonify(chart_data)

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
    app.run(debug=True, port=12128)

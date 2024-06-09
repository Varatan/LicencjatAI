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
    namesList = session.pop('namesList', []) 
    current = session.pop('current', [])
    loading = False
    currentSite = "Names"
    return render_template("names.html", list=namesList, loading=loading, params=params, paramsNames=paramsNames, current = current, sites=sites, currentSite = currentSite, currentYear=currentYear)

@app.route("/info")
def info():
    currentSite="Info"
    return render_template("info.html",sites=sites, currentSite = currentSite, currentYear=currentYear)

@app.route("/stats")
def stats():
    currentSite="Stats"
    races = params['race']
    #print("races:", races)
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
    return render_template("stats.html",sites=sites, currentSite = currentSite, currentYear=currentYear, paramsNames=paramsNames, names=names, queries=queries, races=races)

@app.route('/params')
def parameters():
    value = request.args.get('param').lower().replace(" ", "_")
    #print(value)
    conn = dbOps.get_db_connection()
    cursor = conn.cursor()
    requests = cursor.execute(''f'SELECT {value}, count({value}) as count FROM requests group by {value}''').fetchall()
    conn.close()
    requestsData = [dict(row) for row in requests]

    for item in requestsData:
        if item[f'{value}'] == '':
            item[f'{value}'] = 'Empty'

    requestsData = sorted(requestsData, key=lambda x: x['count'], reverse=True)

    #print("requestsData:", requestsData)
    valueHeader = value.capitalize()
    chartData = [[valueHeader,'Count']]
    for row in requestsData:
        chartData.append([row[f'{value}'], row['count']])

    return jsonify(chartData)

@app.route("/letters")
def letters():
    race = request.args.get('race')
    name = request.args.get('name')
    conn = dbOps.get_db_connection()
    cursor = conn.cursor()
    names = cursor.execute(''f'SELECT name FROM responses join requests on responses.requestID = requests.id where race = "{race}"''').fetchall()
    conn.close()
    
    namesList = [name[0] for name in names]
    if name == 'Yes':
        namesList = [name.split()[0] for name in namesList]
    print("Names list: ",namesList)
    
    # Convert all names to uppercase and concatenate them into a single string
    allNames = ''.join(namesList).upper()

    # Count occurrences of each letter
    letterCounts = Counter(allNames)

    # Prepare data as a list of tuples for Google Charts
    chartData = [('Letter', 'Count')]  # Adding headers for Google Charts
    chartData.extend([(letter, count) for letter, count in sorted(letterCounts.items(), key=lambda item: item[1], reverse=True) if letter not in [' ', "'", '-']])

    #print("Chart data:", chartData)
    return jsonify(chartData)

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
    namesList = names['names']
    session['namesList'] = namesList  # Store namesList in session
    session['current'] = current



    return redirect(url_for('names'))

if __name__ == '__main__':
    app.run(debug=True, port=12128)

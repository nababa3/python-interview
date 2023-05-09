from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="bincomphptest"
)

# Define a route for the home page
@app.route('/')
def home():
    # Query the database for all LGAs in Delta State (state_id = 25)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM lga WHERE state_id = 25")
    lgas = cursor.fetchall()

    return render_template('home.html', lgas=lgas)

# Define a route for the form page
@app.route('/form')
def form():
    # Query the database for all parties
    cursor = db.cursor()
    cursor.execute("SELECT * FROM party")
    parties = cursor.fetchall()

    return render_template('form.html', parties=parties)

# Define a route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data from request object
    polling_unit_number = request.form['polling_unit_number']
    polling_unit_name = request.form['polling_unit_name']
    lga_id = request.form['lga_id']
    
	# Insert new polling unit into database and get its unique ID
	cursor = db.cursor()
	cursor.execute("INSERT INTO polling_unit (polling_unit_number, polling_unit_name, lga_id) VALUES (%s, %s, %s)", (polling_unit_number, polling_unit_name, lga_id))
	polling_unit_id = cursor.lastrowid

	# Insert results for each party into database
	for party in request.form.getlist('party'):
		party_abbreviation = party
		party_score = request.form[party]
		cursor.execute("INSERT INTO announced_pu_results (polling_unit_uniqueid, party_abbreviation, party_score) VALUES (%s, %s, %s)", (polling_unit_id, party_abbreviation, party_score))

	# Commit changes to database
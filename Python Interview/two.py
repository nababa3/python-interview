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

# Define a route for the results page
@app.route('/results', methods=['POST'])
def results():
    # Get the LGA ID from the form data
    lga_id = request.form['lga_id']

    # Query the database for results for all polling units in this LGA
    cursor = db.cursor()
    cursor.execute("SELECT party_abbreviation, SUM(party_score) FROM announced_pu_results JOIN polling_unit ON announced_pu_results.polling_unit_uniqueid=polling_unit.uniqueid WHERE polling_unit.lga_id=%s GROUP BY party_abbreviation", (lga_id,))
    results = cursor.fetchall()

    # Render the results template with the query results
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
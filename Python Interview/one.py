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
    return render_template('home.html')

# Define a route for the results page
@app.route('/results', methods=['POST'])
def results():
    # Get the polling unit ID from the form data
    polling_unit_id = request.form['polling_unit_id']

    # Query the database for results for this polling unit
    cursor = db.cursor()
    cursor.execute("SELECT * FROM announced_pu_results WHERE polling_unit_uniqueid = %s", (polling_unit_id,))
    results = cursor.fetchall()

    # Render the results template with the query results
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
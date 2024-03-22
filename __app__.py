from flask import Flask, render_template, request, redirect, session, jsonify
import requests
from database import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/card', methods=['GET', "POST"])
def card():
    if request.method == 'POST':
        print(request.form[""])   
    info = requests.get("https://randomuser.me/api/")
    data = {
        "results": info.json()["results"],
        "photos": imgData,
    }
    # print(data["photos"])
    return render_template("card.html", data = data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'your_username' and password == 'your_password':
            session['logged_in'] = True
            return redirect('/preferences')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if 'logged_in' not in session:
        return redirect('/login')
    if request.method == 'POST':
        # Process preferences form submission
        preferences = request.form.getlist('preferences')
        # Store preferences in database or session
        return redirect('/dashboard')
    return render_template('preferences.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect('/login')
    # Render dashboard page
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

API_ENDPOINT = "https://api.edamam.com/api/recipes/v2"
APP_ID = "3cbc3c7a"
APP_KEY = "c20c6a318eeef2df0da1867066f61d29"

# example:
# http://127.0.0.1:5000/search?q=chicken+tortillas&type=public&app_id=YOUR_APP_ID&app_key=YOUR_APP_KEY
 
@app.route("/search", methods=["GET"])
def search_recipes():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    params = {
        "q": query,
        "type": request.args.get("type", "any"),
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "ingr": request.args.get("ingr"),
        "diet": request.args.getlist("diet"),
        "health": request.args.getlist("health"),
        "cuisineType": request.args.getlist("cuisineType"),
        "mealType": request.args.getlist("mealType"),
        "dishType": request.args.getlist("dishType"),
        "calories": request.args.get("calories"),
        "time": request.args.get("time"),
        "imageSize": request.args.getlist("imageSize"),
        "glycemicIndex": request.args.get("glycemicIndex"),
        "inflammatoryIndex": request.args.get("inflammatoryIndex"),
        "excluded": request.args.getlist("excluded"),
        "random": request.args.get("random"),
        "nutrients[CA]": request.args.get("nutrients[CA]"),
        "nutrients[CHOCDF]": request.args.get("nutrients[CHOCDF]"),
        # Include other nutrients as needed
        # Add more parameters based on the provided specification
    }

    headers = {"Accept-Language": request.headers.get("Accept-Language", "en")}
    edamam_account_user = request.headers.get("Edamam-Account-User")
    if edamam_account_user:
        headers["Edamam-Account-User"] = edamam_account_user

    response = requests.get(API_ENDPOINT, params=params, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch recipes", "status_code": response.status_code}), 500

if __name__ == "__main__":
    app.run(debug=True)
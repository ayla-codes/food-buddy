from flask import Flask, render_template, request, redirect, session, jsonify
import requests
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

API_ENDPOINT = "https://api.edamam.com/api/recipes/v2"
APP_ID = "3cbc3c7a"
APP_KEY = "c20c6a318eeef2df0da1867066f61d29"
GEN_API_KEY = "AIzaSyBMstHXax4CPEr_SlgrPV18MToDuXu8zLU"

# example:
# http://127.0.0.1:5000/search?q=chicken+tortillas&type=public&app_id=YOUR_APP_ID&app_key=YOUR_APP_KEY
 
@app.route("/recipe", methods=["GET"])
def search_recipes():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    params = {
        "q": query,
        "type": "any",
        "app_id": APP_ID,
        "app_key": APP_KEY,
        # "ingr": request.args.get("ingr"),
        # "diet": request.args.getlist("diet"),
        # "health": request.args.getlist("health"),
    }

    response = requests.get(API_ENDPOINT, params=params)

    if response.status_code == 200:
        age = 18
        sex = "Male"
        weight = "70"
        height = "6'2"
        disease = "Iron Defficency, Anemia"

        prompt = f""" """

        x = response.json()["hits"]
        i = 1
        for j in range(6):
            item = x[j]
            recipe = item["recipe"]
            digest = recipe["digest"]
            recipe_entry = ""
            for nutrient in digest:
                label = nutrient["tag"]
                total = int(nutrient["total"])
                unit = nutrient["unit"]
                recipe_entry += f"{label}{total}{unit}, "
            prompt += f"\n{i}: {recipe_entry}\n"
            i += 1

        prompt += f"""1-6 are nutrient profiles for recipes for: Charachter: {age}yrs {sex} {weight}kg {height}ft Disease: {disease}\n If none of them fit the profile, return a recipie that is well-suited using: {query}\n"""
        prompt += f"""OUTPUT = list([3 indices of recipies])"""
        genai.configure(api_key=GEN_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        print(len(prompt))
        print(response)

        return jsonify({"prompt": prompt})
    else:
        return jsonify({"error": "Failed to fetch recipes", "status_code": response.status_code}), 500

if __name__ == "__main__":
    app.run(debug=True)
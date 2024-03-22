from flask import Flask, render_template, request, redirect, session, jsonify
from keys import *

import requests
import google.generativeai as genai
import ast

app = Flask(__name__)

API_ENDPOINT = "https://api.edamam.com/api/recipes/v2"
APP_ID = "3cbc3c7a"
APP_KEY = "c20c6a318eeef2df0da1867066f61d29"
GEN_API_KEY = "AIzaSyBMstHXax4CPEr_SlgrPV18MToDuXu8zLU"

@app.route("/")
def display_recipies():
    return render_template("form.html")

@app.route("/", methods=["POST"])
def process_recipies():
    age = request.form.get("age")
    gender = request.form.get("gender")
    weight = request.form.get("weight")
    height = request.form.get("height")
    disease = request.form.get("disease")
    q = request.form.getlist("ingredients")

    if not q:
        return jsonify({"error": "Ingredients parameters are required"}), 400
    if not age:
        return jsonify({"error": "Age is required"}), 400
    if not gender:
        return jsonify({"error": "Gender is required"}), 400
    if not weight:
        return jsonify({"error": "Weight is required"}), 400
    if not height:
        return jsonify({"error": "Height is required"}), 400
    if not disease:
        return jsonify({"error": "Disease is required"}), 400
    
    ingredients = ""
    j = 1
    for i in q:
        if len(q) == (j):
            ingredients += i.lower()
        else:
            ingredients += i.lower()
            ingredients += "+"
            j += 1

    params = {
        "q": ingredients,
        "type": "any",
        "app_id": APP_ID,
        "app_key": APP_KEY,
    }

    response_pre = requests.get(API_ENDPOINT, params=params)
    response = response_pre.json()["hits"]
    return render_template("recipes.html", recipes=response)
    # x = []
    # b = 0

    # for k in range(6):
    #     j = response.index(b)
    #     b += 1
    #     i = j["recipe"]
    #     genai.configure(api_key=GEN_API_KEY)
    #     model = genai.GenerativeModel('gemini-pro')
    #     prompt = ""
    #     digest = i["digest"]
    #     recipe_entry = ""
    #     for nutrient in digest:
    #         label = nutrient["tag"]
    #         total = int(nutrient["total"])
    #         unit = nutrient["unit"]
    #         recipe_entry += f"{label}{total}{unit}, "
    #     prompt += f"\n{recipe_entry}\n"
        
    #     response = model.generate_content(f"You are a nutritionist, given a recipie and a health profile for a individual please tell if the recipe is fit for the person or not. Strictly answer in 'yes' or 'no'\n User details: {age}yrs {height}ft {gender} {weight}kg diseases: {disease}\nRecipe Profile: {prompt}")
    #     rt = response.text

    #     if rt == "yes":
    #         x.append(j["recipie"])
    #         print(x)

         




    #     prompt += f"""given above are are nutrient profiles for recipes for: Charachter: {age}yrs {gender} {weight}kg {height}ft Disease: {disease}\n Return only one number as the index of a well suited recipe \n"""
    #     print(prompt)

    #     genai.configure(api_key=GEN_API_KEY)
    #     model = genai.GenerativeModel('gemini-pro')
    #     response = model.generate_content(prompt)
    #     print(response)
    #     rt = response.text
    #     print(f"{rt}")

    #     # print(f"->>>> {rt}")
    #     if len(rt) == 9:
    #         lo = ast.literal_eval(rt)
    #         print(lo)
    #         print(response_a[lo[0]])
    #         return render_template("recipes.html", one=response_a[lo[0]], two=response_a[lo[1]], three=response_a[lo[2]])
    #     else:
    #         return render_template("recipe.html", content=rt)
    # else:
    #     return jsonify({"error": "Failed to fetch recipes", "status_code": response.status_code}), 500

if __name__ == "__main__":
    app.run(debug=False)
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Expanded nutrition dataset (~50 foods) with approximate protein, fat, calories per serving
nutrition_data = {
    'butter chicken': {'protein': '25 g', 'fat': '20 g', 'calories': '300 kcal'},
    'dal': {'protein': '9 g', 'fat': '2 g', 'calories': '150 kcal'},
    'burger': {'protein': '30 g', 'fat': '15 g', 'calories': '400 kcal'},
    'pizza': {'protein': '12 g', 'fat': '10 g', 'calories': '270 kcal'},
    'biryani': {'protein': '22 g', 'fat': '14 g', 'calories': '350 kcal'},
    'samosa': {'protein': '5 g', 'fat': '12 g', 'calories': '250 kcal'},
    'pasta': {'protein': '8 g', 'fat': '10 g', 'calories': '220 kcal'},
    'palak paneer': {'protein': '15 g', 'fat': '18 g', 'calories': '280 kcal'},
    'chicken curry': {'protein': '28 g', 'fat': '17 g', 'calories': '310 kcal'},
    'masala dosa': {'protein': '6 g', 'fat': '8 g', 'calories': '190 kcal'},
    'idli': {'protein': '2.5 g', 'fat': '0.5 g', 'calories': '70 kcal'},
    'tandoori chicken': {'protein': '26 g', 'fat': '12 g', 'calories': '290 kcal'},
    'naan': {'protein': '8 g', 'fat': '7 g', 'calories': '250 kcal'},
    'roti': {'protein': '3 g', 'fat': '1 g', 'calories': '70 kcal'},
    'fish curry': {'protein': '25 g', 'fat': '15 g', 'calories': '280 kcal'},
    'chole': {'protein': '12 g', 'fat': '5 g', 'calories': '210 kcal'},
    'aloo gobi': {'protein': '4 g', 'fat': '6 g', 'calories': '180 kcal'},
    'paneer tikka': {'protein': '18 g', 'fat': '12 g', 'calories': '290 kcal'},
    'vegetable pulao': {'protein': '6 g', 'fat': '9 g', 'calories': '230 kcal'},
    'mutter paneer': {'protein': '16 g', 'fat': '15 g', 'calories': '300 kcal'},
    'egg curry': {'protein': '20 g', 'fat': '14 g', 'calories': '270 kcal'},
    'vada': {'protein': '6 g', 'fat': '10 g', 'calories': '200 kcal'},
    'dal makhani': {'protein': '11 g', 'fat': '12 g', 'calories': '250 kcal'},
    'gobi manchurian': {'protein': '5 g', 'fat': '8 g', 'calories': '220 kcal'},
    'chicken biryani': {'protein': '25 g', 'fat': '17 g', 'calories': '350 kcal'},
    'mango lassi': {'protein': '6 g', 'fat': '4 g', 'calories': '180 kcal'},
    'gulab jamun': {'protein': '4 g', 'fat': '10 g', 'calories': '300 kcal'},
    'rasgulla': {'protein': '3 g', 'fat': '5 g', 'calories': '200 kcal'},
    'jalebi': {'protein': '2 g', 'fat': '18 g', 'calories': '320 kcal'},
    'paneer butter masala': {'protein': '17 g', 'fat': '20 g', 'calories': '330 kcal'},
    'mutton curry': {'protein': '30 g', 'fat': '22 g', 'calories': '400 kcal'},
    'fish fry': {'protein': '28 g', 'fat': '18 g', 'calories': '350 kcal'},
    'palak soup': {'protein': '3 g', 'fat': '2 g', 'calories': '90 kcal'},
    'vegetable soup': {'protein': '4 g', 'fat': '3 g', 'calories': '100 kcal'},
    'cutlets': {'protein': '8 g', 'fat': '10 g', 'calories': '230 kcal'},
    'egg bhurji': {'protein': '18 g', 'fat': '12 g', 'calories': '270 kcal'},
    'dhokla': {'protein': '5 g', 'fat': '3 g', 'calories': '150 kcal'},
    'rogan josh': {'protein': '30 g', 'fat': '22 g', 'calories': '390 kcal'},
    'bhindi masala': {'protein': '3 g', 'fat': '7 g', 'calories': '160 kcal'},
    'paneer bhurji': {'protein': '19 g', 'fat': '14 g', 'calories': '310 kcal'},
    'rajma': {'protein': '15 g', 'fat': '5 g', 'calories': '240 kcal'},
    'pav bhaji': {'protein': '8 g', 'fat': '14 g', 'calories': '290 kcal'},
    'veg fried rice': {'protein': '7 g', 'fat': '9 g', 'calories': '260 kcal'},
    'chicken 65': {'protein': '27 g', 'fat': '18 g', 'calories': '340 kcal'},
    'kheer': {'protein': '6 g', 'fat': '10 g', 'calories': '270 kcal'},
    'kulfi': {'protein': '5 g', 'fat': '12 g', 'calories': '290 kcal'},
    'methi paratha': {'protein': '5 g', 'fat': '7 g', 'calories': '210 kcal'},
    'paneer paratha': {'protein': '12 g', 'fat': '14 g', 'calories': '320 kcal'},
    'chicken soup': {'protein': '18 g', 'fat': '9 g', 'calories': '180 kcal'}
}

def classify_veg_nonveg(category):
    """Classify veg/non-veg based on TheMealDB category"""
    non_veg_cats = ['Beef', 'Chicken', 'Lamb', 'Pork', 'Seafood', 'Goat', 'Veal']
    if category in non_veg_cats:
        return "Non-Vegetarian"
    elif category == 'Vegetarian':
        return "Vegetarian"
    else:
        # Unknown or diverse categories considered Vegetarian for safety
        return "Vegetarian"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_food_info', methods=['POST'])
def get_food_info():
    data = request.json
    food_name = data.get('food_name', '').strip().lower()
    if not food_name:
        return jsonify({'error': True, 'message': 'Please enter a food name!'})

    try:
        # Query TheMealDB API to get recipes
        url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={food_name}'
        resp = requests.get(url)
        meal_data = resp.json()

        if not meal_data or not meal_data['meals']:
            return jsonify({
                'error': False,
                'food_name': food_name.title(),
                'type': 'Unknown',
                'ingredients': ['No recipe data found.'],
                'protein': 'N/A',
                'fat': 'N/A',
                'calories': 'N/A',
                'message': "Sorry, no detailed info found for this food."
            })

        meal = meal_data['meals'][0]

        # Extract category for veg/non-veg classification
        category = meal.get('strCategory', 'Unknown')
        veg_type = classify_veg_nonveg(category)

        # Get the main ingredients (up to 20)
        ingredients = []
        for i in range(1, 21):
            ingredient = meal.get(f'strIngredient{i}')
            measure = meal.get(f'strMeasure{i}')
            if ingredient and ingredient.strip():
                ingredients.append(f"{measure.strip()} {ingredient.strip()}".strip())
            else:
                break

        # Get nutrition info from local dataset if available
        nutrition = nutrition_data.get(food_name, {
            'protein': 'N/A',
            'fat': 'N/A',
            'calories': 'N/A'
        })

        return jsonify({
            'error': False,
            'food_name': meal.get('strMeal', food_name.title()),
            'type': veg_type,
            'ingredients': ingredients if ingredients else ['No ingredients data available.'],
            'protein': nutrition['protein'],
            'fat': nutrition['fat'],
            'calories': nutrition['calories'],
            'message': meal.get('strInstructions', '')[:300] + '...' if meal.get('strInstructions') else ''
        })

    except Exception as e:
        return jsonify({'error': True, 'message': f'Error: {str(e)}'})

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

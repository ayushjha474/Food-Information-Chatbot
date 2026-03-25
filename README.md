# 🍽️ Food Info Chatbot

A simple and interactive web-based chatbot built using Flask that provides detailed information about food items including ingredients, nutritional values, and veg/non-veg classification.

---

## 🚀 Features

* 🔍 Search any food item
* 🥗 Displays ingredients list
* 🔥 Shows calories, protein, and fat
* 🌱 Classifies food as Vegetarian or Non-Vegetarian
* 🌐 Fetches real-time recipe data from TheMealDB API
* 💬 Clean chatbot-style UI

---

## 🛠️ Tech Stack

* Backend: Python (Flask)
* Frontend: HTML, CSS, JavaScript
* API: TheMealDB API

---

## 📂 Project Structure

```
Food-Information-Chatbot/
│── app.py
│── templates/
│     └── index.html
│── requirements.txt
│── README.md


```

---

## ⚙️ Installation & Setup

1. Clone the repository:

```
git clone https://github.com/ayushjha474/Food-Information-Chatbot.git
cd Food-Information-Chatbot
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the application:

```
python app.py
```

4. Open in browser:

```
http://localhost:5555
```

---

## 💡 How It Works

* User enters a food name
* Flask backend sends request to TheMealDB API
* Retrieves ingredients and recipe details
* Matches nutrition data from local dataset
* Displays results in chatbot interface

---

## 📸 Example Queries

* "pizza"
* "dal"
* "paneer tikka"
* "biryani"

---

## ⚠️ Limitations

* Nutrition data is approximate
* Some foods may not be found in API
* Carbohydrates data is currently missing

---

## 🔮 Future Improvements

* Add carbs data
* Improve UI/UX
* Add image of food
* Deploy online (Render / Railway)

---

## 👨‍💻 Author

Aayush Jha

---

## ⭐ If you like this project

Give it a star on GitHub!
c

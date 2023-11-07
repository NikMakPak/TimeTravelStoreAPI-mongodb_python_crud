from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient("mongodb://localhost:27018/")
db = client['timeTravelStore']

categories_col = db['Categories']
countries_col = db['Countries']
travels_col = db['Travels']
users_col = db['Users']
orders_col = db['Orders']

category_data = [
    {"_id": ObjectId(), "name": "Стандартные путешествия"},
    {"_id": ObjectId(), "name": "Акционные путешествия"},
    {"_id": ObjectId(), "name": "VIP путешествия"}
]
categories_col.create_index("name", unique=True)
categories_col.insert_many(category_data)

user_data = [
    {"_id": ObjectId(), "name": "Иван", "email": "ivan@example.com"},
    {"_id": ObjectId(), "name": "Анна", "email": "anna@example.com"}
]
users_col.create_index("email", unique=True)
users_col.insert_many(user_data)

country_data = [
    {"_id": ObjectId(), "name": "Земля"},
    {"_id": ObjectId(), "name": "Марс"}
]
countries_col.create_index("name", unique=True)
countries_col.insert_many(country_data)

travel_data = [
    {
        "_id": ObjectId(),
        "name": "Путешествие в будущее",
        "description": "Путешествие в будущее на 500 лет вперед",
        "category_id": categories_col.find_one({"name": "Стандартные путешествия"})["_id"],
        "country_id": countries_col.find_one({"name": "Земля"})["_id"],
        "year": 2523,
        "price": 10000,
        "reviews": []
    },
    {
        "_id": ObjectId(),
        "name": "Эпоха фараонов: Великий Египет",
        "description": "Путешествие в значимое историческое событие на Земле, а именно Путешествие в Древний Египет",
        "category_id": categories_col.find_one({"name": "Акционные путешествия"})["_id"],
        "country_id": countries_col.find_one({"name": "Земля"})["_id"],
        "year": -2500,
        "price": 7500,
        "reviews": []
    },
    {
        "_id": ObjectId(),
        "name": "Путешествие на Марс",
        "description": "Путешествие на Марс, исследование колоний и пентхауса Маска",
        "category_id": categories_col.find_one({"name": "VIP путешествия"})["_id"],
        "country_id": countries_col.find_one({"name": "Марс"})["_id"],
        "year": 2200,
        "price": 25000,
        "reviews": [
            {
                "_id": ObjectId(),
                "user_id": users_col.find_one({"email": "ivan@example.com"})["_id"],
                "text": "Отличное путешествие!",
                "rating": 5
            },
            {
                "_id": ObjectId(),
                "user_id": users_col.find_one({"email": "anna@example.com"})["_id"],
                "text": "Невероятный опыт! но мало показали всего",
                "rating": 4
            }
        ]
    }
]
travels_col.create_index("name", unique=True)
travels_col.insert_many(travel_data)

order_data = [
    {
        "_id": ObjectId(),
        "user_id": users_col.find_one({"email": "ivan@example.com"})["_id"],
        "travel_id": travels_col.find_one({"name": "Путешествие в будущее"})["_id"],
        "order_date": datetime.now()
    },
    {
        "_id": ObjectId(),
        "user_id": users_col.find_one({"email": "anna@example.com"})["_id"],
        "travel_id": travels_col.find_one({"name": "Путешествие на Марс"})["_id"],
        "order_date": datetime.now()
    },
     {
        "_id": ObjectId(),
        "user_id": users_col.find_one({"email": "anna@example.com"})["_id"],
        "travel_id": travels_col.find_one({"name": "Эпоха фараонов: Великий Египет"})["_id"],
        "order_date": datetime.now()
    }
]
orders_col.insert_many(order_data)
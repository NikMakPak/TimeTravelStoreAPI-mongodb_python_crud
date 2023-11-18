from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27018/")
db = client['timeTravelStore']
categories_col = db['Categories']
countries_col = db['Countries']
travels_col = db['Travels']
users_col = db['Users']
orders_col = db['Orders']

@app.route('/travels/<country_name>', methods=['GET'])
def get_travels_by_country(country_name):
    pipeline = [
        {"$match": {"country_id": countries_col.find_one({"name": country_name})["_id"]}},
        {"$lookup": {
            "from": "Countries",
            "localField": "country_id",
            "foreignField": "_id",
            "as": "country_info"
        }},
        {"$unwind": "$country_info"},
        {"$group": {
            "_id": "$country_info.name",
            "travels": {"$push": "$name"}
        }},
        {"$project": {
            "_id": 0,
            "country": "$_id",
            "travels": 1
        }}
    ]
    result = list(travels_col.aggregate(pipeline))
    return str(result)

@app.route('/users/<email>/orders', methods=['GET'])
def get_user_orders(email):
    pipeline = [
        {"$match": {"user_id": users_col.find_one({"email": email})["_id"]}},
        {"$lookup": {
            "from": "Travels",
            "localField": "travel_id",
            "foreignField": "_id",
            "as": "travel_info"
        }},
        {"$unwind": "$travel_info"},
        {"$group": {
            "_id": "$user_id",
            "total_orders": {"$sum": 1},
            "total_spent": {"$sum": "$travel_info.price"},
            "travels": {"$push": "$travel_info.name"}
        }},
        {"$project": {
            "_id": 0,
            "total_orders": 1,
            "total_spent": 1,
            "travels": 1
        }}
    ]
    result = list(orders_col.aggregate(pipeline))
    return str(result)

@app.route('/categories', methods=['POST'])
def create_category():
    name = request.json.get('name')
    category_id = ObjectId()
    category_data = {"_id": category_id, "name": name}
    categories_col.insert_one(category_data)
    return str(category_id)

@app.route('/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    result = categories_col.find_one({"_id": ObjectId(category_id)})
    return str(result)

@app.route('/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    name = request.json.get('name')
    categories_col.update_one({"_id": ObjectId(category_id)}, {"$set": {"name": name}})
    return 'Category updated successfully'

@app.route('/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    categories_col.delete_one({"_id": ObjectId(category_id)})
    return 'Category deleted successfully'

# Countries collection CRUD operations
@app.route('/countries', methods=['POST'])
def create_country():
    name = request.json.get('name')
    country_id = ObjectId()
    country_data = {"_id": country_id, "name": name}
    countries_col.insert_one(country_data)
    return str(country_id)

@app.route('/countries/<country_id>', methods=['GET'])
def get_country(country_id):
    result = countries_col.find_one({"_id": ObjectId(country_id)})
    return str(result)

@app.route('/countries/<country_id>', methods=['PUT'])
def update_country(country_id):
    name = request.json.get('name')
    countries_col.update_one({"_id": ObjectId(country_id)}, {"$set": {"name": name}})
    return 'Country updated successfully'

@app.route('/countries/<country_id>', methods=['DELETE'])
def delete_country(country_id):
    countries_col.delete_one({"_id": ObjectId(country_id)})
    return 'Country deleted successfully'

@app.route('/travels', methods=['POST'])
def create_travel():
    name = request.json.get('name')
    description = request.json.get('description')
    category_id = request.json.get('category_id')
    country_id = request.json.get('country_id')
    year = request.json.get('year')
    price = request.json.get('price')
    reviews = request.json.get('reviews', [])
    
    travel_id = ObjectId()
    travel_data = {
        "_id": travel_id,
        "name": name,
        "description": description,
        "category_id": ObjectId(category_id),
        "country_id": ObjectId(country_id),
        "year": year,
        "price": price,
        "reviews": reviews
    }
    travels_col.insert_one(travel_data)
    return str(travel_id)

@app.route('/travels/<travel_id>', methods=['GET'])
def get_travel(travel_id):
    result = travels_col.find_one({"_id": ObjectId(travel_id)})
    return str(result)

@app.route('/travels/<travel_id>', methods=['PUT'])
def update_travel(travel_id):
    name = request.json.get('name')
    description = request.json.get('description')
    category_id = request.json.get('category_id')
    country_id = request.json.get('country_id')
    year = request.json.get('year')
    price = request.json.get('price')
    reviews = request.json.get('reviews')
    
    update_data = {}
    if name:
        update_data["name"] = name
    if description:
        update_data["description"] = description
    if category_id:
        update_data["category_id"] = ObjectId(category_id)
    if country_id:
        update_data["country_id"] = ObjectId(country_id)
    if year:
        update_data["year"] = year
    if price:
        update_data["price"] = price
    if reviews is not None:
        update_data["reviews"] = reviews

    travels_col.update_one({"_id": ObjectId(travel_id)}, {"$set": update_data})
    
    return 'Travel updated successfully'

@app.route('/travels/<travel_id>', methods=['DELETE'])
def delete_travel(travel_id):
    travels_col.delete_one({"_id": ObjectId(travel_id)})
    return 'Travel deleted successfully'

# Users collection CRUD operations
@app.route('/users', methods=['POST'])
def create_user():
    name = request.json.get('name')
    email = request.json.get('email')
    
    user_id = ObjectId()
    user_data = {"_id": user_id, "name": name, "email": email}
    users_col.insert_one(user_data)
    
    return str(user_id)

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    result = users_col.find_one({"_id": ObjectId(user_id)})
    
    return str(result)

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    name = request.json.get('name')
    email = request.json.get('email')
    
    update_data = {}
    if name:
        update_data["name"] = name
    if email:
        update_data["email"] = email

    users_col.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    
    return 'User updated successfully'

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    users_col.delete_one({"_id": ObjectId(user_id)})
    
    return 'User deleted successfully'

# Orders collection CRUD operations
@app.route('/orders', methods=['POST'])
def create_order():
    user_id = request.json.get('user_id')
    travel_id = request.json.get('travel_id')
    
    order_id = ObjectId()
    order_date = datetime.now()
    
    order_data = {
        "_id": order_id,
        "user_id": ObjectId(user_id),
        "travel_id": ObjectId(travel_id),
        "order_date": order_date
    }
    
    orders_col.insert_one(order_data)
    
    return str(order_id)

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    print(order_id)
    result = orders_col.find_one({"_id": ObjectId(order_id)})
    return str(result)

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    user_id = request.json.get('user_id')
    travel_id = request.json.get('travel_id')
    
    update_data = {}
    
    if user_id:
        update_data["user_id"] = ObjectId(user_id)
        
    if travel_id:
        update_data["travel_id"] = ObjectId(travel_id)

    orders_col.update_one({"_id": ObjectId(order_id)}, {"$set": update_data})
    
    return 'Order updated successfully'

@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    orders_col.delete_one({"_id": ObjectId(order_id)})
    
    return 'Order deleted successfully'

if __name__ == '__main__':
   app.run()

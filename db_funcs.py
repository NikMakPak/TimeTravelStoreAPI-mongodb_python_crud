from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27018/")
        self.db = self.client['timeTravelStore']
        self.categories_col = self.db['Categories']
        self.countries_col = self.db['Countries']
        self.travels_col = self.db['Travels']
        self.users_col = self.db['Users']
        self.orders_col = self.db['Orders']
    
    def get_travels_by_country(self, country_name):
        pipeline = [
            {"$match": {"country_id": self.countries_col.find_one({"name": country_name})["_id"]}},
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
        return list(self.travels_col.aggregate(pipeline))


    def get_user_orders(self, email):
        pipeline = [
            {"$match": {"user_id": self.users_col.find_one({"email": email})["_id"]}},
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
        return list(self.orders_col.aggregate(pipeline))


    # Categories collection CRUD operations
    def create_category(self, name):
        category_id = ObjectId()
        category_data = {"_id": category_id, "name": name}
        self.categories_col.insert_one(category_data)
        return category_id

    def get_category(self, category_id):
        return self.categories_col.find_one({"_id": ObjectId(category_id)})

    def update_category(self, category_id, name):
        self.categories_col.update_one({"_id": ObjectId(category_id)}, {"$set": {"name": name}})

    def delete_category(self, category_id):
        self.categories_col.delete_one({"_id": ObjectId(category_id)})

    # Countries collection CRUD operations
    def create_country(self, name):
        country_id = ObjectId()
        country_data = {"_id": country_id, "name": name}
        self.countries_col.insert_one(country_data)
        return country_id

    def get_country(self, country_id):
        return self.countries_col.find_one({"_id": ObjectId(country_id)})

    def update_country(self, country_id, name):
        self.countries_col.update_one({"_id": ObjectId(country_id)}, {"$set": {"name": name}})

    def delete_country(self, country_id):
        self.countries_col.delete_one({"_id": ObjectId(country_id)})

    # Travels collection CRUD operations
    def create_travel(self, name, description, category_id, country_id, year, price, reviews=[]):
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
        self.travels_col.insert_one(travel_data)
        return travel_id

    def get_travel(self, travel_id):
        return self.travels_col.find_one({"_id": ObjectId(travel_id)})

    def update_travel(self, travel_id, name=None, description=None, category_id=None, country_id=None,
                      year=None, price=None, reviews=None):
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

        self.travels_col.update_one({"_id": ObjectId(travel_id)}, {"$set": update_data})

    def delete_travel(self, travel_id):
        self.travels_col.delete_one({"_id": ObjectId(travel_id)})

    # Users collection CRUD operations
    def create_user(self, name, email):
        user_id = ObjectId()
        user_data = {"_id": user_id, "name": name, "email": email}
        self.users_col.insert_one(user_data)
        return user_id

    def get_user(self, user_id):
        return self.users_col.find_one({"_id": ObjectId(user_id)})

    def update_user(self, user_id, name=None, email=None):
        update_data = {}
        if name:
            update_data["name"] = name
        if email:
            update_data["email"] = email

        self.users_col.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    def delete_user(self, user_id):
        self.users_col.delete_one({"_id": ObjectId(user_id)})

    # Orders collection CRUD operations
    def create_order(self, user_id, travel_id):
        order_id = ObjectId()
        order_date = datetime.now()
        order_data = {
            "_id": order_id,
            "user_id": ObjectId(user_id),
            "travel_id": ObjectId(travel_id),
            "order_date": order_date
        }
        self.orders_col.insert_one(order_data)
        return order_id

    def get_order(self, order_id):
        return self.orders_col.find_one({"_id": ObjectId(order_id)})

    def update_order(self, order_id, user_id=None, travel_id=None):
        update_data = {}
        if user_id:
            update_data["user_id"] = ObjectId(user_id)
        if travel_id:
            update_data["travel_id"] = ObjectId(travel_id)

        self.orders_col.update_one({"_id": ObjectId(order_id)}, {"$set": update_data})

    def delete_order(self, order_id):
        self.orders_col.delete_one({"_id": ObjectId(order_id)})
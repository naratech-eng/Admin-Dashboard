from flask import Flask, jsonify, request,abort
from flask_mongoengine import MongoEngine
from flask_cors import CORS
import json
from datetime import datetime
from bson import ObjectId
from mongoengine.queryset.visitor import Q
from mongoengine.fields import MapField, IntField, StringField, DateTimeField, ListField, EmbeddedDocumentField, ReferenceField

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'dashboardDB',  # Replace with your MongoDB database name
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine(app)
# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

#Models 
#User data Schema
class User(db.Document):
    # _id = db.StringField(primary_key=True)
    _id = db.ObjectIdField(default=ObjectId, primary_key=True)  # _id field as an ObjectIdField with primary_key=True
    name = db.StringField(required=True, min_length=2, max_length=100, nullable=False)
    email = db.StringField(required=True, max_length=50, unique=True)
    password = db.StringField(required=True, min_length=5)
    city = db.StringField()
    state = db.StringField()
    country = db.StringField()
    occupation = db.StringField()
    phoneNumber = db.StringField()
    transactions = db.ListField(db.StringField())
    role = db.StringField(choices=["user", "admin", "superadmin"], default="admin")
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "users",  # Specify the collection name in MongoDB
        
    }

#Product Data Schema
class Product(db.Document):
    _id = db.ObjectIdField(default=ObjectId, primary_key=True)
    name = db.StringField()
    price = db.FloatField()
    description = db.StringField()
    category = db.StringField()
    rating = db.FloatField()
    supply = db.IntField()

    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)
    meta = {
        'collection': 'products',  # Specify the collection name in MongoDB
       
    }

class ProductStat(db.Document):
    _id = db.ObjectIdField(default=ObjectId)
    # productId = db.StringField()
    productId = db.ReferenceField(Product)
    yearlySalesTotal = db.FloatField()
    yearlyTotalSoldUnits = db.IntField()
    year = db.IntField()
    monthlyData = db.ListField(db.DictField())
    dailyData = db.ListField(db.DictField())

    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)
    meta = {
        'collection': 'product_stats',  # Specify the collection name in MongoDB
    }

class Transaction(db.Document):
    _id = db.ObjectIdField(default=ObjectId)
    userId = db.StringField()
    cost = db.StringField()
    products = db.ListField(db.ReferenceField('Product'))

    meta = {'collection': 'transactions'}
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)


class MonthlyData(db.EmbeddedDocument):
    month = db.StringField()
    totalSales = db.IntField()
    totalUnits = db.IntField()
    _id = db.ObjectIdField(default=ObjectId)


class DailyData(db.EmbeddedDocument):
    date = db.StringField()
    totalSales = db.IntField()
    totalUnits = db.IntField()
    _id = db.ObjectIdField(default=ObjectId)


class OverallStat(db.Document):
    totalCustomers = db.IntField()
    yearlySalesTotal = db.IntField()
    yearlyTotalSoldUnits = db.IntField()
    year = db.IntField()
    monthlyData = db.ListField(db.EmbeddedDocumentField(MonthlyData))
    dailyData = db.ListField(db.EmbeddedDocumentField(DailyData))
    salesByCategory = db.DictField()
    createdAt = db.DateTimeField(default=datetime.utcnow)
    updatedAt = db.DateTimeField(default=datetime.utcnow)
    _id = db.ObjectIdField(default=ObjectId)
    __v = db.IntField()


#load data into database
with open('data/user_data.json', 'r') as file:
    # data_str = file.read()
    user_data = json.load(file)
    
# Iterate over the user data and save each user to the database
for data in user_data:
    email = data['email']
    user = User.objects(email=email).first()
    if user is None:
        user = User(**data)
        user.save()

#load prduct data into database
with open('data/product_data.json', 'r') as fileProduct:
    # data_str = file.read()
    product_data = json.load(fileProduct)
    
# Iterate over the user data and save each user to the database
for data in product_data:
    id = data['_id']
    product = Product.objects(_id=id).first()
    if product is None:
        product = Product(**data)
        product.save()

#load prduct data into database
with open('data/productstat_data.json', 'r') as fileProduct:
    # data_str = file.read()
    productstat_data = json.load(fileProduct)
    
# Iterate over the user data and save each user to the database
for data in productstat_data:
    id = data['_id']
    productstat = ProductStat.objects(_id=id).first()
    if productstat is None:
        productstat = ProductStat(**data)
        productstat.save()

# Load data into the database
with open('data/transactions_data.json', 'r') as file:
    transaction_data = json.load(file)

# Iterate over the transaction data and save each transaction to the database
for data in transaction_data:
    user_id = data['userId']
    transaction = Transaction.objects(userId=user_id).first()
    if transaction is None:
        # Convert the "cost" field to a string before saving
        data['cost'] = str(data['cost'])
        transaction = Transaction(**data)
        transaction.save()
#load prduct data into database
with open('data/overallstat_data.json', 'r') as fileProduct:
    # data_str = file.read()
    overallstat_data = json.load(fileProduct)
    
# Iterate over the user data and save each user to the database
for data in overallstat_data:
    id = data['_id']
    overallstat = OverallStat.objects(_id=id).first()
    if overallstat is None:
        # Remove unwanted fields from the data
        data.pop('createdAt', None)
        data.pop('__v', None)
        data.pop('updatedAt', None)

        overallstat = OverallStat(**data)
        overallstat.save()

#routes
@app.route('/', methods = ['GET', 'POST'])
def home():
    return 'working backend'

@app.route('/users/<string:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.objects.get(_id=id)
        return jsonify(user), 200
    except User.DoesNotExist:
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


### get products route
@app.route('/products', methods=['GET'])
def get_products():
   
    try:

        pipeline = [
            {
                '$lookup': {
                    'from': 'product_stats',
                    'localField': '_id',
                    'foreignField': 'productId',
                    'as': 'stat'
                }
            },
                {
                    '$unwind': {
                        'path': '$stat',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                {
                    '$addFields': {
                        'stat': {
                            '$ifNull': ['$stat', {}]
                        }
                    }
                }
            ]

        products_with_stats = Product.objects.aggregate(*pipeline)
        # Convert ObjectId to string for serialization
        products_with_stats = [
            json.loads(json.dumps(product, default=lambda o: str(o) if isinstance(o, ObjectId) else None))
            for product in products_with_stats
        ]

        return products_with_stats

    except Exception as e:
        return jsonify({"message": str(e)}), 404
    
    #get customers
@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        customers = User.objects(role='user').exclude('password')

        return jsonify(customers), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 404
    
    #get transactions.
@app.route('/transactions', methods=['GET'])
def get_transactions():
    try:
        # Parse query parameters
        page = int(request.args.get('page', 1))
        pageSize = int(request.args.get('pageSize', 20))
        sort = request.args.get('sort')
        search = request.args.get('search', '')
        print(search)
        # Formatted sort should look like { "userId": -1 }
        def generate_sort():
            sort_parsed = json.loads(sort)
            sort_formatted = {sort_parsed['field']: 1 if sort_parsed['sort'] == 'asc' else -1}
            return sort_formatted

        sort_formatted = generate_sort() if sort else {}

        # Query transactions based on search and sort criteria
        query = {
            '$or': [
                {'cost': {'$regex': search, '$options': 'i'}},
                {'userId': {'$regex': search, '$options': 'i'}}
            ]
        }
        transactions = Transaction.objects(__raw__=query).order_by(**sort_formatted).skip((page - 1) * pageSize).limit(pageSize)
        total = Transaction.objects(__raw__=query).count()

        return jsonify({'transactions': transactions, 'total': total}), 200
    except Exception as error:
        return jsonify({'message': str(error)}), 404   

#get sales data
@app.route('/sales', methods=['GET'])
def get_sales():
    try:
        overall_stats = OverallStat.objects().first()

        if overall_stats:
            return jsonify(overall_stats), 200
        else:
            abort(404, "No overall stats found")
    except Exception as e:
        abort(500, str(e))




if __name__ == '__main__':
    app.run(debug=True)
from bson import ObjectId

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
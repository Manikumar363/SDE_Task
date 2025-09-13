import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

# Define JSON schema for employees collection
employee_schema = {
	"bsonType": "object",
	"required": [
		"employee_id", "name", "department", "salary", "joining_date", "skills"
	],
	"properties": {
		"employee_id": {"bsonType": "string"},
		"name": {"bsonType": "string"},
		"department": {"bsonType": "string"},
		"salary": {"bsonType": "double"},
		"joining_date": {"bsonType": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
		"skills": {
			"bsonType": "array",
			"items": {"bsonType": "string"}
		}
	}
}

# Create collection with schema validation if not exists
if "employees" not in db.list_collection_names():
	db.create_collection(
		"employees",
		validator={"$jsonSchema": employee_schema},
		validationLevel="strict"
	)
employees_collection = db["employees"]

# Create unique index on employee_id
employees_collection.create_index("employee_id", unique=True)

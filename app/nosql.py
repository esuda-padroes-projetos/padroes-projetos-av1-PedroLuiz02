from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["meu_ecommerce"]

usuarios = mongo_db["usuarios"]
produtos = mongo_db["produtos"]

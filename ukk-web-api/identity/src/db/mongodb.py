# import os

# from pymongo import MongoClient

# MONGO_USER      = os.environ.get('MONGO_USER')
# MONGO_PASSWORD  = os.environ.get('MONGO_PASSWORD')
# MONGO_HOST      = os.environ.get('MONGO_HOST', 'localhost:27017')
# MONGO_NAME      = os.environ.get('MONGO_NAME', 'ptba')

# DB_URL = f"mongodb://{MONGO_HOST}/"
# if (MONGO_USER): DB_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/"

# client = MongoClient(DB_URL)

# db = client[MONGO_NAME]

# #### DOCS: https://pymongo.readthedocs.io/en/stable/tutorial.html ####

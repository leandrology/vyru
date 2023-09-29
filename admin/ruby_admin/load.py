import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ruby_admin.settings")

import pymongo
from django.core.exceptions import ObjectDoesNotExist

import django
django.setup()

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from convo.models import Response
# MongoDB connection
uri = "mongodb+srv://rubyadmin123:rubyadmin123@cluster0.scmw523.mongodb.net/?retryWrites=true&w=majority"

database = "rasa-ruby"
collection = "rasamodels"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# client = MongoClient(connection_string)
db = client[database]
collection = db[collection]
# client = pymongo.MongoClient("mongodb+srv://rubyadmin123:rubyadmin123@cluster0.scmw523.mongodb.net/?retryWrites=true&w=majority")
# db = client["rasa-ruby"]
# collection = db["rasamodels"]

# Retrieve data from MongoDB
mongo_data = collection.find()

# Map and save data to Django model
for entry in mongo_data:
    try:
        response_instance = Response.objects.get(intent=entry['domain']['intent'])
        print(response_instance)
    except ObjectDoesNotExist:
        response_instance = Response(
            intent=entry['domain']['intent'],
            message=entry['nlu']['examples'][0],
            response=entry['domain']['response']['text'][0],
            createdate=entry['createdAt'],
            status="Waiting for Approval"
        )
    response_instance.save()
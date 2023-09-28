# from datetime import datetime
# from pymongo import MongoClient

# # Define the MongoDB connection string
# username = 'ruby-admin'
# password = 'rubyadmin123'
# host = 'localhost'
# port = '27017'
# database_name = 'rasa-ruby'
# mongo_uri = f'mongodb://{username}:{password}@{host}:{port}/{database_name}'
# collection_name = 'conversations'

# class Conversation:
#     def __init__(self, sender_id: str, events: list, timestamp: datetime):
#         self.sender_id = sender_id
#         self.events = events
#         self.timestamp = timestamp
    
#     def to_dict(self):
#         return {
#             'sender_id': self.sender_id,
#             'events': self.events,
#             'timestamp': self.timestamp
#         }
    
#     @classmethod
#     def from_dict(cls, data):
#         return cls(
#             sender_id=data['sender_id'],
#             events=data['events'],
#             timestamp=data['timestamp']
#         )
    
#     @staticmethod
#     def save(conversation):
#         client = MongoClient(mongo_uri)
#         db = client[database_name]
#         collection = db[collection_name]
#         collection.insert_one(conversation.to_dict())
    
#     @staticmethod
#     def find_all():
#         client = MongoClient(mongo_uri)
#         db = client[database_name]
#         collection = db[collection_name]
#         return [Conversation.from_dict(conversation) for conversation in collection.find()]


from django.contrib import admin
from .models import Response
from more_admin_filters import ChoicesDropdownFilter
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import ruamel.yaml
import io

import os

# Get the current directory of admin.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go two folders up
three_folders_up = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('intent', 'message', 'response', 'createdate', 'status')  # Display fields in the admin table
    list_filter = [('status', ChoicesDropdownFilter)]
    search_fields = ('intent','message', 'response')

    actions = ['approve_selected_records']  # Add your custom action here


    def update_domain(self, document, path):
        yaml = ruamel.yaml.YAML()

        document = document['domain']
        intent = document['intent']
        utter = document['response']['utterResponse']
        response = document['response']['text'][0]

        print("Response updated for {}: {}".format(intent, response))

        with open(path+"domain.yml", "r+") as read_file:
            contents = yaml.load(read_file)
            contents["responses"][utter] = [{'text': response}]

            contents["intents"] = list(contents["intents"])
            contents["intents"].append(intent)

        with open(path+"domain.yml", 'w') as f:
            yaml.dump(contents, f) 

    def update_stories(self, document, path):
        yaml = ruamel.yaml.YAML()

        document = document['stories']
        story_name = document['storyName']
        intent = document['steps'][0]['name']
        action = document['steps'][1]['name']
        
        new_data = {
            'story': story_name,
            'steps': [{'intent': intent},{'action': action}]
            }
        with open(path+"data/stories.yml", "r+") as read_file:
            contents = yaml.load(read_file)
            contents["stories"] = list(contents["stories"])
            contents["stories"].append(new_data)

        with open(path+"data/stories.yml", 'w') as f:
            yaml.dump(contents, f)

    
    def literalize_list(self, v):
        yaml = ruamel.yaml.YAML()
        assert isinstance(v, list)
        buf = io.StringIO()
        yaml.dump(v, buf)
        return ruamel.yaml.scalarstring.LiteralScalarString(buf.getvalue())


    def transform_value(self, d, key, transformation):
        """recursively walk over data structure to find key and apply transformation on the value"""
        if isinstance(d, dict):
            for k, v in d.items():
                if k == key:
                    d[k] = transformation(v)
                else:
                    self.transform_value(v, key, transformation)
        elif isinstance(d, list):
            for elem in d:
                transform_value(elem, key, transformation)

    def update_nlu(self, document, path):
        yaml = ruamel.yaml.YAML()
        
        document = document['nlu']
        intent = document['intentName']
        examples = document['examples']

        # data = add_new_intent(intent, examples)
        data = {}
        data['intent'] = intent
        data['examples'] = examples

        self.transform_value(data, 'examples', self.literalize_list)

        with open(path+"data/nlu.yml", "r+") as read_file:
            contents = yaml.load(read_file)
            contents['nlu'].append(data)
            

        with open(path+"data/nlu.yml", 'w') as f:
            yaml.dump(contents, f)
        

    def approve_selected_records(self, request, queryset):
        # Update the status of selected records to 'Approved'
        
        rows_updated = queryset.update(status='Approved')
        
        self.message_user(
            request,
            f'{rows_updated} record(s) have been approved.',
        )
        
        #connect to MongoDB Atlas
        uri = "mongodb+srv://rubyadmin123:rubyadmin123@cluster0.scmw523.mongodb.net/?retryWrites=true&w=majority"
        

        path=three_folders_up+"/"
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
        # Perform your custom action here for each approved record
        for intent in queryset:
            # Your custom action code here
            documents = collection.find({'domain.intent': str(intent)})
            for document in documents:
                self.update_domain(document, path)
                self.update_stories(document, path)
                self.update_nlu(document, path)
        client.close()
            
            

    
    approve_selected_records.short_description = "Approve selected records"  # Description for the admin UI

    

# Register your models here.
admin.site.register(Response, ResponseAdmin)

admin.site.site_header  =  "RUBY Administration"
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import openai
import os
import json

# Initialize the OpenAI API client with your API key
# openai.api_key = "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"

openai.api_type = "azure"
openai.api_base =  "https://azureaisouthcentral.openai.azure.com" 
openai.api_version = "2023-03-15-preview" 
openai.api_key = "ee182f58a98743c78bd364c566f2ae8b"

deployment_name = "ChatGPTTurbo"
conversation=[{"role": "system", "content": "You are a helpful assistant."}]

class ActionAnswerQuestion(Action):

    def name(self) -> Text:
        return "action_answer_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the user's question from the latest user message
        user_message = tracker.latest_message.get('text', "")
        print(tracker.latest_message.get("intent_text"))
        # Use Rasa to determine if the user's question can be answered by an intent
        intent = tracker.latest_message.get('intent').get('name')
        print(user_message)
        if intent == "greet":
            response = "Hello!"
        elif intent == "goodbye":
            response = "Goodbye!"
        elif intent == "ask_question":
        # Use OpenAI to generate a response
            response = generate_openai_response(user_message)
        elif intent == "nlu_fallback":
        # Use OpenAI to generate a response
            response = generate_openai_response(user_message)
        else:
            response = "I'm sorry, I don't understand your question."

        dispatcher.utter_message(text=response) 

def generate_openai_response(prompt: str) -> str:
    conversation.append({"role": "user", "content": prompt})
    response =  openai.ChatCompletion.create(
        deployment_id=deployment_name, 
         messages=conversation
    )
    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    message = response['choices'][0]['message']['content'].replace('\n', ' ')

    return message

# Define a custom action that generates a response using the OpenAI GPT-3 API
class ActionGenerateResponse(Action):
    def name(self) -> Text:
        return "action_generate_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the user's message from the tracker
        message = tracker.latest_message.get('text', '')
        #message = "Who is the president of USA?"

        # Generate a response using the OpenAI GPT-3 API
        response = openai.Completion.create(
            engine="davinci",
            prompt=message,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the generated response from the OpenAI API response
        response_text = response.choices[0].text.strip()

        print(response_text)

        # Send the response back to the user via the dispatcher
        dispatcher.utter_message(text=response_text)

        return []
   
# def main():
#     message = "Who is the president of the Philippines?"

#     # Generate a response using the OpenAI GPT-3 API
#     response = openai.Completion.create(
#         engine="davinci",
#         prompt=message,
#         max_tokens=1024,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )

#     # Extract the generated response from the OpenAI API response
#     response_text = response.choices[0].text.strip()
#     print(response_text)

# if __name__== "__main__":
#     main()

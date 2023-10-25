import os
import openai
from utils import load_json, save_json

# Define the OpenAI key from the environment variable
openai.api_key = os.environ['OPENAI_API_KEY']


def transcribe_voice(voice):
    transcript = openai.Audio.transcribe(
        "whisper-1",
        voice, 
        temperature = 0.0,
    )
    return transcript['text']

def response_object(context):
    response = openai.ChatCompletion.create(
        temperature=0.0,
        model="gpt-3.5-turbo-16k-0613",
        messages=context
    )
    return response["choices"][0]["message"]

def chatgpt(user_id, user_message):
    # load messages history json
    messages_history = load_json("messages_history.json")     
    # Append the new user message to the message history
    messages_history.append({"role": "user", "content": user_message})
    
    # Get the system message + the most recent messages
    context = [messages_history[0]] + messages_history[-10:]

    # get chat completion response object
    resp_object = response_object(context)
    # append response object to message history
    messages_history.append(resp_object)
    
    # save message history back to the json file
    save_json(messages_history, "messages_history.json")

    return resp_object["content"]



    

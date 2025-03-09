import json
import requests
requests.packages.urllib3.disable_warnings() 
api_key = "AIzaSyAkwVWJqOPPAIPYKctH9Y8XuVHrR9I5JwQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
session = requests.Session()
session.verify = False

safetySettings =  [
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

def update_history(chat_history):
    chat_contents = []
    for chat_pair in chat_history:
        chat_contents.append({
            "role": "user",
            "parts": [
                {
                    "text": chat_pair[0]
                }
            ]
        })
        chat_contents.append({
            "role": "model",
            "parts": [
                {
                    "text": chat_pair[1]
                }
            ]
        })
    return chat_contents

def chatbot(chat_history, session, safetySettings, question):
    contents = update_history(chat_history)
    contents.append({
        "role": "user",
        "parts": [
            {
                "text": question
            }
        ]
    })
    payload = json.dumps({
        "contents": contents,
        "safetySettings": safetySettings
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = session.request("POST", url, headers=headers, data=payload)
    answer = json.loads(response.text)['candidates'][0]['content']['parts'][0]['text']
    chat_history.append((question, answer))
    return response, chat_history

def correcting_spelling(question, session, chat_history):
    question = """You are my girl friend. You are flirting me. Let's talk with me like my girl friend.\nMy talk: """+question
    response, chat_history = chatbot(chat_history, session, safetySettings, question)
    try:
        answer = response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        answer = "Connection error!!!"
    return answer, chat_history

if __name__=='__main__':
    chat_history = []
    while True:
        print('-'*30)
        question = input("User: ")
        response, chat_history = correcting_spelling(question, session, chat_history)
        print("Assistant: ")
        print(response)
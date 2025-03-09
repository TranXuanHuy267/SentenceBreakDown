import json

api_key = "AIzaSyAkwVWJqOPPAIPYKctH9Y8XuVHrR9I5JwQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}";

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

def qa_gemini(question, session):
    
    payload = json.dumps({
      "contents": [
        {
          "parts": [
            {
              "text": question
            }
          ]
        }
      ],
      "safetySettings": safetySettings,
    })
    headers = {
      'Content-Type': 'application/json'
    }
    
    response = session.request("POST", url, headers=headers, data=payload)
    return response

def correcting_spelling(question, session):
    prompt = """You are my girl friend. You are flirting me. Let's talk with me like my girl friend. My talk: """+question
    response = qa_gemini(prompt, session)
    a = json.loads(response.text)
    if 'candidates' in a.keys():
        answer = a['candidates'][0]['content']['parts'][0]['text']
    else:
        answer = "Connection error!!!"
    return answer

if __name__=='__main__':
    import requests
    requests.packages.urllib3.disable_warnings() 
    session = requests.Session()
    session.verify = False
    question = "Hello"
    answer = correcting_spelling(question=question, session=session)
    print(answer)



import json
import requests
requests.packages.urllib3.disable_warnings()
import streamlit as st
import requests
from ASR.whisper.asr import speech_to_text, prepare_asr
from TTS.tts import text_to_speech, prepare_tts
import nltk

if "prompt_2" not in st.session_state:
    st.session_state.prompt_2 = 0

if "prompt_3" not in st.session_state:
    st.session_state.prompt_3 = 0

def clear_history():
    st.session_state.chat_history = []
    st.session_state.chat_history_view = []
    st.session_state.questions = 0
    st.session_state.list_prompt_3 = []

def clear_recent_history():
    x = len(st.session_state.chat_history)
    print("Len chat history view:", len(st.session_state.chat_history_view))
    if x > 0:
        st.session_state.chat_history = st.session_state.chat_history[:-1]
        temp = []
        list_prompt_3_new = []
        for i, j in enumerate(st.session_state.list_prompt_3):
            if j+1 != x:
                temp.append(st.session_state.chat_history_view[i])
                list_prompt_3_new.append(j)
        st.session_state.chat_history_view = temp
        print("List value:", st.session_state.list_prompt_3)
        st.session_state.list_prompt_3 = list_prompt_3_new
        print("List value:", st.session_state.list_prompt_3)
    print("Len chat history view after:", len(st.session_state.chat_history_view))


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history_view = []
    st.session_state.asr = prepare_asr()
    st.session_state.tts = prepare_tts()
    st.session_state.questions = 0
    st.session_state.list_prompt_3 = []
    st.session_state.role = ""
    st.session_state.is_input_role_time = 0
    nltk.download('punkt')

def asr_input():
    st.session_state.prompt_2 = speech_to_text(st.session_state.asr[0], 
                                               st.session_state.asr[1], 
                                               st.session_state.asr[2], 
                                               micro=True)

def tts_output():
    text_to_speech(st.session_state.tts[0], st.session_state.tts[1], st.session_state.chat_history[-1][1])

def check_answer():
    st.session_state.prompt_3 = 1

def input_role():
    st.session_state.chat_history = []
    st.session_state.chat_history_view = []
    st.session_state.is_input_role_time = 1
    st.session_state.questions = 0
    st.session_state.list_prompt_3 = []
    st.session_state.prompt_3 = 0

st.title("Simple Chat Gemini")
with st.sidebar:
    st.title("Chatbot")
    st.markdown("""Hello, this is a simple chatbot that uses the Gemini API.""")
    st.button("Clear History", key="clear_history", on_click=clear_history)
    st.button("Clear Recent History", key="clear_recent_history", on_click=clear_recent_history)
    st.button("Listen", key="listen", on_click=asr_input)
    st.button("Read the answer", key='read_the_answer', on_click=tts_output)
    st.button("Question answering", key="qa", on_click=check_answer)
    st.button("Input role", key="input_role", on_click=input_role)


api_key = "AIzaSyAAZ-Of6RrlXmp6Epqap4TT8pGbnNG4Qvc"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
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
session = requests.Session()
session.verify = False

def update_history():
    chat_contents = []
    for chat_pair in st.session_state.chat_history:
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


def show_beautiful(output):
    if "\n\n" in output.strip():
        output = output.split("\n\n")
        output = ['<b>' + i.replace(':', "</b>:") for i in output]
        output = [i.replace('\n', '.\n').replace('..', '.') for i in output]
        output = '\n\n'.join(output)
    else:
        output = output.split("\n")
        output = ['<b>' + i.replace(':', "</b>:") if ':' in i else i for i in output]
        output = [i + '.' for i in output if i[-1] not in ['.', ',', '!']]
        output = '\n'.join(output)
    return output

def gemini_grammar(text):
    ques = f"""Correct the grammar of the following sentence:\nOriginal: {text}\nFixed Grammar:"""
    response = qa_gemini(ques, session)
    a = json.loads(response.text)
    output = a['candidates'][0]['content']['parts'][0]['text']
    if 'Fixed Grammar:' in output:
        output = output[output.index('Fixed Grammar:')+len('Fixed Grammar:'):]
    return output

def gemini_extraction(text):
    ques = f"""Your task is to extract C1-C2 vocabularies from the below context. Your responses are many lines of the C1-C2 vocabulary in the format:\n"Vocabulary": Meaning of this "Vocabulary"\nSentence: Sentence which has this "Vocabulary"\n\nContext: """+text
    response = qa_gemini(ques, session)
    a = json.loads(response.text)
    output = a['candidates'][0]['content']['parts'][0]['text']
    if 'Fixed Grammar:' in output:
        output = output[output.index('Fixed Grammar:')+len('Fixed Grammar:'):]
    return output

def extract_qa(context):
    ques_num = int(len(context)/250)
    if ques_num > 1:
        keyword = f"{ques_num} pairs"
    else:
        keyword = "a pair"
    ques = f"""Extract {keyword} of question - short answer (answer is no more than two words and/or a number, answer must appear in the following context) about the general knowledge from the following context. \nContext:"""+context+"""\n\nQuestion: <<Question>>\nAnswer: <<Answer>>\n\n"""
    response = qa_gemini(ques, session)
    a = json.loads(response.text)
    output = a['candidates'][0]['content']['parts'][0]['text']
    output = output.replace("*", "")
    qas = output.split("\n\n")
    qas = [qa.split("\n") for qa in qas if "\n" in qa]
    if len(qas) > 0:
        qas = [[i[i.index(":")+1:].strip() if ":" in i else i for i in qa] for qa in qas]
        qa_text = "\n".join([f"{i+1}. {qa[0]}" for i, qa in enumerate(qas)])
    else:
        qas = [[]]
        qa_text = "There is no question extracted from the above answer."
    return qas, qa_text

def chatbot(session, safetySettings, question, prompt):
    contents = update_history()
    # attend
    correct_question = gemini_grammar(question)
    # all_question = """You are the Ielts examiner. You will ask me a Ielts speaking question, listen to my answer and score my answer. Then, you give me the feedback and give me another question. Now you are talking to me. Let's start.\nMy talk: """ + question
    # all_question = """You are the Ielts examiner. You have two options to answer my question:\n1. If I say hello to you, let's respond hello to me and give me a Ielts speaking question.\n2. If I answer an Ielts speaking question from you, let's score my answer, give some feedback for me. If the score is higher than 7, let's give me another Ielts speaking question, otherwise remind me try again with current question.\n\nMy talk: """ + question
    # all_question = """You are Uchiha Sasuke. Now you are talking to me.\nMy talk:""" + question
    # all_question = """You are a gym instructor, you know everything about nutrition to have a beautiful, toned, fat-free body. Now you are talking to me.\nMy talk:""" + question
    # all_question = """<<SYS>>You have got 9.0 Ielts. You have experienced the process from zero to 9.0 Ielts after training all skill of reading, listening, speaking, writing in Ielts. Now you are talking to me.<<SYS>>\nQuestion: """+question+"\nAnswer: "
    # all_question = """<<SYS>>You are a physiology doctor. You know everything about the male penis, the femail clitoris, the ways to stimulate them and make them satisfied. Now you are having a conversation with me.<<SYS>>\nQuestion: """+question+"\nAnswer: "
    # all_question = """<<SYS>>Bạn là bạn trai của Linh. Bạn không phải là mô hình ngôn ngữ của Google. Bạn đang được nói chuyên với tôi, tôi chính là Linh.<SSYS>>\Câu hỏi: """+question+"\nCâu trả lời: "
    # all_question = """<<SYS>>You are a gym instructor, you know everything about nutritions and eating schedules to have a beautiful, toned, fat-free body. Now you are having a conversation with me.<<SYS>>\nQuestion: """+question+"\nAnswer: "
    # all_question = """<<SYS>>You are the best leader in the world. You have inspired so many people and made them believe in you. You are a person with great responsibility, everyone believes in you. You are someone who dares to stand up to every challenge that comes to you and your team. You have conquered people one by one, from nothing to have thousands and thousands of people following you and working for you. Now you are talking to me.<<SYS>>\nQuestion: """+question+"\nAnswer: "
    # all_question = """<<SYS>>You are a driven person with clear goals. You know how to talk to people, know how to treat people, know when to speak up, when to stay silent. You know when you need to make the right decision, when you need someone decisive, when you need to persevere and not give up. Now you are talking to me.<<SYS>>\nQuestion: """+question+"\nAnswer: "
    # all_question = """<<SYS>>You are a trusted adult and have many experiences in bed. You know all the ways to have a wonderful night with your girlfriend. For her, the first time is the most important and you need to know what to do when sleeping with her. Now you are talking to me.<<SYS>>\nQuestion: """+question+"\nAnswer: "
    # all_question = """Let's fix my speaking words to be more concise. You can give me some feedbacks to improve my grammar, my vocabulary.\nQuestion: """+question+"\nAnswer: "
    # all_question = """You know everything about the general knowledge of the following contents:\n+ Characteristics of the number system\n+ Digital design process\n+ Types of digital chips\n+ Basic terms\n+ Number systems\n+ Convert between number systems\n+ Numerical representations\n+ Boolean algebra\nCan you provide more details about our questions?\nQuestion: """+question+"""\nAnswer: """
    
    if prompt.strip() != '':
        all_question = '<SYS>'+prompt+'<SYS>'+'Question: '+question+'\nAnswer: '
    else:
        all_question = question
    contents.append({
        "role": "user",
        "parts": [
            {
                "text": all_question
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

    if "response:" in answer:
        answer = answer[answer.index(':')+1:].strip()

    # extend
    extract_question, extract_question_text = extract_qa(answer)
    extracted_word = gemini_extraction(answer)
    while '\n\n' in extracted_word:
        extracted_word = extracted_word.replace("\n\n", '\n')
    extracted_word = extracted_word.replace('\n', '\n\n').replace('"', "**")
    view_answer = "**Grammar Correction**: " + correct_question.strip() + "\n\n**Answer**:\n\n"+answer+"\n\n**Question**:\n\n"+extract_question_text
    new_answer = "**Grammar Correction**: " + correct_question.strip() + "\n\n**Answer**:\n\n"+answer +"\n\n**Question**:\n\n"+extract_question_text+ '\n\n**New words**:\n\n'+ extracted_word
    st.session_state.chat_history.append((question, answer))
    st.session_state.chat_history_view.append((question, view_answer))
    st.session_state.questions = extract_question_text
    st.session_state.list_prompt_3.append(st.session_state.prompt_3)
    return new_answer

def answer_question(session, safetySettings, question):
    contents = update_history()
    all_question = "Evaluate the following answer(s) is/are correct or not from the following context and questions:"+"\n\n**Context**:\n\n"+st.session_state.chat_history[-1][1]+"\n\n**Question**:\n\n"+st.session_state.questions+"\n\nAnswer: "+question
    contents.append({
        "role": "user",
        "parts": [
            {
                "text": all_question
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

    if "response:" in answer:
        answer = answer[answer.index(':')+1:].strip()

    st.session_state.chat_history_view.append((question, answer))
    st.session_state.list_prompt_3.append(st.session_state.prompt_3*len(st.session_state))
    return answer

for message in st.session_state.chat_history_view:
    with st.chat_message("user"):
        st.markdown(message[0])
    with st.chat_message("ai"):
        st.markdown(message[1])

if st.session_state.prompt_2:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(st.session_state.prompt_2)
    response = chatbot(session, safetySettings, st.session_state.prompt_2, st.session_state.role)

    with st.chat_message("ai"):
        st.markdown(response)
    st.session_state.prompt_2 = 0

if prompt := st.chat_input("What is up?"):
    if st.session_state.is_input_role_time == 0:
        if st.session_state.prompt_3:
            st.session_state.prompt_3 = 0
            with st.chat_message("user"):
                st.markdown(prompt)
            response = answer_question(session, safetySettings, prompt)
            with st.chat_message("ai"):
                st.markdown(response)
        else:
            with st.chat_message("user"):
                st.markdown(prompt)
            response = chatbot(session, safetySettings, prompt, st.session_state.role)
            with st.chat_message("ai"):
                st.markdown(response)
    else:
        st.session_state.role = prompt
        st.session_state.is_input_role_time = 0

if st.session_state.role != '':
    with st.sidebar:
        st.title("New Role")
        st.markdown(st.session_state.role)
import os 
from openai import OpenAI
import json
import time

with open("new_json_files/test.json", 'r', encoding='utf-8') as f:
    test1 = json.load(f)
    test1 = {
        "input": "I hope that my teacher will take into account the fact that I was ill just before the exam",
        "output": [
            {
                "leaf text": "I",
                "id": "1",
                "info": "Subject of the main clause."
            },
            {
                "leaf text": "hope",
                "id": "2",
                "info": "Verb of the main clause."
            },
            {
                "leaf text": "that",
                "id": "3",
                "info": "Introduces the object clause."
            },
            {
                "leaf text": "my",
                "id": "4",
                "info": "Possessive determiner modifying 'teacher'."
            },
            {
                "leaf text": "teacher",
                "id": "5",
                "info": "Meaning 'giáo viên'"
            },
            {
                "leaf text": "will",
                "id": "6",
                "info": "Auxiliary verb indicating future tense."
            },
            {
                "leaf text": "take into account",
                "id": "7 8 9",
                "info": "Meaning 'cân nhắc, xem xét, tính đến'"
            },
            {
                "leaf text": "the",
                "id": "10",
                "info": "Definite article modifying 'fact'."
            },
            {
                "leaf text": "fact",
                "id": "11",
                "info": "Meaning 'sự thật'"
            },
            {
                "leaf text": "that",
                "id": "12",
                "info": "Relative pronoun introducing the clause."
            },
            {
                "leaf text": "I",
                "id": "13",
                "info": "Subject of the relative clause."
            },
            {
                "leaf text": "was",
                "id": "14",
                "info": "Verb of the relative clause."
            },
            {
                "leaf text": "ill",
                "id": "15",
                "info": "Meaning 'ốm'"
            },
            {
                "leaf text": "just",
                "id": "16",
                "info": "Adverb modifying 'before'."
            },
            {
                "leaf text": "before",
                "id": "17",
                "info": "Preposition indicating time."
            },
            {
                "leaf text": "the",
                "id": "18",
                "info": "Definite article modifying 'exam'."
            },
            {
                "leaf text": "exam",
                "id": "19",
                "info": "Meaning 'bài kiểm tra'"
            }
        ]
    }
    test1_string = json.dumps(test1, indent=2)

with open("new_json_files/test2.json", 'r', encoding='utf-8') as f:
    test2 = json.load(f)
    test2 = {
        "input": "take your mask off",
        "output": [
            {
                "text": "take off",
                "id": "1 4",
                "info": "Meaning 'cởi ra'"
            },
            {
                "text": "your",
                "id": "2",
                "info": "This is a possessive pronoun modifying 'mask'."
            },
            {
                "text": "mask",
                "id": "3",
                "info": "Meaning 'khẩu trang'"
            }
        ]
    }
    test2_string = json.dumps(test2, indent=2)


system_prompt = """
You are an English analyzer. You are provided with an English sentence, phrase, or paragraph. Your task is to analyze the sentence structure by identifying the grammatical role of each token in the input. For each token (or group of tokens that form a meaningful unit), create a JSON object with the following keys:
{
    "text": The exact text of the token or phrase,
    "id": The text's id (or a space-separated list of token ids if the token spans multiple words),
    "info": A short brief description of the grammatical function.
    "mean": A short meaning of the text.
}
Format your output as a list containing these JSON objects. Do not include any additional commentary or information.
""".strip() + f"""
Here are some example you can refer to:
Example 1:
Input: {json.dumps(test1['input'], indent=2)}
Output:
{json.dumps(test1['output'], indent=2)}

Example 2:
Input: {json.dumps(test2['input'], indent=2)}
Output:
{json.dumps(test2['output'], indent=2)}
"""

print(system_prompt)

# os.environ['OPENAI_API_KEY'] = "sk-proj-B4FSqO3dGff3kJNOcQEGT3BlbkFJGwl36VlJgi5Gn0MADw4d"
os.environ['OPENAI_API_KEY'] = "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"
client = OpenAI()

prompt = "There is one all-important law of human conduct."

start_time = time.time()
"""completion = client.chat.completions.create(
    model="gpt-4-turbo",
    # model="o1-mini",
    messages=[
        {
            "role": "user",
            "content":  system_prompt + "\n\n" + prompt
        } 
    ]
)"""

completion = client.chat.completions.create(
    model="gpt-4-turbo",
    # model="o1-mini",
    messages=[
        {
            "role": "system",
            "content":  system_prompt
        },
        {
            "role": "user",
            "content":  prompt
        } 
    ]
)
end_time = time.time()
answer = completion.choices[0].message.content
print(answer)
print("Time (s): " + str(end_time-start_time))


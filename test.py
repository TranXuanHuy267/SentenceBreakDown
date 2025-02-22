import os 
from openai import OpenAI
import json
import time

with open("json_files/test.json", 'r', encoding='utf-8') as f:
    test1 = json.load(f)
    test1_string = json.dumps(test1, indent=2)

with open("json_files/test2.json", 'r', encoding='utf-8') as f:
    test2 = json.load(f)
    test2_string = json.dumps(test2, indent=2)


system_prompt = """You are an English analyzer. You are given an English phrase or a sentence or a paragraph. Your task is to extract the """
system_prompt = """
You are an English analyzer. You are provided an English phrase or a sentence or a paragraph. Your task is to analyze all of the necessary informations in the given English words.
Thought: While traversing through the given input, analyze the sentence structure and identify key grammatical components.
	Terms include subject, verb, object clause, and their subcomponents such as relative clauses, noun phrases, and phrasal verbs.
	Terms should be as accurate as possible.

Format your output as a JSON, not including any unnecessary information. Each element of the JSON represents a grammatical component, like the following:
{
    "subject": "The subject of the sentence",
    "verb": "The main verb of the sentence",
    "object_clause": "The object clause of the verb",
    "subcomponents": {
        "relative_clause": "The relative clause within the object clause",
        "noun_phrase": "The noun phrase acting as the object",
        "phrasal_verb": "The phrasal verb within the object clause"
    }
}""".strip() + f"""
Here are some example you can refer to:
Example 1:
Input: {test1['text']}
Output:
{test1_string}


Example 2:
Input: {test2['text']}
Output:
{test2_string}
"""



# os.environ['OPENAI_API_KEY'] = "sk-proj-B4FSqO3dGff3kJNOcQEGT3BlbkFJGwl36VlJgi5Gn0MADw4d"
os.environ['OPENAI_API_KEY'] = "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"
client = OpenAI()

prompt = "There is one all-important law of human conduct."

start_time = time.time()
completion = client.chat.completions.create(
    # model="gpt-4-turbo",
    model="o1-mini",
    messages=[
        {
            "role": "user",
            "content": system_prompt+"\n\n"+prompt
        } 
    ]
)
end_time = time.time()
answer = completion.choices[0].message.content
print(answer)
print("Time (s): " + str(end_time-start_time))


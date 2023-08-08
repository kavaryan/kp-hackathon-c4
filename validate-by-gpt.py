import json
import re
import openai
import matplotlib.pyplot as plt
from tqdm import tqdm

openai.api_key_path = 'openai_api_key.txt'  # Set your OpenAI API key here

META_LABELS = ['I', 'R', 'U', 'D']
MODEL = 'gpt-3.5-turbo'

# Read the jsonl file
class_names = []
with open('tutorial-ontoclean-labels.jsonl', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line_d = json.loads(line)
        class_names.append(line_d['classname'])

# Process each line
for class_name in tqdm(class_names):
    # Query ChatGPT
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f'Provide OntoClean metalabels (Identity, Unity, Rigidity, Dependence, such as +I, -D, etc.) for the class "{class_name}":'},
        ],
        max_tokens=250,
        temperature=0
    )
    
    # chatgpt_labels = response.choices[0].text.strip()
    pred_labels = response.choices[0]['message']['content']
    print('='*20)
    print(f'Class name: {class_name}')
    print(f'Reference labels: {metalabels}')
    print(f'{MODEL} output:', pred_labels)
    print()
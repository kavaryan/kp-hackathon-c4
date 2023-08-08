import json
import re
import openai
import matplotlib.pyplot as plt
from tqdm import tqdm

openai.api_key_path = 'openai_api_key.txt'  # Set your OpenAI API key here

META_LABELS = ['I', 'R', 'U', 'D']
MODEL = 'gpt-3.5-turbo'


prompt_short_context = 'Provide OntoClean metalabels (Identity, Unity, Rigidity, Dependence, such as +I, -D, etc.) for the class "{class_name}":'
prompt_full_context = """Provide OntoClean metalabels (Identity, Unity, Rigidity, Dependence, such as +I, -D, etc.) for the class "{class_name}":

Rigidity = 'Rigidity is based on the notion of essence. A concept is essential for an instance iff it is necessarily an instance of this concept, in all worlds and at all times. Iff a concept is essential to all of its instances, the concept is called rigid and is tagged with +R. Iff it is not essential to some instances, it is called non-rigid, tagged with -R. An anti-rigid concept is one that is not essential to all of its instances. It is tagged ∼R. '
Unity='Unity is about "What is part of something and what is not?" This answer is given by an Unity Criterion (UC), which is true for all parts of an instance of this concept, and for nothing else. '
Identity='Identity. A concept with Identity is one, where the instances can be identified as being the same at any time and in any world, by virtue of this concept. This means that the concept carries an Identity Criterion (IC). It is tagged with +I, and with -I otherwise. It is not important to answer the question of what this IC is (this may be hard to answer), it is sufficient to know that the concept carries an IC.'
Dependence='Dependence. A concept C1 is dependent on a concept C2 (and thus tagged +D), iff for every instance of C1 an instance of C2 must exist."""

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
            {'role': 'user', 'content': prompt_full_context.format(class_name=class_name)},
        ],
        max_tokens=250,
        temperature=0
    )
    
    # chatgpt_labels = response.choices[0].text.strip()
    pred_labels = response.choices[0]['message']['content']
    print('='*20)
    print(f'Class name: {class_name}')
    # print(f'Reference labels: {metalabels}')
    print(f'{MODEL} output:', pred_labels)
    print()
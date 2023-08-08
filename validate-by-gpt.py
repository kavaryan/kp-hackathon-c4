import json
import re
import openai
import matplotlib.pyplot as plt

openai.api_key_path = 'openai_api_key.txt'  # Set your OpenAI API key here

# Load the OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

META_LABELS = ['I', 'R', 'U', 'D']

def parse_metalabels_str(s):
    """ Parse a string representation of meta labels into a dictionary.

    Example: '+I-D' --> {'I': '-I', 'D': '-D'}
    """
    ret = dict()
    assert re.match(s, '(^[-|\+][IRUD])+$')
    for i in range(1, len(s), 2):
        ret[s[i].upper()] = s[i-1:i+1].upper()
    return ret


# Read the jsonl file
with open('file.jsonl', 'r') as f:
    lines = f.readlines()

results = {label: [0, 0] for label in META_LABELS}  # Correct/Incorrect counts for each metalabel

# Process each line
for line in lines:
    data = json.loads(line)
    class_name = data['name']
    metalabels = data['metalabels']
    metalabels = parse_metalabels_str(metalabels)

    # Query ChatGPT
    response = openai.Completion.create(
      engine="davinci",
      prompt=f"Provide OntoClean metalabels for the class '{class_name}':",
      max_tokens=100
    )
    chatgpt_labels = response.choices[0].text.strip()

    # Compare ChatGPT's response with the given metalabels
    for label in META_LABELS:
        expected = metalabels.get(label)
        if expected and expected in chatgpt_labels:
            results[label][0] += 1  # Correct
        else:
            results[label][1] += 1  # Incorrect

# Plot the results
fig, axs = plt.subplots(2, 2)
labels = ['Correct', 'Incorrect']
for idx, label in enumerate(META_LABELS):
    ax = axs[idx//2, idx%2]
    ax.pie(results[label], labels=labels, autopct='%1.1f%%')
    ax.set_title(f'Metalabel {label}')

plt.show()

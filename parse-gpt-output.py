import json
import re

from matplotlib import pyplot as plt


META_LABELS = ['I', 'R', 'U', 'D']

with open('tutorial-output.txt') as f:
    lines = f.readlines()

def parse_metalabels_str(s):
    """ Parse a string representation of meta labels into a dictionary.

    Example: '+I-D' --> {'I': '-I', 'D': '-D'}
    """
    ret = dict()
    if not re.match(r'^([-+~][IRUD])+$', s):
        raise ValueError(f'Bad input: {s}')
    for i in range(1, len(s), 2):
        ret[s[i].upper()] = s[i-1:i+1].upper()
    return ret

predictions = dict()
class_name, metalabels = None, ''
for l in lines:
    l = l.strip()
    if l.startswith('Class name:'):
        class_name = l.replace('Class name: ', '', 1)
        metalabels = ''
    else:
        for metalabel in ['Identity', 'Unity', 'Rigidity', 'Dependence']:
            if l.startswith(f'- {metalabel} ('):
                metalabels += l.replace(f'- {metalabel} (', '', 1)[:2]

    if class_name is not None:
        predictions[class_name] = metalabels

# Read the jsonl file
ground_truth = dict()
with open('tutorial-ontoclean-labels.jsonl', 'r') as f:
    lines = f.readlines()
    for line in lines:
        data = json.loads(line)
        ground_truth[data['classname']] = data['metalabels']
        
results = {label: [0, 0] for label in META_LABELS}  # Correct/Incorrect counts for each metalabel

for class_name, pred_labels in predictions.items():
    real_labels = parse_metalabels_str(ground_truth[class_name])
    pred_labels = parse_metalabels_str(pred_labels)
    for label in META_LABELS:
        real_label = real_labels.get(label)
        if real_label and pred_labels.get(label, '') == real_label:
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

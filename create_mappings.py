import json

with open('index.txt') as index:
    id = 0
    label2id = {}
    for i in index:
        i = i.replace('\n', '')
        with open('./data/'+i) as rf:
            data = json.load(rf)
            label2id[id] = data['title']
        id += 1
    with open('label2id.json', 'w') as wf:
        json.dump(label2id, wf, indent=1)

    id2label = {v:k for k, v in label2id.items()}
    with open('id2label.json', 'w') as wf:
        json.dump(id2label, wf, indent=1)

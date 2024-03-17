from tqdm import tqdm
from transformers import BertTokenizerFast
import re
from html2text import html2text as htt
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from tqdm.contrib.concurrent import process_map
import json
import os
import numpy as np

sp_token = BertTokenizerFast.from_pretrained('bert-base-uncased')
label2id = None

def create_data(datapath):
    train_texts, labels = read_dataset(datapath)
    global label2id
    with open('label2id.json') as rf:
        label2id = json.load(rf)
    
    print(f'tokeninizing {len(train_texts)} datapoints. . .')

    with ThreadPoolExecutor(max_workers=cpu_count()-1) as p:
        encoded_texts = np.array(list(tqdm(p.map(encode, train_texts))))

    print('Saving Text Embeddings. . .')
    np.savez('enc_txt.npz', encoded_texts)
    
    with ThreadPoolExecutor(max_workers=cpu_count()-1) as p:
        encoded_labels = np.array(list(tqdm(p.map(encode_label, labels))), dtype=object)
    
    print('Saving Labels . . .')
    np.savez('enc_labs.npz', encoded_labels)

def encode(texts):
    return sp_token.encode(texts, max_length = 256, add_special_tokens=False, truncation=True, padding='max_length')

def encode_label(label):
    encoded = []
    for j in label:
        try:
            encoded.append(label2id[j])
        except:
            pass
    return encoded

def read_dataset(datapath):
    train_texts = []; labels = []
    def clean(text, section=None):
        htt(text)
        text = text.replace('\n', ' ')
        non_pron_text = re.compile('[^\x00-\xFF]+')
        text = non_pron_text.sub(' ', text)
        if section:
            section_title_pattern = re.compile(r'==+.*?==+') # == Section Header ==
            text = section_title_pattern.sub("", text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    with open(f'index.txt') as f:
        for datapoint in tqdm(f.readlines()):
            datapoint = datapoint.replace('\n', '')
            with open(datapath+datapoint) as f:
                datapoint = json.load(f)
                doc_title = clean(datapoint['title'])
                for i in datapoint['sections']:
                    title = doc_title + ': ' + i['title']
                    text = '[CLS]' + title + '[SEP]' + i['content'].lower()
                    section_label = i['links']
                    section_label.append(doc_title.lower())
                    train_texts.append(text)
                    labels.append(section_label)
    
    return train_texts, labels
    
if __name__ == '__main__':
    create_data('./data/')
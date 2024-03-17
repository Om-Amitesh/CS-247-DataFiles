# CS 247 DataFiles
Code that was used to preprocess the entirety of english wikipedia to a section-level granular dataset for document reccomendation for the course project of UCLA CS 247 - Advanced Data Mining.
## Automated Run:
1. Ensure the `enwiki-latest-pages-articles.xml` file is present in the same directory as the `run.sh` file.
2. Follow the instructions on the run.sh file and make changes if necessary.
3. run `bash run.sh` to complete dataset creation.
4. Output files and directories:
    1. `label2id.json` : name implied, a mapping of titles to ids
    2. `id2label.json` : name implied, a mapping of ids to titles
    3. `enc_labs.npz` : npz file consisting of the labels ids.
    4. `enc_txt.npz` : npz file consisting of the tokenized text.
    5. `data/` : directory consisting of json files for each article. 
    6. `index.txt` : index of the `data/` directory that lets you traverse its contents easily.

## How to load data:
Kindly follow instructions in the load_data.py file and use the starter code from there.

# Other:
## How to create section-level aggregated data?
Kindly follow the README file in the PlainTextWikipedia folder.
## How to tokenize?
Kindly use the encoding.py file with updated filepaths to create tokenized embeddings.

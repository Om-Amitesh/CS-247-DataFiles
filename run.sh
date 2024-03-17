# In order to perform this automated run, I'd like you to have the .xml file in the root.
# i.e in the same directory as this run.sh file.

mkdir -p data # This folder would contain json files = the number of articles in wikipedia by the time this program finishes executing.
python3 PlainTextWikipedia/wiki_to_text.py # this creates the json files for each article.

ls data > index.txt # we're going to create an index to traverse our data folder easily.

python3 create_mappings.py # creating a label2id.json
python3 encoding.py # creating an encoding.

echo "Completed dataset creation. \n article-level data can be found at ./data, tokenized embeddings at enc_txt.npz and labels at enc_labs.npz"

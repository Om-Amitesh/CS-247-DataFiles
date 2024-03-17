from dewiki_functions import *

#wiki_xml_file = 'F:/simplewiki-20210401/simplewiki-20210401.xml'  # update this
wiki_xml_file = '/home/skharbanda/wikidata/enwiki-latest-pages-articles.xml'  # update this
json_save_dir = '/home/skharbanda/wikidata/data2/'

if __name__ == '__main__':
    process_file_text(wiki_xml_file, json_save_dir)
from threading import Thread
import json
import re
from html2text import html2text as htt
import wikitextparser as wtp
from threading import Lock

def dewiki(text):
    
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
    
    text = wtp.parse(text)
    sections = text.sections
    sections_data = []
    
    for section in sections:

        title = clean(section.title) if section.title else "Introduction"

        if title in ['External links', 'References', 'Further reading', 'Notes', 'See also'] or section.level > 2:
            continue

        title = clean(section.title) if section.title else "Introduction"

        if len(section.sections) <=  2:
            links = list(set([wiki_link.title.lower() for wiki_link in section.wikilinks]))
            links = [clean(i) for i in links]

            content = htt(section.plain_text())
            content = clean(content, section = section.level)

            extracted_info = dict(title = title, content = content, links = links)
            sections_data.append(extracted_info)

        else:

            section_info = section.get_sections(level = 2, include_subsections = False)

            if len(section_info) > 0 and len(clean(section_info[0].plain_text())) > len(title)+6:
                links = list(set([wiki_link.title.lower() for wiki_link in section_info[0].wikilinks]))
                links = [clean(i) for i in links]

                subsection_title = clean(title + ": " + 'Introduction')

                content = htt(section_info[0].plain_text())
                content = clean(content, section = section.level)
                
                section_only_extraction = dict(
                    title = subsection_title,
                    content = content,
                    links = links
                )
                sections_data.append(section_only_extraction)
            
            subsections = section.sections

            for subsection in subsections:

                if subsection.title != None:

                    if subsection.level == 3:
                        links = list(set([wiki_link.title.lower() for wiki_link in subsection.wikilinks]))
                        links = [clean(i) for i in links]

                        subsection_title = clean(title.strip() + ': ' + subsection.title.strip())

                        content = htt(subsection.plain_text())
                        content = clean(content, section = subsection.level)

                        extracted_info = dict(
                            title = subsection_title,
                            content = content,
                            links = links
                        )
                        sections_data.append(extracted_info)
            

    return sections_data


def analyze_chunk(text):
    try:
        if '<redirect title="' in text:  # this is not the main article
            return None
        if '(disambiguation)' in text:  # this is not an article
            return None
        else:
            title = text.split('<title>')[1].split('</title>')[0]
            title = htt(title)
            if ':' in title:  # most articles with : in them are not articles we care about
                return None
        serial = text.split('<id>')[1].split('</id>')[0]
        content = text.split('</text')[0].split('<text')[1].split('>', maxsplit=1)[1]
        sections = dewiki(content)

        return {'title': title.strip(), 'sections': sections, 'id': serial.strip()}
        
    except Exception as oops:
        print(oops)
        return None


def save_article(article, savedir):
    doc = analyze_chunk(article)
    if doc:
        filename = doc['id'] + '.json'
        # with lock:
        #     with open('/Users/omamitesh/wikidata/gen_title.txt', 'a') as wt:
        #         print(doc['title'], file = wt)
        #     with open('/Users/omamitesh/wikidata/gen_index.txt', 'a') as wi:
        #         print(filename, file = wi)
        print(filename)
        with open(savedir + filename, 'w', encoding='utf-8') as outfile:
            json.dump(doc, outfile, sort_keys=True, indent=1, ensure_ascii=False)


def process_file_text(filename, savedir):
    article = ''
    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            if '<page>' in line:
                article = ''
            elif '</page>' in line:  # end of article
                Thread(target=save_article, args=(article, savedir)).start()
            else:
                article += line + '\n'       
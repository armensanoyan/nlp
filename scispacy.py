import os
import ssl
import json, xmltodict
from collections import Counter, defaultdict
import re
from summa import summarizer, keywords
import scispacy
import spacy
from tika import parser
from tqdm import tqdm
import multiprocessing as mp
from joblib import Parallel, delayed

nlp = spacy.load("en_core_sci_scibert")
num_cores = mp.cpu_count()

def clean_stoping_words(text):
    # text_list = text.split(' ')
    filtered_sentence ='' 

    pattern = re.compile(r"[A-Za-z0-9\-]{3,50}")
    re_text = re.findall(pattern, text)
    
    for word in re_text:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence += word + ' ' 
    return filtered_sentence

def get_vector(string):
    s = nlp(string)
    return s.vector

with open('all_articles.text', 'r') as wo:
    data = wo.read()

cln_data = clean_stoping_words(data)
print('yes')

PATH = os.path.join(os.getcwd(), 'meta.json')
def get_metadata():
    with open(PATH) as f:
        for line in f:
            yield line

# metadata = get_metadata()
# paper_from_metadata(metadata)


# from neo4j import GraphDatabase

# uri = "neo4j://localhost:11005"
# driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))

# def pdf_to_json(file_name):
#     parsed = parser.from_file(os.path.join(os.getcwd(), 'artcles', file_name))
#     whole_data = parsed["metadata"]
#     whole_data['text'] = parsed["content"].replace('\n','')
#     with open(f'jsons/{file_name}.json', 'w', encoding='utf-8') as file:
#         #  file.write(parsed["content"])
#         json.dump(whole_data, file, indent=4, sort_keys=False)


import urllib
def paper_from_metadata():
    for paper in metadata:
        first_paper = json.loads(paper)
        text = first_paper['abstract']
        doc = nlp(text)
        print(doc.ents)
        
        url = f'http://export.arxiv.org/pdf/{first_paper["id"]}.pdf'
        # with urllib.request.urlopen(url) as ur:
        #     s = ur.read()
        pdf_buffer = urllib.request.urlopen(url).read()
        pdf_to_string = parser.from_buffer(pdf_buffer)
        # I'm guessing this would output the html source code ?
        content = pdf_to_string['content'].replace('\n', '').replace('\r','')
        text_doc = nlp(content)
        print('\n\n\n\n')
        print(text_doc.ents)
        print('yes')

# driver.close()

def cleaner(df):
    "Extract relevant text from DataFrame using a regex"
    # Regex pattern for only alphanumeric, hyphenated text with 3 or more chars
    pattern = re.compile(r"[A-Za-z0-9\-]{3,50}")
    df = df.findall(pattern).str.join(' ')
    if limit > 0:
        return df
    else:
        return df


QUERY = 'graphene'
URL = f'http://export.arxiv.org/api/query?search_query=all:{QUERY}&max_results=10'
def scrape_articles_by_query():
    xml_scraped = urllib.request.urlopen(URL).read()
    json_scraped = xmltodict.parse(xml_scraped)['feed']['entry']
    all_articles = ''
    counter = 0
    for meta_article in json_scraped:
        url = meta_article['id'].replace('abs','pdf') +'.pdf'
        context = ssl._create_unverified_context()
        # urllib.urlopen("https://no-valid-cert", context=context)
        pdf_buffer = urllib.request.urlopen(url, context=context).read()
        pdf_to_string = parser.from_buffer(pdf_buffer)
        article_text = pdf_to_string['content'].replace('\n', ' ').replace('\r', '')
        # text_doc = nlp(article_text)
        all_articles += article_text
        # key words from article
        # ents = text_doc.ents

        # summarizer
        # summarizer.summarize(article_text)
        counter +=1
        print(counter)
        # print(ents)
    nlp_text = nlp(all_articles[:100000])
    ents = nlp_text.ents
    print('END')
# scrape_articles_by_query()



print('json_scraped: ', json_scraped)
print('yes')
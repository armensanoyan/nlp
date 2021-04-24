
import os
import ssl
import json, xmltodict
from collections import Counter, defaultdict
import re
from summa import summarizer, keywords
# import scispacy
import spacy
from tika import parser
from tqdm import tqdm
import multiprocessing as mp
from joblib import Parallel, delayed
import time
from scispacy.abbreviation import AbbreviationDetector
from scispacy.linking import EntityLinker


nlp = spacy.load("en_core_sci_scibert")
nlp.add_pipe("abbreviation_detector")
# nlp = spacy.load('en_core_sci_scibert', disable=['parser', 'ner'])
# nlp.add_pipe('sentencizer')

def clean_stoping_words(text):
    text = text.replace('\n', ' ')
    text_list = text.split(' ')
    filtered_sentence ='' 

    # pattern = re.compile(r"[A-Za-z0-9\-]{3,50}")
    # re_text = re.findall(pattern, text)
    
    for word in text_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence += word + ' ' 
    return filtered_sentence

# try it with scispacy

with open('all_articles.text', 'r') as wo:
    art = clean_stoping_words(wo.read())

doc = nlp(art[:200000])
last_abrv = ''
for abrv in doc._.abbreviations:
    if str(abrv.text) != last_abrv:
        print(f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}")
        last_abrv = str(abrv.text)

print("yes")

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

def chunker(iterable, total_length, chunksize):
    return (iterable[pos: pos + chunksize] for pos in range(0, total_length, chunksize))

def flatten(list_of_lists):
    "Flatten a list of lists to a combined list"
    return [item for sublist in list_of_lists for item in sublist]

def lemmatize_pipe(doc):
    lemma_list = [str(tok.lemma_).lower() for tok in doc
                  if tok.is_alpha and tok.text.lower()] 
    return lemma_list

def process_chunk(texts, count):
    count +=1
    print('text')
    preproc_pipe = []
    print('before')
    # works for values <5
    for doc in nlp.pipe(texts, batch_size=4):
        print('after')
        # return a text not the 
        preproc_pipe.append(lemmatize_pipe(doc))
        print(count)
    print('end')
    return preproc_pipe
                                    # =10 works
def preprocess_parallel(texts, chunksize=1):
    count = 0
    executor = Parallel(n_jobs=num_cores, backend='multiprocessing', prefer="processes")
    do = delayed(process_chunk)
    tasks = (do(chunk, count) for chunk in chunker(texts, len(texts), chunksize=chunksize))
    result = executor(tasks)
    return flatten(result)

def get_files():
    return [open(os.path.join('graphene', file), 'r').read() for file in os.listdir('graphene')]

if __name__ == '__main__':
    texts = get_files()
    preprocess_parallel(texts)

    print('yes')


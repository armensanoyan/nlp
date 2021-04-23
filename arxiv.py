import numpy as np
import pandas as pd
import gc
import os
import json
from collections import Counter, defaultdict
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
import plotly.express as px
import re
import matplotlib
from summa import summarizer, keywords

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
PATH = os.path.join(os.getcwd(), 'meta.json')
def get_metadata():
    with open(PATH) as f:
        for line in f:
            yield line

metadata = get_metadata()


from neo4j import GraphDatabase

uri = "neo4j://localhost:11005"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))

def create_friend_of(tx, authors, title, id, journal_ref, abstract, categories):
    print('title: ', first_paper['title'])
    created_nodes = tx.run("""
        UNWIND $authors AS i
        MERGE (author:Author {name:i})
        MERGE (article:Article {title:$title, idn:$id, journal_ref:$journal_ref, abstract:$abstract, categories:$categories})
        MERGE (author)-[wrote:WROTE]->(article)
        RETURN author, wrote, article
        """, authors=authors, title=title, id=id, journal_ref=journal_ref, abstract=abstract, categories=categories)
    print('created', created_nodes)

for paper in metadata:
    first_paper = json.loads(paper)
    authors = first_paper['authors'].split(',')
    journal_ref = '' if first_paper['journal-ref'] == None else first_paper['journal-ref']
    with driver.session() as session:
        session.write_transaction(create_friend_of, 
                                    authors, 
                                    first_paper['title'],
                                    first_paper['id'],
                                    journal_ref,
                                    first_paper['abstract'],
                                    first_paper['categories'])


driver.close()
print('yes')
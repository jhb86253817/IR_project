# -*- coding: utf-8 -*-

"""
Extract phrases from 7000 abstracts and store them in json
"""

import MySQLdb as mdb
import extractor
import json

def read_data():
    texts = []
    con = mdb.connect('localhost', 'root', 'jhb196635', 'Articles')
    with con:
        cur = con.cursor()
        cur.execute("select Abstract from Abstracts where ID<= 7000")
        for i in range(int(cur.rowcount)):
            texts.append(str(cur.fetchone()).replace('\\n',' '))

    return texts

def extract(texts):
    phrases = []
    e = extractor.PhraseExtractor()
    count = 0
    for text in texts:
        count += 1
        if count % 100 == 0: print count
        phrase = e.extract(text)
        phrase = [' '.join(p) for p in phrase if len(p)>1]
        phrase = list(set(phrase))
        phrases.append(phrase)

    phrases_string = json.dumps(phrases)
    with open('phrases-json', 'wb') as f:
        f.write(phrases_string)

def load_data():
    with open('phrases-json', 'rb') as f:
        phrases_string = f.read()
    phrases = json.loads(phrases_string)
    for p in phrases:
        print p

if __name__ == '__main__':
    texts = read_data()
    #print texts[0]
    extract(texts)
    #load_data()


 

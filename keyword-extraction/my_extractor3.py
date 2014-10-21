# -*- coding: utf-8 -*-

"""
This class extracts keywords from given documents based on TFIDF.
The extractor is tested on the preprocessedabstracts in database keyword_app.
"""

from __future__ import division
import MySQLdb as mdb
import nltk
from collections import defaultdict
from math import log
from operator import itemgetter
from sklearn.feature_extraction.text import TfidfVectorizer


class keywordExtractor():
    def __init__(self):
        self.abstracts = []
        self.words = []
        self.keywords = []
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.idf = defaultdict(float)
        self.tfidf = []

    def read_data(self):
        """read data from database keyword_app and store it in self.abstracts."""
        con = mdb.connect('localhost', 'root', 'jhb196635', 'keyword_app')
        with con:
            cur = con.cursor()
            cur.execute("select Abstract from PreprocessedAbstracts")
            for i in range(int(cur.rowcount)):
                self.abstracts.append(str(cur.fetchone())[2:-3])

    def preprocess(self):
        """preprocess the text in self.abstracts, which means split them and get rid of meaningless words."""
        for a in self.abstracts:
            token_words = a.split(',')
            self.words.append(token_words)


    def compute_idf(self):
        """calculate the inverse document frequency for all the words."""
        words_all = []
        for l in self.words:
            words_all += l
        words_uniq = set(words_all)
        for w in words_uniq:
            for l in self.words:
                if w in l: self.idf[w] += 1.0
        for w in self.idf:
            self.idf[w] = log(len(self.words) / self.idf[w], 2) 

    def compute_tfidf(self):
        """calculate the term frequency for the words in every document."""
        for l in self.words:
            fdist = dict(nltk.FreqDist(l))
            for k in fdist:
                fdist[k] = fdist[k] * 1.0 / len(l) * self.idf[k]
            self.tfidf.append(fdist)
        
    def keyword_extract(self, n):
        """extract top n keywords based on their TFIDF value and store them in self.keywords."""
        for l in self.tfidf:
            keywords = sorted(l.items(), key=itemgetter(1), reverse=True)[:n]
            keywords = [k for k,v in keywords]
            self.keywords.append(keywords)
        for l in self.keywords:
            print l
            print '\n'

            

if __name__ == '__main__':
    e = keywordExtractor()
    e.read_data()
    e.preprocess()
    e.compute_idf()
    e.compute_tfidf()
    e.keyword_extract(10)

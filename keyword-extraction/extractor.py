# -*- coding: utf-8 -*-
"""
This class deals with way of getting information from different sources
Currently, it includes getting information from
1. name of all researchers paper
2. 70k abstracts of paper from arxiv
"""


from __future__ import division
#from lxml import etree
from os import path
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize
from string import printable

import functools
import operator
import nltk
import string
import pickle

import MySQLdb as mdb

def isPunct(word):
    return len(word) == 1 and word in string.punctuation

def isNumeric(word):
    try:
        float(word) if '.' in word else int(word)
        return True
    except ValueError:
        return False

def listify(f):
    @functools.wraps(f)
    def listify_helper(*args, **kwargs):
        return list(f(*args, **kwargs))
    return listify_helper

class PhraseExtractor():
    def __init__(self):
        self.lemmatizer = nltk.WordNetLemmatizer()
        self.stemmer = nltk.stem.porter.PorterStemmer()

    def leaves(self, tree):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter = lambda t: t.node=='NP'):
            yield subtree.leaves()
    
    def normalise(self,word):
        """Normalises words to lowercase and stems and lemmatizes it."""
        word = word.lower()
        #word = self.stemmer.stem_word(word)
        #word = self.lemmatizer.lemmatize(word)
        return word
    
    def acceptable_word(self,word):
        """Checks conditions for acceptable word: length, stopword."""
        accepted = bool(2 <= len(word) <= 40
            and word.lower() not in self.stopwords)
        return accepted
    
    def get_terms(self,tree):
        for leaf in self.leaves(tree):
            term = [ self.normalise(w) for w,t in leaf if self.acceptable_word(w) ]
            yield term
    
    def extract(self, text):
    
        # Used when tokenizing words
        sentence_re = r'''(?x)      # set flag to allow verbose regexps
              ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
            | \w+(-\w+)*            # words with optional internal hyphens
            | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
            | \.\.\.                # ellipsis
            | [][.,;"'?():-_`]      # these are separate tokensconverseur
        '''
    
        #Taken from Su Nam Kim Paper...
        grammar = r"""
            NBAR:
                {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
    
            NP:
                {<NBAR>}
                {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
        """
        chunker = nltk.RegexpParser(grammar)
    
        toks = nltk.regexp_tokenize(text, sentence_re)
        postoks = nltk.tag.pos_tag(toks)
        tree = chunker.parse(postoks)
    
        from nltk.corpus import stopwords
        self.stopwords = stopwords.words('english')
    
        terms = self.get_terms(tree)
        return terms


if __name__ == "__main__":
    #import os
    #import glob
    #files =  glob.glob(os.getcwd()+"/*.txt")
    #for file in files:
    #    with open(file, 'r') as f:
    #        text = f.read()
    #    text = filter(lambda x: x in printable, text)
    #    e = PhraseExtractor()
    #    terms = e.extract(text)
    #    print [' '.join(t) for t in terms]
    #text = "reinforcement learning you you you cat cat cat dog"
    #e = PhraseExtractor()
    #terms = e.extract(text)
    #print [' '.join(t) for t in terms]
    titles = []
    con = mdb.connect('localhost', 'root', 'jhb196635', 'keyword_app')
    with con:
        cur = con.cursor()
        #get titles
        cur.execute("select Title from Abstracts")
        for i in range(int(cur.rowcount)):
            titles.append(str(cur.fetchone()))
    for text in titles:
        text = filter(lambda x: x in printable, text)
        e = PhraseExtractor()
        terms = e.extract(text)
        print [' '.join(t) for t in terms]


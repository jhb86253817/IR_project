# -*- coding: utf-8 -*-
"""
This class deals with way of getting information from different sources
Currently, it includes getting information from
1. name of all researchers paper
2. 70k abstracts of paper from arxiv
"""

from __future__ import division
from nltk.corpus import stopwords
from nltk import word_tokenize

import operator
import nltk
import string
import pickle

import MySQLdb as mdb
from gensim import corpora, models, similarities

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

def get_phrases():
    """use PhraseExtractor to get phrase from abstracts."""
    abstracts = []
    terms = []
    con = mdb.connect('localhost', 'root', 'jhb196635', 'Articles')
    with con:
        cur = con.cursor()
        #get abstracts
        cur.execute("select Title from Abstracts where ID<30")
        for i in range(int(cur.rowcount)):
            abstracts.append(str(cur.fetchone()))
    e = PhraseExtractor()
    for text in abstracts:
        term = e.extract(text)
        terms.append([' '.join(t) for t in term if len(t)>1][1:-1])

    #remove term with one word
    #terms = [[term for term in t if len(term)>1] for t in terms]
    return terms



if __name__ == "__main__":
    terms = get_phrases()
    #dictionary = corpora.Dictionary(terms)
    #corpus = [dictionary.doc2bow(term) for term in terms]
    #tfidf = models.TfidfModel(corpus)
    #corpus_tfidf = tfidf[corpus]
    #sorted_corpus_tfidf = [sorted(c, key=lambda item: item[1], reverse=True) for c in corpus_tfidf]
    #sorted_keywords = [[dictionary[k] for k,v in c] for c in sorted_corpus_tfidf]
    #for i in range(20):
    #    print sorted_keywords[i][:5]
    for i in range(len(terms)):
        print i+1, terms[i] 
    


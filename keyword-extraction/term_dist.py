#_*_ coding: utf-8 _*_

"""
visualize the term distribution of given corpus.
"""

import nltk
from nltk import *
import MySQLdb as mdb
import matplotlib.pyplot as plt 
import numpy as np
from operator import itemgetter
import extractor

class DistPlot():
    def __init__(self, num):
        self.num = num
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.texts = []
        self.words = []
        self.phrases = []
        self.bigrams = []
        self.trigrams = []
        self.words_all = []

    def read_data(self):
        con = mdb.connect('localhost', 'root', 'jhb196635', 'Articles')
        with con:
            cur = con.cursor()
            cur.execute("select Abstract from Abstracts where ID<= %s", self.num)
            for i in range(int(cur.rowcount)):
                self.texts.append(str(cur.fetchone()))
    
    def preprocess(self):
        """preprocess the text in self.abstracts, which means split them and get rid of meaningless words."""
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        for a in self.texts:
            token_words = tokenizer.tokenize(a)
            token_words = [w.lower() for w in token_words if len(w)>1 and w.isalpha()]
            token_words = [w for w in token_words if w not in self.stopwords]
            self.words.append(token_words)
        for t in self.words:
            self.words_all += t

    def preprocess2(self):
        e = extractor.PhraseExtractor()
        for text in self.texts:
            phrase = e.extract(text)
            self.phrases.append([' '.join(p) for p in phrase if len(p)>1][1:-1])

    def df_word(self):
        """calculate the document frequency for all the words."""
        words_set = []
        for t in self.words:
            words_set += set(t)

        fdist = FreqDist(words_set)

        #fdist = list(FreqDist(words_set).items())
        #fdist_sorted = sorted(fdist, key=itemgetter(1), reverse=False)
        #fdist_sorted = [(k,v) for (k,v) in fdist_sorted if v>1]
        

        #y_values = [v for (k,v) in fdist_sorted[:15]]
        #text_values = [k for (k,v) in fdist_sorted[:15]]
        #x_values = np.arange(1, len(text_values)+1, 1)
        #plt.bar(x_values, y_values)
        #plt.xticks(x_values, text_values)
        #plt.show()

    def dist_word(self):
        fdist = FreqDist(self.words_all)
        fdist.plot(30)

    def dist_phrase(self):
        phrases_set = []
        for t in self.phrases:
            phrases_set += set(t)

        #fdist.plot(50)
        fdist = list(FreqDist(phrases_set).items())
        fdist_sorted = sorted(fdist, key=itemgetter(1), reverse=True)
        fdist_sorted = [(k,v/5000.0) for (k,v) in fdist_sorted]
        with open('phrase-document-frequency', 'wb') as f:
            for w in fdist_sorted:
                f.write(str(w)+'\n')


    def dist_bigram(self):
        self.bigrams = nltk.bigrams(self.words_all)
        fdist = FreqDist(self.bigrams)
        fdist.plot(20)

    def dist_trigram(self):
        self.trigrams = nltk.trigrams(self.words_all)
        fdist = FreqDist(self.trigrams)
        fdist.plot(20)

if __name__ == '__main__':
    dist_plot = DistPlot(5000)
    dist_plot.read_data()
    dist_plot.preprocess2()

    #dist_plot.dist_word()
    #dist_plot.dist_bigram()
    #dist_plot.dist_trigram()
    #dist_plot.df_word()
    dist_plot.dist_phrase()

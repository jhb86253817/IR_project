"""
Filter the key phrases that are not related to professional phrases based on standard phrases from MSML.
"""
from __future__ import division
import json
import MySQLdb as mdb
from collections import Counter
from operator import itemgetter

def read_msml():
    with open('msml-json', 'rb') as f:
        msml_string = f.read()
    msml = json.loads(msml_string)
    return msml

def read_phrases():
    with open('phrases-json', 'rb') as f:
        phrases_string = f.read()
    phrases = json.loads(phrases_string)
    return phrases

def filter1(msml, phrases):
    """if all words in a phrase not appear in MSML set, then it will be removed"""
    words = [w for p in msml for w in p.split()]
    words = set(words)
    phrases_filter = []
    for p in phrases:
        p_filter  = [pp for pp in p if contain_word(pp, words)]
        phrases_filter.append(p_filter)
    return phrases_filter

def filter2(msml, phrases):
    """based on the average counts of words in MSML set to score a phrase"""
    words = [w for p in msml for w in p.split()]
    counter = Counter(words)
    words_set = set(words)

    for p in phrases[1]:
        print p, get_score(p, words_set, counter)

def filter3(msml, phrases):
    """use score to rank phrases"""
    words = [w for p in msml for w in p.split()]
    words_set = set(words)
    counter = Counter(words)
    #print counter.most_common(1)[0][1]
    #print '\n'
    #phrases_filter = []
    #for p in phrases:
    #    p_filter  = [pp for pp in p if contain_word(pp, words_set)]
    #    phrases_filter.append(p_filter)
    #for p in phrases_filter[900]:
    #    print p, get_score(p, counter)
    phrases_score = []
    for p in phrases:
        p_score = [(pp, get_score(pp, counter)) for pp in p]
        p_score = sorted(p_score, key=itemgetter(1))
        phrases_score.append(p_score[:3])

    for p in phrases_score[20:40]:
        print p

def contain_word(phrase, words):
    p = phrase.split()
    for pp in p:
        if pp in words: return True
    return False

def get_score(phrase, counter):
    """for a phrase, the score is based on its word with least count but above certain threshold."""
    p = phrase.split()
    score = counter.most_common(1)[0][1]
    for pp in p:
        if counter[pp] >= 2 and counter[pp] < score: 
            score = counter[pp]
    return score 

def get_score2(phrase, counter):
    p = phrase.split()
    score = 0.0
    for pp in p:
            score += counter[pp]
    return score 


if __name__ == '__main__':
    msml = read_msml()
    phrases = read_phrases()
    filter3(msml, phrases)

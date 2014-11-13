import json 

def read_phrases():
    with open('phrases-json', 'rb') as f:
        phrases_string = f.read()
    phrases = json.loads(phrases_string)
    return phrases

def write_phrases(phrases):
    phrases_new = [p.replace(' ','_') for pp in phrases for p in pp]
    with open('phrases-word2vec.txt', 'wb') as f:
        f.write(' '.join(phrases_new))

if __name__ == '__main__':
    phrases = read_phrases()
    write_phrases(phrases)

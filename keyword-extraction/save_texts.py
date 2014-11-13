
import MySQLdb as mdb
import nltk


def read_data():
    texts = []
    con = mdb.connect('localhost', 'root', 'jhb196635', 'Articles')
    with con:
        cur = con.cursor()
        cur.execute("select Abstract from Abstracts where ID<= 7000")
        for i in range(int(cur.rowcount)):
            texts.append(str(cur.fetchone()).replace('\\n',' '))

    return texts

def write_data(texts):
    toks = []
    for text in texts:
        toks += nltk.word_tokenize(text.replace('-', ' '))
    toks = [t.lower() for t in toks if t.isalpha()]
    with open('7000articles.txt', 'wb') as f:
        f.write(' '.join(toks))

if __name__ == '__main__':
    texts = read_data()
    write_data(texts)

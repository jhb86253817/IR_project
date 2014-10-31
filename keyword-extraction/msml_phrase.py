"""
Get MSML key-phrases from mysql and store them to json file.
"""


import MySQLdb as mdb
import json

def read_data():
    phrases = []
    con = mdb.connect('localhost', 'root', 'jhb196635', 'keyword_app')
    with con:
        cur = con.cursor()
        cur.execute("select Keyword from MSMLKeywords")
        for i in range(int(cur.rowcount)):
            phrases.append(cur.fetchone()[0])

    return phrases

if __name__ == '__main__':
    phrases = read_data()
    phrases = [p.lower() for p in phrases]
    phrases_string = json.dumps(phrases)
    with open('msml-json', 'wb') as f:
        f.write(phrases_string)



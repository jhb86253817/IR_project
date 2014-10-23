import xml.etree.ElementTree as ET 
import MySQLdb as mdb

tree = ET.parse('./data/data/data7.xml')
root = tree.getroot()

con = mdb.connect('localhost', 'root', 'jhb196635', 'Articles')
with con:
    cur = con.cursor()
    #cur.execute("CREATE TABLE IF NOT EXISTS Abstracts(ID int primary key auto_increment, Title varchar(255), Abstract varchar(4096))")

    title = None
    abstract = None
    count = 0
    for e in root.iter():
        if e.tag.split('}')[1] == 'title':
            title = e.text
        if e.tag.split('}')[1] == 'abstract':
            abstract = e.text
        if title and abstract:
            cur.execute("INSERT INTO Abstracts (Title, Abstract) VALUES(%s, %s)", (title, abstract))
            #print title 
            #print abstract
            #print s
            title = None
            abstract = None

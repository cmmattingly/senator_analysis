import mysql.connector
import datetime
import time

cnx = mysql.connector.connect(user='toutvisadmin', password='aa5HZeJ2tahR5Gyz',
                              host='eltanin',
                              database='TextOutlierVis')

cursor = cnx.cursor()
add_party = ("INSERT INTO parties"
               "(party_name, party_color) "
               "VALUES (%s, %s)")
parties = [('democratic', 'red'),
           ('republican', 'blue'),
           ('independent', 'green')]
cursor.executemany(add_party, parties)
cnx.commit()
cnx.close()

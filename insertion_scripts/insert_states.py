import mysql.connector
import datetime
import time

cnx = mysql.connector.connect(user='toutvisadmin', password='aa5HZeJ2tahR5Gyz',
                              host='eltanin',
                              database='TextOutlierVis')

cursor = cnx.cursor()
add_state = ("INSERT INTO state"
               "(state_name, state_gdp, state_population) "
               "VALUES (%s, %s, %s)")

states = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

for state in states:
    cursor.execute(add_state, (state, 0, 0))
cnx.commit()
cnx.close()

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('hyperlinks.db')
c = conn.cursor()

# Query the database
c.execute('SELECT * FROM hyperlinks')

# Fetch and print all results
rows = c.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()


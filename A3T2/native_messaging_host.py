import sys
import json
import struct
import sqlite3

# Initialize the SQLite database
conn = sqlite3.connect('hyperlinks.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS hyperlinks (
        site TEXT,
        href TEXT,
        count INTEGER,
        PRIMARY KEY (site, href)
    )
''')
conn.commit()

def insert_or_update_link(site, href, count):
    c.execute('''
        INSERT INTO hyperlinks (site, href, count) VALUES (?, ?, ?)
        ON CONFLICT(site, href) DO UPDATE SET count = count + ?
    ''', (site, href, count, count))
    conn.commit()

def read_message():
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        sys.exit(0)
    message_length = struct.unpack('=I', raw_length)[0]
    message = b""
    while len(message) < message_length:
        chunk = sys.stdin.buffer.read(min(4096, message_length - len(message)))
        if not chunk:
            break
        message += chunk
    return json.loads(message.decode('utf-8'))

def send_message(message):
    encoded_message = json.dumps(message).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('=I', len(encoded_message)))
    sys.stdout.buffer.write(encoded_message)
    sys.stdout.buffer.flush()

while True:
    message = read_message()
    if 'site' in message and 'links' in message:
        for link in message['links']:
            insert_or_update_link(message['site'], link['href'], link['count'])
        send_message({'status': 'success'})
    else:
        send_message({'status': 'failure'})


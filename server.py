import sqlite3
import os

import hug


def create_db_connection():
    db_file_root = os.path.dirname(os.path.realpath(__file__))
    db_file = os.path.join(db_file_root, 'messages.sql')
    try:
        return sqlite3.connect(db_file)
    except Exception as e:
        print(e)


@hug.cli()
def create_db_tables():
    conn = create_db_connection()
    try:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE
            IF NOT EXISTS messages (
                id integer PRIMARY KEY,
                text text NOT NULL,
                nickname text NOT NULL,
                created_at text
            );
        """)
        print('Created messages table!')
        conn.close()
    except Exception as e:
        print(e)


def get_message(conn, id):
    c = conn.cursor()
    c.execute("""
        SELECT * FROM messages WHERE id={id};
    """.format(id=id))
    return c.fetchone()


def create_message(conn, text, nickname):
    c = conn.cursor()
    c.execute("""
        INSERT INTO messages (text, nickname, created_at)
        VALUES (?, ?, datetime('now'));
    """, (text, nickname))
    conn.commit()
    id = c.lastrowid
    return get_message(conn, id)


def get_all_messages(conn):
    c = conn.cursor()
    c.execute("""
        SELECT * FROM messages;
    """)
    return c.fetchall()


def render_message(message):
    return {
        'id': message[0],
        'text': message[1],
        'nickname': message[2],
        'created_at': message[3],
    }


@hug.post('/messages')
def create_message_api(text, nickname):
    conn = create_db_connection()
    message = create_message(conn, text, nickname)
    conn.close()
    return render_message(message)


@hug.get('/messages')
def get_all_messages_api():
    conn = create_db_connection()
    messages = get_all_messages(conn)
    conn.close()
    return [render_message(message) for message in messages]


@hug.get('/messages/{id}')
def get_single_message_api(id: hug.types.number):
    conn = create_db_connection()
    message = get_message(conn, id)
    conn.close()
    return render_message(message)


@hug.get('/', output=hug.output_format.html)
def root():
    with open('index.html', 'r') as page:
        return page.read()

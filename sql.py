import sqlite3
import json

def read_common_words_fr():
    try:
        with sqlite3.connect('common.db') as cnt:
            cursor = cnt.cursor()

            cursor.execute('SELECT ngram FROM common_words_fr LIMIT 1000')
            words = cursor.fetchall()
            cursor.close()
            return words

    except sqlite3.Error as error:
        print('Failed to read 1000 most common words- ', error)
    
def read_book_words(freq, book_name):
    try:
        with sqlite3.connect('common.db') as cnt:
            cursor = cnt.cursor()

            cursor.execute('SELECT word FROM book_words WHERE count > ? and book = ?', (int(freq), book_name))
            results = cursor.fetchall()
            words = [row[0] for row in results]

            return words


    except sqlite3.Error as error:
        print(f'Failed to read {book_name} words from database- ', error)
        return []

def add_book(bookname, dictionary):
    try:
        with sqlite3.connect('common.db') as cnt:
            print('db init')
            
            cursor = cnt.cursor()

            cnt.execute('''CREATE TABLE IF NOT EXISTS book_words 
            (book TEXT,
            word TEXT,
            count INT,
            CONSTRAINT id PRIMARY KEY (book, word))''')
            
            for word, count in dictionary.items():
                cursor.execute('INSERT or ignore INTO book_words (book, word, count) VALUES (?, ?, ?)',
                                (bookname, word, count))
            cursor.close()
            print('success')

    except sqlite3.Error as error:
        print(f'Failed to add {bookname}to database - ', error)
    
def write_book_words_to_known_words(freq, book_name):
    try:
        with sqlite3.connect('common.db') as cnt:
            print('db init')
            
            cnt.execute('''CREATE TABLE IF NOT EXISTS  known_words
            (word TEXT PRIMARY KEY)''')

            cursor = cnt.cursor()
            cursor.execute('SELECT word FROM book_words WHERE count > ? AND book = ?', (int(freq), book_name)) 
            words = cursor.fetchall()


            cursor.executemany('INSERT OR IGNORE INTO known_words (word) VALUES (?)', (words))
            print(f'Successfully added {cursor.rowcount} words to known_words')

    except sqlite3.Error as error:
        print(f'Failed to add words to known words from {book_name} - ', error)

def read_known_words():
    try:
        with sqlite3.connect('common.db') as cnt:
            print('db init')
            
            cnt.execute('''CREATE TABLE IF NOT EXISTS  known_words
            (word TEXT PRIMARY KEY)''')

            cursor = cnt.cursor()
            cursor.execute('SELECT word FROM known_words',) 
            results = cursor.fetchall()
            words = [row[0] for row in results]

            return words


    except sqlite3.Error as error:
        print('Failed to read known words- ', error)
        return []

def read_words_for_anki_deck(freq, book_name):
    try:
        with sqlite3.connect('common.db') as cnt:
            cursor = cnt.cursor()

            cursor.execute('''SELECT word
            FROM book_words
            WHERE book = ?
            AND count > ?
            AND word NOT IN (SELECT ngram FROM common_words_fr LIMIT 1000)
            AND word NOT IN (SELECT word FROM known_words);
            ''', (book_name, int(freq)))
            results = cursor.fetchall()
            words = [row[0] for row in results]

            return words


    except sqlite3.Error as error:
        print(f'Failed to read {book_name} words from database- ', error)
        return []


if __name__ == "__main__":
    print("")

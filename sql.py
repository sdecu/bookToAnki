import sqlite3
import json
from deckMaker import translate_text 

def main():
    try:
        with sqlite3.connect('common.db') as cnt:
            print('db init')
        
            cnt.execute('''CREATE TABLE IF NOT EXISTS common_words_fr
            (WORD TEXT PRIMARY KEY,
            SENTENCE TEXT,
            TRANSWORD TEXT,
            TRANSSENTENCE TEXT)''')

            cursor = cnt.cursor()
            

            """
            for word, sent in dict.items():
                cursor.execute('INSERT INTO common_words_fr (WORD, SENTENCE, TRANSWORD, TRANSSENTENCE) VALUES (?, ?, ?, ?)',
                                (word, sent, translate_text('en', word), translate_text('en', sent)))
            """
            cnt.commit()
            print('success')

    except sqlite3.Error as error:
        print('Error occured - ', error)


        #rewrite query function 
def read_book_words(freq, book_name):
    try:
        with sqlite3.connect('common.db') as cnt:
            cursor = cnt.cursor()

            cursor.execute('SELECT word FROM book_words WHERE count > ? and book = ?', (freq, book_name))
            results = cursor.fetchall()
            words = [row[0] for row in results]

            return words


    except sqlite3.Error as error:
        print('Error occured - ', error)
        return []

def read_common_words_fr():
    try:
        with sqlite3.connect('common.db') as cnt:
            cursor = cnt.cursor()

            cursor.execute('SELECT ngram FROM common_words_fr LIMIT 1000')
            words = cursor.fetchall()
            cursor.close()
            return words

    except sqlite3.Error as error:
        print('Error occured - ', error)
    

def add_book(bookname, dictionary):
    try:
        with sqlite3.connect('common.db') as cnt:
            print('db init')
            

            cnt.execute('''INSERT INTO book_words
            (book text
            word TEXT PRIMARY KEY,
            count INT)''', (bookname))
            cursor = cnt.cursor()
            

            for word, count in dictionary.items():
                cursor.execute('INSERT INTO book_words (book, word, count) VALUES (?, ?, ?)',
                                (bookname, word, count))
            cursor.close()
            print('success')

    except sqlite3.Error as error:
        print('Error occured - ', error)
    
def add_book_words_to_known_words(freq, book_name):
    try:
        with sqlite3.connect('common.db') as cnt:
            print('db init')
            
            cnt.execute('''CREATE TABLE IF NOT EXISTS  known_words
            (WORD TEXT PRIMARY KEY)''')

            cursor = cnt.cursor()
            cursor.execute('SELECT word FROM book_words WHERE count > ? AND book = ?', (freq, book_name)) 
            words = cursor.fetchall()


            cursor.executemany('INSERT OR IGNORE INTO known_words (word) VALUES (?)', (words))
            print(f'Successfully added {cursor.rowcount} words to known_words')

    except sqlite3.Error as error:
        print('Error occured - ', error)
    
if __name__ == "__main__":
    main()

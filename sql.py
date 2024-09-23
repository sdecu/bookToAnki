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
            
            cursor.execute('ATTACH DATABASE test.db AS new_db;')
            cursor.execute('INSERT INTO new_db.common_words_fr SELECT * FROM common.db.common_words_fr;')

            """
            for word, sent in dict.items():
                cursor.execute('INSERT INTO common_words_fr (WORD, SENTENCE, TRANSWORD, TRANSSENTENCE) VALUES (?, ?, ?, ?)',
                                (word, sent, translate_text('en', word), translate_text('en', sent)))
            """
            cnt.commit()
            print('success')

    except sqlite3.Error as error:
        print('Error occured - ', error)

def query(db, cols, vals):
    try:
        with sqlite3.connect(db) as cnt:
            cursor = cnt.cursor()

            cursor.execute(f'INSERT INTO {db}({cols}) VALUES ({vals})')
            


    except sqlite3.Error as error:
        print('Error occured - ', error)

def read_common_words_fr():
    try:
        with sqlite3.connect('common.db') as cnt:
            cursor = cnt.cursor()

            cursor.execute('SELECT ngram FROM common_words_fr LIMIT 1000')
            words = cursor.fetchall()
            return words

    except sqlite3.Error as error:
        print('Error occured - ', error)
    
    finally:
        if cursor:
            cursor.close()
            



def create_book_db(bookname, dictionary):
    try:
        with sqlite3.connect('common.db') as cnt:
            print('db init')
            
            cnt.execute('DROP TABLE IF EXISTS ?', (bookname))

            cnt.execute('''CREATE TABLE IF NOT EXISTS  ?
            (WORD TEXT PRIMARY KEY,
            SENTENCE TEXT,
            TRANSWORD TEXT,
            TRANSSENTENCE TEXT)''', (bookname))

            cursor = cnt.cursor()
            

            for word, sent in dictionary.items():
                cursor.execute('INSERT INTO common_words_fr (WORD, SENTENCE, TRANSWORD, TRANSSENTENCE) VALUES (?, ?, ?, ?)',
                                (word, sent, translate_text('en', word), translate_text('en', sent)))
            print('success')

    except sqlite3.Error as error:
        print('Error occured - ', error)
    
    
if __name__ == "__main__":
    main()

import spacy
import fr_dep_news_trf
from sql import *
import string
import typer
from typing_extensions import Annotated
import os

def cli(count: Annotated[int, typer.Argument(help="if word appears more often than <number> it will be added to anki deck")],
        file: Annotated[str, typer.Argument(help="absolute or relative path to book")],
        language: Annotated[str, typer.Argument(help="language that the book is in, target must be an ISO 639-1 language code ")]):
    
    book_name = sanitize_bookname(file)
    book = get_text(file)
    nlp = fr_dep_news_trf.load()
    doc = nlp(book)

    
    processed = ""
    for token in doc:
        processed = processed + token.lemma_ + " "
    wc = word_count(processed)
    wc = remove_punctuation(wc)
    add_book(book_name, wc)
    
    anki_words = read_words_for_anki_deck(count, book_name, language)
    click.echo(anki_words)

    #sentences = extract_sentences(anki_words, doc, nlp)
    #click.echo(sentences)
    
    write_book_words_to_known_words(count, book_name, language)

def get_text(text):
    with open(text) as f:
        return f.read()

def word_count(book):
    words = book.lower().split()

    count_dict = {}

    for word in words:
        if word in count_dict:
            count_dict[word] += 1
        else:
            count_dict[word] = 1
    return count_dict

def sort_dict(words):
    return {key: value for key, value in sorted(words.items(), key=lambda item: item[1], reverse=True)}


def remove_uncommon_words(words):
    return {key: value for key, value in words.items() if value >= 3}

def remove_punctuation(words):
    return {key: value for key, value in words.items() if key not in string.punctuation}

def remove_known_words(known, common):
    temp = common.copy()
    for i in range(1, 1001):
        temp.pop(known[str(i)], None)
    return temp

def store_common_words(dictionary):
    f = open("./tmp.py", "w")
    f.write("common_words = " + str(dictionary))
    f.close()

def extract_sentences(dictionary, doc, nlp):
    i = len(dictionary)
    result = {}
    for word in dictionary:
        for sent in doc.sents:
            if word in [token.lemma_.lower() for token in nlp(sent.text)]:
                result[word] = sent.text.strip()
                break
        if word not in result:
            result[word] = f"No sentence found for '[word]'"
        i = i -1
        click.echo(i)
    return result

def sanitize_bookname(filepath):
    pos1 = [pos for pos, char in enumerate(filepath) if char == '/']
    pos2 = [pos for pos, char in enumerate(filepath) if char == '.']
    return f'book_{filepath[pos1[-1]+1:pos2[-1]]}'
    
if __name__ == '__main__':
    typer.run(cli)

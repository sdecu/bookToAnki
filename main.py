import spacy
import fr_dep_news_trf
from sql import *
import string

def main():
    book = get_text("./books/test.txt")
    nlp = fr_dep_news_trf.load()
    doc = nlp(book)

    known_words = read_known_words()

    processed = ""
    for token in doc:
        processed = processed + token.lemma_ + " "
    wc = word_count(processed)
    wc = remove_punctuation(wc)
    add_book("test", wc)
    
    print(read_words_for_anki_deck(5, "test"))
    #print(wc)

    

    sentences = extract_sentences(read_words_for_anki_deck(5, "test"), doc, nlp)
    print(sentences)
    """
    with open("./fr.json", "w", encoding="utf-8") as f:
        json.dump(sentences, f, ensure_ascii=False, indent=2)
    """
    #for token in doc:
    #    print(token.text)


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
        print(i)
    return result

    

main()

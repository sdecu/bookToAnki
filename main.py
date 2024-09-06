import spacy
import fr_dep_news_trf
import make
import deckMaker
from tmp import *
import json

def main():
    text = "/home/sdecu/repo/bookToAnki/books/stranger.txt"
    book = get_text(text)
    nlp = fr_dep_news_trf.load()
    doc = nlp(book)

    words_known = None

    with open("./dict5k.json") as f:
        words_known = json.load(f)
    

    processed = ""
    for token in doc:
        processed = processed + token.lemma_ + " "
    wc = word_count(processed)
    store_common_words(wc)
    wc = remove_uncommon_words(common_words)
    wc = sort_dict(wc)
    #print(wc)

    
    wc = remove_known_words(words_known, wc)

    sentences = extract_sentences(wc, doc, nlp)

    with open("./sentences.json", "w", encoding="utf-8") as f:
        json.dump(sentences, f, ensure_ascii=False, indent=2)

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
    return {key: value for key, value in words.items() if value >= 4}

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
    i = len(dictionary.keys())
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

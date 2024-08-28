import spacy
import fr_dep_news_trf

def main():
    text = "/home/sdecu/repo/anki/books/compteDeMonteCristo.txt"
    book = get_text(text)
    nlp = fr_dep_news_trf.load()
    doc = nlp(book)
    words_known = get_text("./dict5k.json")


    
    processed = ""
    for token in doc:
        processed = processed + token.lemma_ + " "
    wc = word_count(processed)
    wc = remove_uncommon_words(wc)
    wc = sort_dict(wc)
    for k, v in wc.items():
        print(k, v)
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
    dic = {key: value for key, value in words.items() if value >= 5}
    return dic

def remove_known_words(known, common):
    temp = None
    for i in range(1, 1000):
        temp = [item for item in common if item is not known[str(i)]]
    return temp
main()

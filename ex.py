def main():
    text = "/home/sdecu/repo/anki/books/compteDeMonteCristo.txt"
    book = get_text(text)
    get_word_count(book) 
    get_char_count(book) 
    report(book, text)
    print(report(book, text))

def get_text(text):
    with open(text) as f:
        return f.read()


def get_word_count(string):
    string = string.split()
    i = 0
    for s in string:
        i +=1
    return i


def get_char_count(book):
    arr = list(book)
    alphabet = 'abcdefghijklmnopqrstuvwxyzàâæçéèêëîïôœùûüÿ'
    dict = {}
    for c in alphabet:
        i = 0
        for letter in arr:
            if c == letter.lower():
                i += 1
        dict[c] = i
    return dict

def report(book, text):
    p = f"--- Begin report of {text} ---\n"
    p = p + f"{get_word_count(book)} words found in the document\n\n"
    dict = get_char_count(book)
    sort = reversed(sorted(dict.items(), key = lambda item: item[1]))
    for key, value in sort:
        p = p + f"The '{key}' character was found {value} times\n"
    p = p + "--- End report ---"
    total = 0
    for letter in dict:
        total += int(dict[letter])
    p = p + str(total)
    return p
main()

from tmp import *

def main():
    lst = []
    
    for k in common_words.keys():
        lst.append(str(k))
    
    total = 0
    for item in lst:
        total = total + len(item) 
    print(total)

main()

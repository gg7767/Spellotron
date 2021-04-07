"""
Author : Gnandeep Gottipati
language: python3
Function : Spellchecker and spell corrector
"""
#importing the required modules

import sys
import time

#Assigning global variables
LEGAL_WORD_FILE = "american-english.txt"
KEY_ADJACENCY_FILE = "keyboard-letters.txt"

def validate(st, lst):
    """
    checks if the string is in the given list
    """
    #file = open(LEGAL_WORD_FILE)
    if st in lst:
        return True
    else:
        return False

def adj_dic():
    """
    creates a dictionary with the key as a letter and list of adjacent words of the values
    """
    file = open(KEY_ADJACENCY_FILE)
    dic = dict()
    for line in file:
        line = line.strip().split()
        dic[line[0]] = line[:]
    return dic

def make_list(length):
    """
    makes a list of given length
    """

    file = open(LEGAL_WORD_FILE)
    lst = []
    if length== "e":
        for line in file:
            line = line.strip()
            lst.append(line)
    else:
        for line in file:
            line = line.strip()
            if len(line) == length:
                lst.append(line)
    return lst


def punctuation_stripper(st):
    """
    gets rids of all the punctuations before and after the string and returns and tuple.
    """
    start_st = ""
    end_st = ""
    lst = []
    sub_lst = []
    lst += st
    if len(lst) == 1:
        return start_st, ''.join(lst), end_st
    for i in range(len(lst)):
        if not ord("A") <= ord(lst[i]) <= ord("Z") and not ord("a") <= ord(lst[i]) <= ord("z"):
            if i == len(lst) - 1:
                return start_st + lst[i], '', ''
            start_st += lst[i]
            sub_lst.append(lst[i])
        else:
            break
    for i in range(len(lst) - 1, 0, -1):
        if not ord("A") <= ord(lst[i]) <= ord("Z") and not ord("a") <= ord(lst[i]) <= ord("z"):
            end_st += lst[i]
            sub_lst.append(lst[i])
        else:
            break
    for ch in sub_lst:
        lst.remove(ch)
    return start_st, ''.join(lst), end_st[::-1]

def punctuation_joiner(st_st, st, en_st):
    """
    combines all the strings which are given as inputs
    """
    return st_st + st + en_st

def remove(st):
    """
    removes and checks all the possible words with the letter removed from the string
    """
    lst = []
    lst += st
    if len(lst) == 0:
        return ''
    length = len(lst) - 1
    lst_words = make_list(length)
    for i in range(len(lst)):
        popped = lst.pop(i)
        word = ''.join(lst)
        if word in lst_words:
            return word
        lst.insert(i, popped)
    return False

def insert(st, dic):
    """
    inserts the alphabets and checks if the inserted string exist in the dictionary or not
    """
    if len(st) == 0:
        return ''
    length = len(st) + 1
    lst_words = make_list(length)
    for i in range(len(st)+1):
        for alpha in range(ord("a"), ord("z") + 1):
            word = st[:i] + chr(alpha) + st[i:]
            if word in lst_words:
                return word
    return False

def adj_letter(st, dic):
    """
    checks the typo for adjacent letters or not and returns the correct word
    """

    if len(st) == 0:
        return ''
    length = len(st)
    lst_words = make_list(length)
    for i in range(len(st)):
        if st[i].isupper():
            st = st[i].lower() + st[1:]
        if ord(st[i]) < 97 or ord(st[i]) > 122:
            continue
        for key in dic[st[i]]:
            word = st[:i] + key + st[i+1:]
            if word in lst_words:
                return word
    return False

def correctors(st, dic):
    """
    calls all the corrected functions in the decreasing order of priority
    and returns a tuple as a string and a number
    """
    if not adj_letter(st, dic) is False:
        a = st
        result = adj_letter(st, dic)
        if a[0].isupper():
            return result[0].upper() + result[1:], 1
        return result, 1
    elif not insert(st, dic) is False:
        result = insert(st, dic)
        return result, 2
    elif not remove(st) is False:
        result = remove(st)
        return result, 3
    else:
        return st, 4



def main():
    """
    Calls all the terminal functions and makes use of all the functions to correct the words. It alsochecks the punctuation cases
    """
    mode = sys.argv[1]
    dic = adj_dic()
    lst = make_list("e")
    count_1 = 0
    corrected_words = []
    unknown_words = []

    if mode != "words" and mode != "lines":
        print("Error!", file = sys.stderr)
        return ""

    if len(sys.argv) == 3:
        filename = sys.argv[2]
        file_1 = open(filename)
        if mode == "lines":
            for line in file_1:
                print()
                st = line.strip().split()
                for ch in st:
                    actual_word = ch
                    count_1 += 1
                    start_st, stripped_st, end_st = punctuation_stripper(ch)
                    if stripped_st == "":
                        continue
                    if validate(stripped_st, lst) == True:
                        print(start_st + stripped_st + end_st, end= " ")
                        continue
                    if stripped_st[0].isupper():
                        temp = stripped_st[0].lower() + stripped_st[1:]
                        if validate(temp, lst) == True:
                            temp = temp[0].upper() + temp[1:]
                            print(start_st + temp + end_st, end = " ")
                            continue
                    a, b = correctors(stripped_st, dic)
                    if b != 4:
                        print(punctuation_joiner(start_st, a, end_st), end= " ")
                        corrected_words.append(actual_word)
                    if b == 4:
                        if a[0].islower():
                            print(punctuation_joiner(start_st, a, end_st), end= " ")
                            unknown_words.append(a)
                            continue
                        high = stripped_st[0]
                        lower_st = stripped_st[0].lower() + stripped_st[1:]
                        a, b = correctors(lower_st, dic)
                        if b == 1:
                            print(punctuation_joiner(start_st, a, end_st), end= " ")
                            corrected_words.append(actual_word)
                        elif b==2 or b==3:
                            print(punctuation_joiner(start_st, high + a, end_st), end= " ")
                            corrected_words.append(actual_word)
                        else:
                            print(punctuation_joiner(start_st, a, end_st), end= " ")
                            if not a[0].isidentifier():
                                continue
                            unknown_words.append(stripped_st)
        elif mode == "words":
            for line in file_1:
                st = line.strip().split()
                for ch in st:
                    actual_word = ch
                    count_1 += 1
                    start_st, stripped_st, end_st = punctuation_stripper(ch)
                    if stripped_st == "":
                        continue
                    if validate(stripped_st, make_list(len(stripped_st))) == True:
                        #print(start_st + stripped_st + end_st, end= " ")
                        continue
                    if stripped_st[0].isupper():
                        temp = stripped_st[0].lower() + stripped_st[1:]
                        if validate(temp, make_list(len(stripped_st))) == True:
                            #print(start_st + temp + end_st)
                            continue
                    a, b = correctors(stripped_st, dic)
                    if b != 4:
                        print(actual_word, "->", punctuation_joiner(start_st, a, end_st))
                        corrected_words.append(actual_word)
                    if b == 4:
                        if a[0].islower():
                            unknown_words.append(a)
                            continue
                        high = stripped_st[0]
                        lower_st = stripped_st[0].lower() + stripped_st[1:]
                        a, b = correctors(lower_st, dic)
                        if b == 1:
                            print(actual_word, "->",punctuation_joiner(start_st, a, end_st))
                            corrected_words.append(actual_word)
                        elif b==2 or b==3:
                            print(actual_word, "->",punctuation_joiner(start_st, high + a, end_st))
                            corrected_words.append(actual_word)
                        else:
                            if not a[0].isidentifier():
                                continue
                            #print(punctuation_joiner(start_st, a, end_st), end= " ")
                            unknown_words.append(stripped_st)


    elif len(sys.argv) == 2:
        st = input("Enter your text: ")
        if mode == "lines":
            st = st.split(" ")
            count = len(st) - 1
            for ch in st:
                    actual_word = ch
                    count_1 += 1
                    start_st, stripped_st, end_st = punctuation_stripper(ch)
                    if stripped_st == "":
                        continue
                    if validate(stripped_st, lst) == True:
                        print(start_st + stripped_st + end_st, end= " ")
                        continue
                    if stripped_st[0].isupper():
                        temp = stripped_st[0].lower() + stripped_st[1:]
                        if validate(temp, lst) == True:
                            temp = temp[0].upper() + temp[1:]
                            print(start_st + temp + end_st, end = " ")
                            continue
                    a, b = correctors(stripped_st, dic)
                    if b != 4:
                        print(punctuation_joiner(start_st, a, end_st), end= " ")
                        corrected_words.append(actual_word)
                    if b == 4:
                        if a[0].islower():
                            print(punctuation_joiner(start_st, a, end_st), end= " ")
                            unknown_words.append(a)
                            continue
                        high = stripped_st[0]
                        lower_st = stripped_st[0].lower() + stripped_st[1:]
                        a, b = correctors(lower_st, dic)
                        if b == 1:
                            print(punctuation_joiner(start_st, a, end_st), end= " ")
                            corrected_words.append(actual_word)
                        elif b==2 or b==3:
                            print(punctuation_joiner(start_st, high + a, end_st), end= " ")
                            corrected_words.append(actual_word)
                        else:
                            print(punctuation_joiner(start_st, a, end_st), end= " ")
                            if not a[0].isidentifier():
                                continue
                            unknown_words.append(stripped_st)


        if mode == "words":

            st = st.split(" ")
            count = len(st) - 1
            for ch in st:
                    actual_word = ch
                    count_1 += 1
                    start_st, stripped_st, end_st = punctuation_stripper(ch)
                    if stripped_st == "":
                        continue
                    if validate(stripped_st, make_list(len(stripped_st))) == True:
                        #print(start_st + stripped_st + end_st, end= " ")
                        continue
                    if stripped_st[0].isupper():
                        temp = stripped_st[0].lower() + stripped_st[1:]
                        if validate(temp, make_list(len(stripped_st))) == True:
                            #print(start_st + temp + end_st)
                            continue
                    a, b = correctors(stripped_st, dic)
                    if b != 4:
                        print(actual_word, "->", punctuation_joiner(start_st, a, end_st))
                        corrected_words.append(actual_word)
                    if b == 4:
                        if a[0].islower():
                            unknown_words.append(a)
                            continue
                        high = stripped_st[0]
                        lower_st = stripped_st[0].lower() + stripped_st[1:]
                        a, b = correctors(lower_st, dic)
                        if b == 1:
                            print(actual_word, "->",punctuation_joiner(start_st, a, end_st))
                            corrected_words.append(actual_word)
                        elif b==2 or b==3:
                            print(actual_word, "->",punctuation_joiner(start_st, high + a, end_st))
                            corrected_words.append(actual_word)
                        else:
                            if not a[0].isidentifier:
                                continue
                            #print(punctuation_joiner(start_st, a, end_st), end= " ")
                            unknown_words.append(stripped_st)
    print()
    print()
    print(count_1, "words read from file")
    print()
    print()
    print(len(corrected_words), "Corrected Words")
    print(corrected_words)
    print()
    print()
    print(len(unknown_words), "Unknown Words")
    print(unknown_words)


#calling the main function
main()




import subprocess
import csv
import os

# dependencies
# 1 - first word priority
# 2 - second word priority
# 3 - consider as one
# 12 - both words important
# 0 - ignore

dependencies = {
'root' : 0,
'dep' : 1,
'aux' : 0,
'auxpass' : 0,
'abbrev' : 0,
'attr' : 0,
'cop' : 1,
'arg' : 12,
'agent' : 12,
'comp' : 12,
'acomp' : 2,
'ccomp' : 0,
'xcomp' : 12,
'obj' : 12,
'dobj' : 12,
'iobj' : 0,
'pobj' : 0,
'subj' : 12,
'nsubj' : 12,
'nsubjpass' : 12,
'csubj' : 12,
'csubjpass' : 12,
'infmod' : 12,
'cc' : 0,
'conj' : 0,
'expl' : 0,
'mod' : 0,
'amod' : 2,
'appos' : 0,
'advcl' : 12,
'det' : 0,
'predet' : 0,
'preconj' : 0,
'vmod' : 0,
'mwe' : 12,
'mark' : 1,
'advmod' : 2,
'neg' : 12,
'rcmod' : 12,
'quantmod' : 0,
'nn' : 0,
'npadvmod' : 0,
'tmod' : 0,
'num' : 0,
'number' : 0,
'prep' : 0,
'poss' : 0,
'possessive' : 0,
'prt' : 3,
'parataxis' : 12,
'goeswith' : 0,
'punct' : 0,
'ref' : 0,
'sdep' : 1,
'xsubj' : 1,
'rel' : 1,
'purpcl' : 12,
'measure' : 12
}

# parse a sentence from input.txt file to a syntax tree
def tree_parse():
    tree = open("tree.txt", "w+")
    dependencies = open("dep.txt", "w+")
    output = subprocess.check_output(["../sp/3.8.0/libexec/./lexparser.sh", "input.txt"])
    o = output.decode("utf-8").split('\n\n')
    tree.writelines(o[0])
    dependencies.writelines(o[1])
    tree.close()
    dependencies.close()

# check whether the whole sentence is neutral
def neutral_checkup(sent):
    flag = True
    for dep in sent:
        if dependencies[dep[2]] != 0 and dependencies[dep[2]] != 2:
            return False
    return True

# analyse dependencies on positivity and negativity
def analyse_dep():
    # edit the dependencies for analysis -> a list dep_list with 2 words and the dependency between them
    with open("dep.txt") as dep:
        content = dep.readlines()
        dep_list = []
        for line in content:
            o = line.split('(')
            o[1] = o[1].split(')')
            o[1].remove(o[1][1])
            a = o[1][0].split(', ')
            o.remove(o[1])
            a.append(o[0])
            dep_list.append(a)
        #print(dep_list)

        if neutral_checkup(dep_list):
            return 2
        else:
            positivity_index = int(coll_dic(filter(dep_list[0][1])))
            for dep in dep_list:
                positivity_index = dep_est(dep, positivity_index)
            return positivity_index

# estimation functions for the dependency
def dep_est(dep, current_index):
    if dep[2] in dependencies:
        dep_key = dependencies[dep[2]]
    else:
        return current_index

    if dep_key == 0:
        return current_index
    elif dep_key == 1 or dep_key == 12:
        return calculate(int(coll_dic(filter(dep[0]))), current_index)
    elif dep_key == 2:
        return current_index
    else:
        return calculate(int(coll_dic(filter(dep[0]) + '' + filter(dep[1]))), current_index)


def calculate(a,b):
    if a == 1 and b == 1:
        return 1
    else:
        return 0

# removes the difits and prefix
def filter(s):
    result = ''.join([i for i in s if not i.isdigit()])
    result = result.replace('-', '')
    return result

# collocations dictionary reading, takes a word as a token and returns it's positivity index
def coll_dic(token):
    found_flag = False
    with open('dictionary.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['word'] == token.lower():
                found_flag = True
                return row['pindex']

    if found_flag == False:
        index = input('Enter a positivity index for the word ' + '""' + token + '""' + ': ')
        with open(r'dictionary.csv', 'a') as csvfile:
            fieldnames = ['word', 'pindex']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writeheader()
            writer.writerow({'word': token.lower(), 'pindex': index})
            return index
    else:
        print('Something went wrong...')

#check whether the sentence was analyzed already
def sentence_history(token):
    with open('history.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['sentence'] == token.lower():
                return row['result']

    return False

#output function, that outputs a result, understandable for a user
def print_output(res):
    if res == 1:
        return "positive"
    elif res == 0:
        return "negative"
    else:
        return "neural"

# receive a sentence from a user and parses it to a syntax tree
def run_treep(sentence):
    #inp = ''
    #while inp == '':
    #    inp = input("Enter a string: ")

    #check whether the sentence was being checked before
    if sentence_history(sentence) != False:
        print("The sentence exists in the history.")
        return print_output(sentence_history(sentence))

    i = open("input.txt", "w")
    i.write(sentence)
    i.close()
    tree_parse()

    clean_to_menu()
    result = analyse_dep()

    with open(r'history.csv', 'a') as csvfile:
        fieldnames = ['sentence', 'result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'sentence': sentence.lower(), 'result': result})

    return print_output(result)
    #return result
    #print("Done.")
    i.close()

#checks whether a parameter is a digit
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#checks whether the string is empty
def isNotEmpty(s):
    return bool(s and s.strip())

#random function that prints out the csv file
def viewcsv(f):
    if f == 'dictionary.csv':
        key = 'word'
        token = 'pindex'
    else:
        key = 'sentence'
        token = 'result'

    with open(f) as csvfile:
        reader = csv.DictReader(csvfile)
        print(key + ', ' + token)
        print('--------------------')
        for row in reader:
            print(row[key] + ' -- ' + print_output(int(row[token])))

def clean_to_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Hello! This is a beta version of a text context definition algorithm. \n Choose one of the next options:")
    print("1. Analyse a sentence")
    print("2. View the dictionary")
    print("3. View the history of sentences analysis")
    print("4. Exit")
    print("======================================================")

def console_ui():
    flag = True
    while flag:
        clean_to_menu()
        s = 0
        while is_int(s) != True or (int(s) != 1 and int(s) != 2 and int(s) != 3 and int(s) != 4):
            s = input("Your answer (1,2,3,4): ")
            if is_int(s) != True or (int(s) != 1 and int(s) != 2 and int(s) != 3 and int(s) != 4):
                print("You should choose only one out of 3 options!")

        print("======================================================")

        if int(s) == 1:
            sent = ""
            while isNotEmpty(sent) == False:
                sent = input("Input your sentence: ")
                if isNotEmpty(sent) == False:
                    print("The sentence can not be empty!")
            print(run_treep(sent))
            wait = input("Press any key to continue...")
        elif int(s) == 2:
            print("COLLOCATIONS DICTIONARY")
            viewcsv('dictionary.csv')
            wait = input("Press any key to continue...")
        elif int(s) == 3:
            print("HISTORY")
            viewcsv('history.csv')
            wait = input("Press any key to continue...")
        else:
            flag = False

console_ui()
#s = input("Input the string:")
#print(run_treep(s))
#print(run_treep())
#print(coll_dic("happy"))
#d = ['love-2', 'I-1', 'nsubj']
#print(dep_est(d, 1))
#print(filter('risk-10'))

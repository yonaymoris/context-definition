import subprocess
import csv

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

# analyse dependencies on positivity and negativity
def analyse_dep():
    with open("dep.txt") as dep:
        content = dep.readlines()
        for line in content:
            o = line.split('(')
            o[1] = o[1].split(')')
            o[1].remove(o[1][1])
            print(o)

# collocations dictionary reading
def coll_dic(token):
    found_flag = False
    with open('dictionary.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['word'] == token.lower():
                found_flag = True
                return row['pindex']

    if found_flag == False:
        index = raw_input('Enter a positivity index for the word ' + token + ': ')
        with open(r'dictionary.csv', 'a') as csvfile:
            fieldnames = ['word', 'pindex']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writeheader()
            writer.writerow({'word': token.lower(), 'pindex': index})
            return index
    else:
        print('Something went wrong...')

# takes 2 words and their dependency as an argument and defines the main one out of 2
def main_word():
    dependencies = {
    'root' : root
    'dep' : dependent
    'aux' : auxiliary
    'auxpass' : passive auxiliary cop - copula
    'arg' : argument agent - agent
    'comp' : complement
    'acomp' : adjectival complement
    'ccomp' : clausal complement with internal subject xcomp - clausal complement with external subject obj - object
    'dobj' : direct object
    'iobj' : indirect object
    'pobj' : object of preposition
    'subj' : subject
    'nsubj' : nominal subject
    'nsubjpass' : passive nominal subject csubj - clausal subject
    'csubjpass' : passive clausal subject
    'cc' : coordination
    'conj' : conjunct
    'expl' : expletive (expletive “there”) mod - modifier
    'amod' : adjectival modifier appos - appositional modifier
    'advcl' : adverbial clause modifier det - determiner
    'predet' : predeterminer
    'preconj' : preconjunct
    'vmod' : reduced, non-finite verbal modifier mwe - multi-word expression modifier
    'mark' : marker (word introducing an advcl or ccomp advmod - adverbial modifier
    'neg' : negation modifier
    'rcmod' : relative clause modifier
    'quantmod' : quantifier modifier
    'nn' : noun compound modifier
    'npadvmod' : noun phrase adverbial modifier
    'tmod' : temporal modifier num - numeric modifier
    'number' : element of compound number prep - prepositional modifier
    'poss' : possession modifier
    'possessive' : possessive modifier (’s)
    'prt' : phrasal verb particle parataxis - parataxis
    'goeswith' : goes with punct - punctuation
    'ref' : referent
    'sdep' : semantic dependent
    'xsubj' : controlling subject
    }

# receive a sentence from a user and parses it to a syntax tree
def run_treep():
    inp = raw_input("Enter a string: ")
    i = open("input.txt", "w")
    i.write(inp)
    i.close()
    tree_parse()
    print("Done.")
    i.close()

#run_treep()
#analyse_dep()
print(coll_dic("happy"))

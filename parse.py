import subprocess

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

# takes 2 words and their dependency as an argument and defines the main one out of 2
def main_word():
    dependencies = []

# receive a sentence from a user and parses it to a syntax tree
def run_treep():
    inp = input("Enter a string: ")
    i = open("input.txt", "w")
    i.write(inp)
    i.close()
    tree_parse()
    print("Done.")

#run_treep()
analyse_dep()

#!/usr/bin/env python

#########################
#                       #
#      PDB-parser       #
#                       #
#  by Nicolas Pettican  #
#                       #
#########################

import os
import sys
import re

# optional user input file location
#DATADIR = raw_input("\nINPUT FILE LOCATION: ")
#DATAFILE = raw_input("\nINPUT FILE NAME: ")
#DATAOUT = raw_input("\nOUTPUT FILE NAME: ")
DATADIR = "F:\MSc\RP2\DSGONgly"
DATAFILE = "new1001.pdb"
OUTFILE = "new1001pymod.pdb"


def parse(datafile):
    # nothing clever here, the file parser
    data = [line.strip() for line in open(datafile, 'r')]
    return data

def welcome():
    # opening credits
    print ("#" * 25 + "\n#\t\t\t#\n#\tPDB-parser\t#" + "\n#\t\t\t#" +
           "\n#  by Nicolas Pettican  #" + "\n#\t\t\t#\n" + "#" *25 + "\n")

def lineheads(datafile):
    data = [line.strip().split() for line in open(datafile, 'r')]
    print "\nThe file has %s lines\n" %(len(data))
    lineheadset = set()
    for line in data:
        if line[0] != "END":
            lineheadset.add(line[0])
    # it was 3 in the morning when I wrote this...
    # so I can't exactly remember how
    for element in set(lineheadset):
        x = [line[0].count(element) for line in data]
        print "{x} of which are {y} elements\n".format(x=x.count(1), y=element)

def optionsbegin(pdb):
    # options the user has
    choice = int
    while not (choice == 1 or choice == 2 or choice == 3):
        choice = input("What would you like to do to the PDB file?\n" +
                       "Here are the current options:\n" +
                       "1. Replace a number or string    # it will replace every instance of that number or string\n" +
                       "2. Nothing else yet...           # there will be more options in the future\n" +
                       "3. Quit\n")
    return choice

def findelement(pdb,busca):
    # finds where the elements to change are
    return sum(1 for l in pdb if re.search(busca, l))

def findrange(pdb,busca):
    rangebusca = [i for i, line in enumerate(pdb) if re.search(busca, line)]
    return [rangebusca[0], rangebusca[-1] + 2]

def findindex(pdb,busca):
    # finds what column the query string is
    datalist = [line.split() for line in pdb if re.search(busca, line)]
    temp = set()
    tempupdate = [temp.add(index) for i, value in enumerate(datalist) 
                  for index, l in enumerate(datalist[i], 1) if re.search(busca, l)]
    return list(temp)

def replacechar(pdb):
    # to change something within the PDB
    # chosen by the user
    try:
        busca = raw_input("\nInsert characters you want to look for:\t")
        while not (len(busca) > 2):
            busca = raw_input("\n*Note that it must be 3 or more characters*\t")
        instances = findelement(pdb,busca)
        rangebusca = findrange(pdb,busca)
        print "\n%s appears %s times in lines %s to %s" %(busca, instances, rangebusca[0], rangebusca[-1])
    except:
        print "\nWoops, can't seem to find %s\n" %(busca)
    # finds what column the query string is in
    try:
        indexloc = findindex(pdb,busca)
        if len(indexloc) < 2:
            print "\n%s is located in column %s\n" %(busca, indexloc[0])
        elif len(indexloc) > 1:
            notgood = ", ".join(str(x) for x in indexloc)
            print "\n%s is located in columns %s\nyou may want to double check before proceeding" %(busca, notgood)
            if not continuar():
                quit()
    except:
        print "\nWoops, can't seem to find %s's location\n" %(busca)
    # THE REPLACING SECTION, under development
    try:
        cambia = raw_input("Insert number or string you want to replace it with:\t")
        if len(busca) == len(cambia):
            newpdb = replace(pdb,busca,cambia)
            return newpdb
        else:
            print ("\nYou can't replace a string of different size...\n" +
                   "it will break the PDB file!\n")
            quit()
    except:
        print "\nWoops, something went wrong\n"
        quit()

def replace(pdb,busca,cambia):
    # THE REPLACING FUNCTION, under development
    # note that this will break the pdb into individual characters
    # pdbchars has all the lines broken into individual characters
    # for some reason it struggles with busca <= 3

    pdbchars = [[l.strip() for l in line] for line in pdb]
    buscachars = [l.strip() for l in busca]
    cambiachars = [l.strip() for l in cambia]
    rangebusca = findrange(pdb,busca)
    
    begin = 100   # just as a default
    end = 101     # just as a default

    # I really don't like nested code...
    # but it could be worse!
    newpdb = []
    counter = 0
    for line in pdbchars:
        newline = []
        b = 0
        charcount = 0
        if counter not in range(rangebusca[0], rangebusca[-1]):
            for char in line:
                newline.append(char)
        else:
            for char in line:
                check = 0
                if line[charcount] == buscachars[0] and line[charcount + 1] == buscachars[1]:
                    for i, value in enumerate(buscachars):
                        if line[charcount + i] == buscachars[i]:
                            check = i
                    if check > 1:
                        begin = b
                        end = b + len(buscachars)
                        x = 0
                        for chars in pdbchars[counter][begin:end]:
                            newline.append(char.replace(char, cambiachars[x]))
                            x += 1
                elif charcount not in range(begin, end):
                    newline.append(char)
                charcount += 1
                b += 1
        counter += 1
        newpdb.append(newline)

    return newpdb

def reconstruct(newpdb):
    # reconstruct the "replaced" lines with the appropriate spacing
    readypdb = []
    for line in newpdb:
        newline = []
        for char in line:
            if char != '':
                newline.append(char)
            elif char == '':
                newline.append(' ')
        readypdb.append(newline)
    return ["".join(str(x) for x in line) for line in readypdb]

def outputfile(readypdb,outfile):    
    with open(outfile, 'w') as output:
        output.writelines(str(i) + "\n" for i in readypdb)
        #output.write('\n'.join(str(i)) for i in readypdb)

def nothingyet():
    # just some of my nonesense :grin:
    print ("\nNot much else going on here for now,\n" +
           "I want to add a 'replace entire column' option,\n" +
           "but I could use some help to increase functionality,\n" +
           "so be sure to fork it on github :D\n")
    sys.exit("\n\nQuitting the session...\n" + "-"*20 +
             "\nThank you for using PDB-parser!\n")

def continuar():
    # the "are you sure?" function
    return raw_input("\nContinue? [yes|no]\t").lower().startswith('y')

def quit():
    # quite, of course
    sys.exit("\n\nQuitting the session...\n" + "-"*20 +
             "\nThank you for using PDB-parser!\n" + "-"*20 +
             "\nBe sure to check it out on GitHub:\ngithub.com/nickpettican/PDB-parse\n")

def main():
    # the main function
    datafile = os.path.join(DATADIR, DATAFILE)
    outfile = os.path.join(DATADIR, OUTFILE)
    if datafile:
        # pdb is now a list containing all the lines of the input PDB file
        pdb = parse(datafile)
        welcome()
        lineheads(datafile)
        choice = optionsbegin(pdb)
        if choice == 1:
            newpdb = replacechar(pdb)
        elif choice == 2:
            nothingyet()
        elif choice == 3:
            quit()

        try: 
            readypdb = reconstruct(newpdb)
            print "\n*Successfuly reconstructed new PDB structure!*\n"
        except:
            print "\nWoops, something went wrong when reconstructing the PDB!\n"
            quit()

        try:
            outputfile(readypdb,outfile)
            print "*Successfuly created new PDB file!*\n"
        except:
            print "\nWoops, something went wrong when creating the PDB!\n"
            quit()
   
    else:
        print "\nCould not open file\nMake sure you type the correct directory and file name\n"
        quit()

if __name__ == "__main__":
    main()

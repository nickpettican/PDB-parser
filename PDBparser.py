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
from itertools import groupby
from operator import itemgetter

# optional user input file location
#DATADIR = raw_input("\nINPUT FILE LOCATION: ")
#DATAFILE = raw_input("\nINPUT FILE NAME: ")
#OUTFILE = raw_input("\nOUTPUT FILE NAME: ")
DATADIR = "/Users/Priyanka/Documents/Nick/Python"
DATAFILE = "test02.pdb"
OUTFILE = "testmod02.pdb"


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
    while True:
        try:
            choice = int(raw_input("What would you like to do to the PDB file?\n" +
                           "Here are the current options:\n" +
                           "Option 1 - Replace characters    # it will replace every instance of those characters\n" +
                           "Option 2 - ATOM to HETATM        # work in progress\n" +
                           "Option 3 - Quit\n\nOption: "))
        except ValueError:
            continue
        if 1 <= choice <= 3:
            return choice

def findelement(pdb,busca):
    # finds where the elements to change are
    return sum(1 for l in pdb if re.search(busca, l))

def findrange(pdb,busca):
    rangebusca = [i for i, line in enumerate(pdb) if re.search(busca, line)]
    realranges = [map(itemgetter(1), value)
                  for i, value in groupby(enumerate(rangebusca),
                  lambda (i, x): i-x)]
    if len(realranges) == 1:
        return [realranges[0][0], realranges[0][-1] + 1]
    elif len(realranges) >= 2:
        return [[realranges[i][0], realranges[i][-1] + 1]
                for i, line in enumerate(realranges)]
        #return [line[0], line[1] + 1 for line in realranges]
    #return [rangebusca[0], rangebusca[-1] + 1]

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
        print rangebusca
        if len(rangebusca) == 1:
            print "\n%s appears %s times in lines %s to %s" %(busca, instances, rangebusca[0][0], rangebusca[0][-1])
        elif len(rangebusca) >= 2:
            print "\n%s appears %s times in lines %s" %(busca, instances, rangebusca)
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
                quitsesh()
    except:
        print "\nWoops, can't seem to find %s's location\n" %(busca)
    # THE REPLACING SECTION
    try:
        cambia = raw_input("Insert number or string you want to replace it with:\t")
        if len(busca) == len(cambia):
            newpdb = replace(pdb,busca,cambia)
            return newpdb
        else:
            print ("\nReplacing a string of different size may break the PDB.\n")
            if continuar():
                newpdb = replace(pdb,busca,cambia)
                return newpdb
            else:
                quitsesh()
    except:
        print "\nWoops, something went wrong\n"
        quitsesh()

def replace(pdb,busca,cambia):
    # THE REPLACING FUNCTION
    # note that this will break the pdb into individual characters
    # pdbchars has all the lines broken into individual characters
    # for some reason it struggles with busca <= 3

    pdbchars = [[l.strip() for l in line] for line in pdb]
    buscachars = [l.strip() for l in busca]
    cambiachars = [l.strip() for l in cambia]
    rangebusca = findrange(pdb,busca)

    begin = 100   # just as a default
    end = 101     # just as a default

    # not a big fan of nested code...
    newpdb = []
    for counter, line in enumerate(pdbchars):
        newline = []
        b = 0
        charcount = 0
        if checkinrange(counter,rangebusca) == True:
            for char in line:
                newline.append(char)
        elif checkinrange(counter,rangebusca) == False:
            print "yes\n"
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
        newpdb.append(newline)

    return newpdb

def checkinrange(counter,rangebusca):
    if len(rangebusca) == 1:
        if counter not in range(rangebusca[0][0], rangebusca[0][-1]):
            return True
    elif len(rangebusca) >= 2:
        for l in rangebusca:
            for value in range(l[0], l[-1]):
                if counter != value:
                    return True
    else:
        return False

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
    print ("\nCurrently working on ATOM to HETATM conversion\n" +
           "I also want to add a 'replace entire column' option,\n" +
           "but I could use some help to increase functionality,\n" +
           "so be sure to fork it on github :D\n")
    sys.exit("\n\nQuitting the session...\n" + "-"*20 +
             "\nThank you for using PDB-parser!\n")

def continuar():
    # the "are you sure?" function
    return raw_input("\nContinue? [yes|no]\t").lower().startswith('y')

def quitsesh():
    # quit, of course
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
            quitsesh()

        try:
            readypdb = reconstruct(newpdb)
            print "\n*Successfully reconstructed new PDB structure!*\n"
        except:
            print "\nWoops, something went wrong when reconstructing the PDB!\n"
            quitsesh()

        try:
            outputfile(readypdb,outfile)
            print "*Successfully created new PDB file!*\n"
        except:
            print "\nWoops, something went wrong when creating the PDB!\n"
            quitsesh()

    else:
        print "\nCould not open file\nMake sure you type the correct directory and file name\n"
        quitsesh()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        quitsesh()

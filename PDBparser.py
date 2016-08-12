#!/usr/bin/env python

'''                     
    Copyright 2016 Nicolas Pettican

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''

import os
import sys
import re
from itertools import groupby
from operator import itemgetter

# optional user input file location
#DATADIR = raw_input("\nINPUT FILE LOCATION: ")
#DATAFILE = raw_input("\nINPUT FILE NAME: ")
#OUTFILE = raw_input("\nOUTPUT FILE NAME: ")
DATADIR = "G:\MSc\RP2\PyTests"
DATAFILE = "5erdB.pdb"
OUTFILE = "5erdtest.pdb"
AAS = ["ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLY", 
      "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", 
      "SER", "THR", "TRP", "TYR", "VAL", "GLU"]

def parse(datafile):
    # nothing clever here, the file parser
    data = [line.strip() for line in open(datafile, 'r')]
    return data

def welcome():
    # opening credits
    print ('''
 ____  ____  ____                                 
|  _ \|  _ \| __ ) _ __   __ _ _ __ ___  ___ _ __ 
| |_) | | | |  _ \| '_ \ / _` | '__/ __|/ _ \ '__|
|  __/| |_| | |_) | |_) | (_| | |  \__ \  __/ |   
|_|   |____/|____/| .__/ \__,_|_|  |___/\___|_|   
                  |_|                             
                         by Nicolas Pettican
    ''')
    #print ("#" * 25 + "\n#\t\t\t#\n#\tPDB-parser\t#" + "\n#\t\t\t#" +
    #       "\n#  by Nicolas Pettican  #" + "\n#\t\t\t#\n" + "#" *25 + "\n")

def lineheads(datafile):
    # finds and prints the different elements in line[0]
    data = [line.strip().split() for line in open(datafile, 'r')]
    print "The file has %s lines\n" %(len(data))
    lineheadset = set()
    for line in data:
        if line[0] != "END":
            lineheadset.add(line[0])
    # prints the element types, found at line[0]
    for element in set(lineheadset):
        x = [line[0].count(element) for line in data]
        print "{x} of which are {y} elements\n".format(x=x.count(1), y=element)

def optionsbegin(pdb):
    # options the user has
    while True:
        try:
            choice = int(raw_input("What would you like to do to the PDB file?\n" +
                           "Here are the current options:\n\n" +
                           "Option 1 - Replace characters    # it will replace every instance of those characters\n" +
                           "Option 2 - ATOM to HETATM        # converts user-chosen ATOMs to HETATMs\n" + 
                           "Option 3 - HETATM to ATOM        # converts user-chosen HETATMs to ATOMs\n" +
                           "Option 4 - Future options        # future options will be available\n" +
                           "Option 5 - Quit\n\nOption: "))
        except ValueError:
            continue
        if 1 <= choice <= 5:
            return choice

def findelement(pdb,busca):
    # finds where the elements to change are
    return sum(1 for l in pdb if re.search(busca, l))

def findrange(pdb,busca):
    # finds the range/s where the query "busca" is
    rangebusca = [i for i, line in enumerate(pdb) if re.search(busca, line)]
    realranges = [map(itemgetter(1), value)
                  for i, value in groupby(enumerate(rangebusca),
                  lambda (i, x): i-x)]
    if len(realranges) == 1:
        return [[realranges[0][0], realranges[0][-1] + 1]]
    elif len(realranges) >= 2:
        return [[realranges[i][0], realranges[i][-1] + 1]
                for i, line in enumerate(realranges)]

def findindex(pdb,busca):
    # finds what column the query string is
    datalist = [line.split() for line in pdb if re.search(busca, line)]
    temp = set()
    tempupdate = [temp.add(index) for i, value in enumerate(datalist)
                  for index, l in enumerate(datalist[i], 1) if re.search(busca, l)]
    return list(temp)

def replacechar(pdb):
    # to change user defined characters within the PDB
    try:
        busca = raw_input("\nInsert characters you want to look for:\t")
        while not (len(busca) > 2):
            busca = raw_input("\n*Note that it must be 3 or more characters*\t")
        instances = findelement(pdb,busca)
        rangebusca = findrange(pdb,busca)
        # PRINTS THE RANGE
        if len(rangebusca) == 1:
            print "\n%s appears %s times in lines %s to %s" %(busca, instances, rangebusca[0][0], rangebusca[0][-1])
        elif len(rangebusca) >= 2:
            print "\n%s appears %s times in lines %s" %(busca, instances, rangebusca)
    except:
        print "\nWoops, can't seem to find %s\n" %(busca)
    # PRINTS THE COLUMN LOCATION OF QUERY
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
    option = 0  # just as a default
    try:
        cambia = raw_input("Insert number or string you want to replace it with:\t")
        if len(busca) == len(cambia):
            convertrange = rangebusca
            newpdb = replace(pdb,busca,cambia,convertrange,option)
            return newpdb
        else:
            print ("\nReplacing a string of different size may break the PDB.\n")
            if continuar():
                convertrange = rangebusca
                newpdb = replace(pdb,busca,cambia,convertrange,option)
                return newpdb
            else:
                quitsesh()
    except:
        print "\nWoops, something went wrong replacing the string\n"
        quitsesh()

def replace(pdb,busca,cambia,convertrange,option):
    # THE REPLACING FUNCTION
    # note that this will break the pdb into individual characters
    # pdbchars has all the lines broken into individual characters
    pdbchars = [[l.strip() for l in line] for line in pdb]
    buscachars = [l.strip() for l in busca]
    cambiachars = [l.strip() for l in cambia]
    begin = 100   # just as a default
    end = 101     # just as a default
    # goes through each character and changes under conditions
    newpdb = []
    for counter, line in enumerate(pdbchars):
        newline = []
        checkifrange = checkinrange(counter,convertrange)
        # check if current row is in the range
        if checkifrange:
            for char in line:
                newline.append(char)
        else:
            if option > 0:
                for charcount, char in enumerate(line):
                    if charcount == 0:
                        for x, chars in enumerate(pdbchars[counter][0:6]):
                            newline.append(char.replace(char, cambiachars[x]))
                    elif charcount not in range(0,6):
                        newline.append(char)
            else:
                for charcount, char in enumerate(line):
                    if line[charcount] == buscachars[0] and line[charcount + 1] == buscachars[1] and line[charcount + 2] == buscachars[2]:
                        check = [value for i, value in enumerate(buscachars) if line[charcount + i] == buscachars[i]]
                        if len(check) > 2:
                            begin = charcount
                            end = charcount + len(buscachars)
                            for x, chars in enumerate(pdbchars[counter][begin:end]):
                                newline.append(char.replace(char, cambiachars[x]))
                    elif charcount not in range(begin, end):
                        newline.append(char)
        newpdb.append(newline)

    return newpdb

def checkinrange(counter,convertrange):
    # returns true if the line is not in the range
    if len(convertrange) == 1:
        return [True if counter not in range(convertrange[0][0], convertrange[0][-1]) else False][0]
    elif len(convertrange) >= 2:
        isit = 0
        for r in convertrange:
            if counter not in range(r[0], r[-1]):
                isit += 1
        return [True if isit == len(convertrange) else False][0]
    
def atomtohet(pdb,option):
    # to convert ATOM to HETATM
    elementsofinterest = ["ATOM", "HETATM"]
    data = [line.split() for line in pdb]
    # check what column the elements are in
    try:
        busca = checkforadefault(pdb)
        column = int(findindex(pdb,busca)[0] - 1)
    except:
        print "\nAn error occurred within checkforadefault()!\n"
    lineheadset = set()
    # finds the elements available to substitute
    try:
        for line in data:
            if len(line) > column and line[column] not in AAS and line[0] in elementsofinterest:
                lineheadset.add(line[column])
        for element in set(lineheadset):
            x = [line[column].count(element) for line in data if len(line) > column]
            print "\nFound {y} element {x} times".format(x=x.count(1), y=element)
    except:
        print "\nWoops, could not find elements other than amino acids!\n"
        quitsesh()
    # user chooses which elements to substitute
    try:
        chosen = atomhetoptions(lineheadset)
    except:
        print "\nWoops, failed to find elements!\n"
        quitsesh()
    # find the range of user-input elements
    try:
        rawrange = [findrange(pdb,busca) for busca in chosen]
        convertrange = [x for i in rawrange for x in i]
    except:
        print "\nWoops, could not find range!\n"
    # THE REPLACING SECTION
    try:
        if option == 1:
            busca = "ATOM  "
            cambia = "HETATM"
        elif option == 2:
            cambia = "ATOM  "
            busca = "HETATM"
        newpdb = replace(pdb,busca,cambia,convertrange,option)
        return newpdb
    except:
        print "\nWoops, failed to replace!\n"
    
def checkforadefault(pdb):
    # fun fact, these bellow are the most abundant amino acids in proteins
    # excluding of course NAG and MAN
    defaults = ['LEU', 'SER', 'LYS', 'GLU' 'NAG', 'MAN']
    return [i for i in defaults for line in pdb if re.search(i, line)][0]
    
def atomhetoptions(lineheadset):
    # user enters the desired element/s to substitute
    busca = raw_input("\nWhich element would you like to convert?\n" + 
                      "You can input multiple elements separated by ','\n" + 
                      "e.g.\tNAG, MAN\n\nElement/s: ").split(',')
    buscaset = set()
    tmp = [buscaset.add(i) for i in busca]
    while not any(s in lineheadset for s in busca):
        busca = raw_input("\nCould not find element/s, " + 
                          "try again and enter them correctly.\n" + 
                          "e.g. NAG\tor\tNAG, MAN" +
                          "\n\nElement/s:").split(',')
        buscaset = set()
        tmp = [buscaset.add(i) for i in busca]
    for element in set(buscaset):
        print "\nElement %s found" %(element)
    return [element for element in set(buscaset)]

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
    print ("\nCurrently perfecting ATOM to HETATM conversion\n" +
           "I also want to add a 'replace entire column' option,\n" +
           "but I could use some help to increase functionality,\n" +
           "so be sure to fork it on github :D\n")
    sys.exit("\n\nQuitting the session...\n" + "-"*20 +
             "\nThank you for using PDB-parser!\n")

def continuar():
    # the "are you sure?" function
    return raw_input("Continue? [yes|no]\t").lower().startswith('y')

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
        # GIVE USER OPTIONS
        choice = optionsbegin(pdb)
        if choice == 1:
            newpdb = replacechar(pdb)
        elif choice == 2:
            option = 1
            newpdb = atomtohet(pdb,option)
        elif choice == 3:
            option = 2
            newpdb = atomtohet(pdb,option)
        elif choice == 4:
            nothingyet()
        elif choice == 5:
            quitsesh()
        # RECONSTRUCT NEW PDB
        try:
            readypdb = reconstruct(newpdb)
            print "\n*Successfully reconstructed new PDB structure!*\n"
        except:
            print "\nWoops, something went wrong when reconstructing the PDB!\n"
            quitsesh()
        # WRITE NEW PDB TO FILE
        try:
            outputfile(readypdb,outfile)
            print "*Successfully created new PDB file!*\n"
        except:
            print "\nWoops, something went wrong when creating the PDB!\n"
            quitsesh()
    # if user inpyted wrong file info
    else:
        print "\nWoops, could not open file!\nMake sure you type the correct directory and file name!\n"
        quitsesh()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        quitsesh()
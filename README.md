# PDB-parse

By Nicolas Pettican, for the Tabernero and Bella labs, University of Manchester.

### A PDB parser that corrects errors by replacing them with the correct strings

PDB is not my favourite format. In fact its kind of special in that every single white space is important. So forget about importing it into Python, modify it, and output each column separated by a tab.
Why can't biologists just use something easier to manipulate...? :expressionless:

I created this parser in order to modify some characters that are repeated throughout the PDB file. Why do I need this? Because despite all the scientific advancements, there still isn't a straightforward way to e.g. add specific glycans to specific residues in a protein. You kind of have to play around with it. And that can create PDB files that need to be modified. 

Once I get the reconstruct() function finished I can work towards outputing a brand new working PDB file, maybe using a function called output() :punch:.

Feel free to fork it and collaborate! Let us contribute to the advancement of computational biology. I mean, someone has to do it... :metal:

<center><a href="http://www.nicolaspettican.com"><img src="https://raw.githubusercontent.com/nickpettican/SparkzLab/master/img/code_white_small.gif" style="width: 40%; -moz-border-radius: 128px; border-radius: 50%; height: auto; -webkit-border-radius: 50%;"></img></a></center>

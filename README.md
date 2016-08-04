# PDB-parser

By Nicolas Pettican, for the Tabernero and Bella labs, University of Manchester.

---------

### A PDB parser that corrects errors by replacing them with the correct strings

> note that this requires Python 2.7

#### Motivation:

The PDB format is kind of special in that every single white space is important. So forget about importing it into Python, modify it, and outputting each column separated by a tab, it doesn't work.

I created this parser in order to modify characters that are repeated throughout the PDB file. Since there still isn't a straightforward way to e.g. add specific glycans to specific residues in a protein, you kind of have to play around with it. And that can create PDB files that have columns that need to be modified.

#### Development:

At least for my intents and purposes it is finished. However, I do want to improve its functionality, such as changing entire columns if e.g. the order of residues or atoms is wrong or broken and needs mending, or remove the second protein if you have a double protein PDB file.

#### Usage:

To use simply run ```python PDBparser.py``` on your Python environment, or use ```PDBparser.ipynb``` in a iPython or [jupyter notebook](http://jupyter.readthedocs.io/en/latest/install.html). You may want to edit DATADIR, DATAFILE and OUTFILE to your requirements before running.

----------

Feel free to fork it and collaborate! Let us contribute to the advancement of computational biology. :metal:

<br />
<center><a href="https://github.com/nickpettican/PDB-parse/blob/master/PDBparser.py"><img src="https://raw.githubusercontent.com/nickpettican/SparkzLab/master/img/code_white_small.gif" style="width: 40%; border-radius: 50%; height: auto;"></img></a></center>

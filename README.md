# PDB-parse

By Nicolas Pettican, for the Tabernero and Bella labs, University of Manchester.

### A PDB parser that corrects errors by replacing them with the correct strings

PDB is not my favourite format. In fact its kind of special in that every single white space is important. So forget about importing it into Python, modify it, and output each column separated by a tab.
Why can't biologists just use something easier to manipulate...? :expressionless:

I created this parser in order to modify some characters that are repeated throughout the PDB file. Why do I need this? Because despite all the scientific advancements, there still isn't a straightforward way to e.g. add specific glycans to specific residues in a protein. You kind of have to play around with it. And that can create PDB files that need to be modified. 

Once I get the reconstruct() function finished I can work towards outputing a brand new working PDB file, maybe using a function called output() :punch:.

Feel free to fork it and collaborate! Let us contribute to the advancement of computational biology. I mean, someone has to do it... :metal:

<div class="container">
  <div class="row">
    <div class="col-sm-2">
      <a href="http://nicolaspettican.com" style="
        background-position: center center;
        background-repeat: no-repeat;
        background-size: cover;
        height: 0;
        padding-bottom: 100%;
        position: relative;
        width: 100%;
        background-image: url(http://www.nicolaspettican.com/img/guy_white.gif);
        display: block;
        height: auto;
        max-width: 100%;
        border-radius: 50%;"></a>
    </div>
  </div>
</div>

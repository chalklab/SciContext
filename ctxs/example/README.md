# Example: A JSON-LD data file and its context file
Below is a small example of how a JSON-LD context file works, when loaded at the top of a JSON-LD data file (if the data
file is small the context definition can be in the document, however if you have lots of data files in the same format it
makes sense to create one context file, and load it at the top of each data file).

<div align="center"><img src="images/example_file.png" alt="JSON-LD data file" width="700"></div>

In the data file above there are four pieces of data about a chemical compounds: name, formula, molecular weight and 
"[chebi](https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:16716)", a semantic identifier for benzene. Looking at
this information (as humans do) we understand what the first three are as we understand the meaning of the data labels
(and we have learned about ChEBI we it also).  However, in this JSON-LD file the data is just text and thus there is no
representation of the meaning in the file... unless we add meaning by defining semantically what each data element
means.  The JSON-LD file below defines the meaning for each of the data elements above, and includes statements defining
the datatype of each element.

<div align="center"><img src="images/example_ctx.png" alt="JSON-LD context file" width="600"></div>

To prove this works and produces valid RDF you can use the JSON-LD Playground to convert the file to RDF in different 
formats.  You can see this by clicking this [link](https://tinyurl.com/2mkhg6f4). The RDF that is produced is 
(shortened for clarity):

![example_rdf.png](images/example_rdf.png)
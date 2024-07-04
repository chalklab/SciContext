## SciContext: A JSON-LD Context File Development System
This project is to develop a web-based processing system, built in Django, to manage the creation of [JSON-LD](https://json-ld.org/) 
context files. As JSON-LD files are an encoding of the resource description framework ([RDF](https://www.w3.org/TR/rdf11-schema/)) 
data, context file needed to add semantic annotation of (the meaning) data defined in a JSON-LD file, this allowing 
conversion to RDF [triples](https://en.wikipedia.org/wiki/Semantic_triple).

This application can be used with any JSON-LD data, however it was developed with the SciData framework data format in 
mind, that encourages creating context files for metadata elements in a specific knowledge domain (i.e. a minimal metadata standard)
which can be reused in multiple places, published as a standard, and then be used across different diciplines, as needed.

Additionally, this application allows the publication of the context files created, by publishing them to the GitHub pages
branch of your GitHub repository, so that the files can be managed and publised easily in one system.
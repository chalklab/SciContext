""" functions for the ChEMBL API"""
from config.models import *
from ols_py.client import *


def svronts(svrid):
    # get the list of ontologies in this server
    svr = Servers.objects.get(id=svrid)
    olist = []
    # what type of server?
    if svr.type == 'ols':
        client = Ols4Client(svr.apiurl)
        resp = client.get_ontologies(0, 300)
        onts = resp.embedded.ontologies
        for ont in onts:
            meta = ont.config
            # ontologyID is used as the pk for the ontology
            olist.append({'ns': ont.ontologyId, 'title': meta['title'], 'description': meta['description'],
                          'path': meta['fileLocation'], 'homepage': meta['homepage']})
    else:
        pass
    return olist


def svronttrms(svrid, ontid):
    # get terms in ontology (ontns) on server (svrid)
    svr = Servers.objects.get(id=svrid)
    ont = Onts.objects.get(id=ontid)
    tlist = []
    if svr.type == 'ols':
        client = Ols4Client(svr.apiurl)
        resp = client.get_terms(ont.ns)
        terms = resp.embedded.terms
        for term in terms:
            tlist.append({'title': term.label, 'code': term.ontology_name,
                          'description': term.description[0], 'visible': 'yes', 'ontid': ontid})
    else:
        pass
    return tlist

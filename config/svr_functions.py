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
            olist.append({'ns': ont.ontologyId, 'title': str(meta['title']).strip(), 'description': meta['description'],
                          'path': meta['fileLocation'], 'homepage': meta['homepage'], 'trmcnt': ont.numberOfTerms,
                          'version': ont.version})
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
        resp = client.get_terms(ont.ns, params={"page": 0, "size": 1000})
        terms = resp.embedded.terms
        for term in terms:
            desc = None
            if term.description:
                desc = term.description[0]
            tlist.append({'title': term.label, 'code': term.ontology_name,
                          'description': desc, 'visible': 'yes', 'ontid': ontid})
    else:
        pass
    return tlist


def svrsearch(svrid, query):
    # search for terms in server (svrid)
    svr = Servers.objects.get(id=svrid)
    results = []
    if svr.type == 'ols':
        client = Ols4Client()
        resp = client.search(query, params={"exact": 'true', "rows": 1000})
        hits = resp.response.docs
        for hit in hits:
            if hit['is_defining_ontology'] == 'false':
                continue
            results.append({'title': hit.label, 'desc': hit.description, 'iri': hit.iri, 'type': hit['type']})
    else:
        pass
    return results


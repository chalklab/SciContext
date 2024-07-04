""" functions for the ChEMBL API"""
import json
import urllib.request

apiurl = 'https://www.ebi.ac.uk/ols/api/'
headers = {'Accept': 'application/json'}


def olsonts():
    with urllib.request.urlopen(apiurl + 'ontologies?size=300') as url:
        data = json.loads(url.read().decode())
    onts = data['_embedded']['ontologies']
    olist = []
    for ont in onts:
        meta = ont['config']
        olist.append({'ns': meta['namespace'], 'title': meta['title'],
                      'path': meta['fileLocation'], 'homepage': meta['homepage']})
    return olist


def olsont(ontid):
    with urllib.request.urlopen(apiurl + 'ontologies/' + ontid + '/terms?size=500') as url:
        data = json.loads(url.read().decode())
    terms = data['_embedded']['terms']
    tlist = []
    for term in terms:
        if term['description']:
            desc = str(term['description']).replace('[', '').replace(']', '').replace('\'', '')
        elif term['annotation']:
            ann = term['annotation']
            if 'definition' in ann.keys():
                desc = str(term['annotation']['definition'][0]).replace('[', '').replace(']', '').replace('\'', '')
            else:
                desc = ''
        else:
            desc = ''
        tlist.append((term['iri'], term['label'], desc, term['short_form']))
    return tlist

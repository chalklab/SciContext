import json
import os
import sys
import django
import requests
import config
import pandas as pd
from config.settings import *
from glob import glob
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


if False:
    # aggregate terms from NFDI4Chem terminology server
    # get ontologies
    inturl = 'https://service.tib.eu/ts4tib/api/ontologies'
    ofile = '../static/nfdi/onts.json'
    with open(ofile) as f:
        onts = json.load(f)
    # download the entries for each ontology
    for ont in onts['_embedded']['ontologies']:
        ontid = ont['ontologyId']
        print("ontology" + str(ontid))
        onturl = 'https://service.tib.eu/ts4tib/api/ontologies/' + ontid + '/terms'
        ofile = requests.get(onturl)
        jfile = json.loads(ofile.text)
        if jfile['page']['totalPages'] > 1:
            # keep downloading till done
            numpages = jfile['page']['totalPages']
            for i in range(1, numpages, 1):  # not sure why numpages -1 does not work here...
                nonturl = onturl + '?page=' + str(i) + "&size=20"
                print(nonturl)
                ofile = requests.get(nonturl)
                newfile = requests.get(nonturl)
                njfile = json.loads(ofile.text)
                for n in njfile['_embedded']['terms']:
                    jfile['_embedded']['terms'].append(n)
        with open('../static/nfdi/onts/' + ontid + '.json', 'w') as f:
            f.write(json.dumps(jfile))
        print(ontid + " saved")
    exit()

if False:
    # find terms through search
    srcstr = "https://service.tib.eu/ts4tib/api/search?q=*term*&exclusiveFilter=false&exact=true&obsoletes=false&local=false&rows=10&format=json"
    tfile = '../static/iupac/trs_terms.json'
    with open(tfile) as f:
        terms = json.load(f)
    done = []
    for trmid, term in terms.items():
        if '\"' in term or "<" in term or "/" in term or term in done:
            continue
        print(term)
        src = srcstr.replace('*term*', term)
        stmp = requests.get(src)
        srcresp = json.loads(stmp.text)
        with open('../static/iupac/trmsch/' + term + '.json', 'w') as f:
            f.write(json.dumps(srcresp))
        done.append(term)
        print(srcresp)
    print(done)


def grouped(iterable, grp):
    return zip(*[iter(iterable)]*grp)


if False:
    # get the stats for the terms in the NFDI TS
    from glob import glob

    stats = {}
    for fname in glob("../static/iupac/trmsch/*.json"):
        with open(fname, 'r') as f:
            tmp = json.load(f)
            if tmp['response']['numFound'] > 0:
                term = fname.replace('.json', '').replace('../static/iupac/trmsch/', '')
                onts = tmp['facet_counts']['facet_fields']['ontology_name']
                ostats = {}
                for abbrev, cnt in grouped(onts, 2):
                    if cnt > 0:
                        ostats[abbrev] = cnt

                stats.update({term: {'count': tmp['response']['numFound'], 'stats': ostats}})
            else:
                continue
            print("added " + term)
    with open('../static/iupac/trmstats_detail.json', 'w') as f:
        f.write(json.dumps(stats))
    sterms = sorted(stats)
    counts = {}
    for sterm in sterms:
        counts.update({sterm: stats[sterm]['count']})
    with open('../static/iupac/trmstats.json', 'w') as f:
        f.write(json.dumps(counts))
    exit()

if False:
    # generate aggregate stats
    onts = {}
    tfile = '../static/iupac/trmstats_detail.json'
    with open(tfile) as f:
        tstats = json.load(f)
    for term, stats in tstats.items():
        cnts = stats['stats']
        for abbrev, cnt in cnts.items():
            if abbrev not in onts.keys():
                onts.update({abbrev: cnt})
            else:
                onts[abbrev] += cnt
    with open('../static/iupac/ontstats.json', 'w') as f:
        f.write(json.dumps(onts))
    exit()

if True:
    with open('../static/iupac/ontstats.json', encoding='utf-8') as f:
        tmp = json.load(f)

    with open("../static/iupac/ontstats.csv", "w", newline="") as f:
        w = csv.DictWriter(f, tmp.keys())
        w.writeheader()
        w.writerow(tmp)

""" terms view file """
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from config.functions import *
from django.http import JsonResponse
from datetime import datetime
import urllib.request
import json


# Create your views here.
def index(request):
    """view to generate list of namespaces"""
    termz = gettrms()
    return render(request, "terms/index.html", {'terms': termz})


def view(request, trmid):
    """view to show all data about an ont term"""
    term = gettrm(trmid)
    nsiri = term.ont.ns + ':' + term.code
    flds = term.fields_set.all()
    return render(request, "terms/view.html", {'term': term, 'nsiri': nsiri, 'flds': flds})


def add(request):
    """add a term or create a page so a user can do that"""
    if request.method == "POST":
        # save new term
        data = request.POST
        term = Terms()
        term.title = data['title']
        term.definition = data['definition']
        term.code = data['code']
        ont = Onts.objects.get(ns=data['ns'], server_id=data['svrid'])  # ns is the text code for the ontology
        term.ont_id = ont.id
        term.iri = ont.path + ':' + data['code']
        term.updated = datetime.now()
        term.save()
        return redirect('/terms/')

    svrs = Servers.objects.all()
    return render(request, "terms/add.html", {'svrs': svrs})


@csrf_exempt
def byont(request, svrid, ontid):
    svr = Servers.objects.get(id=svrid)
    with urllib.request.urlopen(svr.apiurl + 'ontologies/' + ontid + '/terms?size=500') as url:
        data = json.loads(url.read().decode())
    terms = data['_embedded']['terms']
    tlist = []
    for term in terms:
        tlist.append({"label": term['label'], "code": term['short_form']})
    return JsonResponse(tlist, safe=False, status=200)


@csrf_exempt
def trmsrc(request, svrid, srcstr):
    svr = Servers.objects.get(id=svrid)
    with urllib.request.urlopen(svr.apiurl + 'search?q=' + srcstr + '&rows=1000&lang=en') as url:
        data = json.loads(url.read().decode())
    terms = data['response']['docs']
    # return JsonResponse(terms, safe=False, status=200)
    tlist = {}
    for term in terms:
        # ignore duplicates using the term code
        if 'short_form' not in term.keys():
            continue
        if term['short_form'] in tlist.keys():
            continue
        if len(term['description']) == 0:
            desc = "Not available"
        else:
            tmp = term['description']
            desc = tmp[0]
        tlist.update({term['short_form']: {"title": term['label'], 'defn': desc, 'ns': term['ontology_name']}})
    # generate output list of dictionaries
    output = []
    for key, value in tlist.items():
        # add the ontology ID in the database
        ont = Onts.objects.get(ns=value['ns'], server_id=svr.id)
        output.append({"code": key, "title": value['title'], "defn": value['defn'], "ns": value['ns'], "ontid": ont.id})
    # sort
    out2 = sorted(output, key=lambda d: d['title'])
    return JsonResponse(out2, safe=False, status=200)

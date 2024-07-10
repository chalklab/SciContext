""" terms view file """
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from config.functions import *
from django.http import JsonResponse
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
        # save new namespace
        data = request.POST
        term = Terms()
        term.title = data['title']
        term.definition = data['definition']
        term.code = data['code']
        term.ontid = data['nsid']
        ont = Onts.objects.get(id=data['nsid'])
        term.url = ont.ns + ':' + data['code']
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
    with urllib.request.urlopen(svr.apiurl + 'search?q=' + srcstr + '&lang=en') as url:
        data = json.loads(url.read().decode())
    terms = data['response']['docs']
    # return JsonResponse(terms, safe=False, status=200)
    tlist = []
    for term in terms:
        if len(term['description']) == 0:
            desc = "Not available"
        else:
            tmp = term['description']
            desc = tmp[0]
        tlist.append({"code": term['short_form'], "label": term['label'], 'desc': desc})
    return JsonResponse(tlist, safe=False, status=200)

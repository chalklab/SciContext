""" onts view file """
from django.shortcuts import render, redirect
from config.functions import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import urllib.request
import json


def index(request):
    """view to generate list of namespaces"""
    onts = getonts()
    return render(request, "onts/index.html", {'onts': onts})


def view(request, ontid):
    """view to show all data about a namespace"""
    ont = getont(ontid)
    trms = gettrms(ontid)
    if not trms:
        # on terms loaded so go get list from the server
        loaded = 'no'
        svrid = ont.server.id
        trms = svronttrms(svrid, ontid)
    else:
        loaded = 'yes'

    return render(request, "onts/view.html", {'ont': ont, 'trms': trms, 'loaded': loaded})


def add(request):
    """add a new ontology"""
    if request.method == "POST":
        # save new namespace
        data = request.POST
        o = Onts()
        o.name = data['name']
        o.ns = data['alias']
        o.path = data['path']
        o.homepage = data['homepage']
        o.server_id = data['svrid']
        o.save()
        return redirect('/onts/')

    aliases = ontaliases()
    svrs = Servers.objects.all().values_list('id', 'name').order_by('name')
    oonts = allonts()  # list of tuples (four values)
    # oonts.sorted(key=lambda tup: tup[1])
    return render(request, "onts/add.html", {'aliases': aliases, 'onts': oonts, 'svrs': svrs})


# JavaScript functions


@csrf_exempt
def ontget(request, svrid, ontid):
    # get current list of ontologies on server
    sonts = svronttrms(svrid, ontid)
    return JsonResponse(sonts, safe=False, status=200)


@csrf_exempt
def ontupd(request, svrid, ontid):
    # load DB with list of terms in an ontology (from a specific server)
    ontload(svrid, ontid)
    return redirect('/onts/view/' + str(ontid))


@csrf_exempt
def bysvr(request, svrid):
    # get a list of ontologies on a server
    svr = Servers.objects.get(id=svrid)
    with urllib.request.urlopen(svr.apiurl + 'ontologies?size=10000') as url:
        data = json.loads(url.read().decode())
    onts = data['_embedded']['ontologies']
    ontlist = []
    for ont in onts:
        meta = ont['config']
        ontlist.append({"ns": meta['namespace'], "title": meta['title'], "count": ont['numberOfTerms']})
    return JsonResponse(ontlist, safe=False, status=200)

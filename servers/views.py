""" servers view file """
from django.shortcuts import render, redirect
from config.functions import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime


# Create your views here.
def index(request):
    """view to generate list of ontology servers"""
    servers = getsvrs()
    return render(request, "servers/index.html", {'servers': servers})


def view(request, svrid):
    """view to show all data about an ontology server"""
    server = getsvr(svrid)
    return render(request, "servers/view.html", {'server': server})


def add(request):
    # add a server
    if request.method == "POST":
        # save new namespace
        post = request.POST  # post is immutable QueryDict
        data = post.copy()  # required to identify empty values (creates mutable QueryDict)
        for key in data.keys():  # only expecting single values for each field
            if data[key]:
                if data[key][0] == '':
                    data[key][0] = None
            else:
                data[key] = None
        s = Servers()
        s.name = data['name']
        s.abbrev = data['abbrev']
        s.description = data['desc']
        s.homepage = data['home']
        s.apiurl = data['apiurl']
        s.apikey = data['apikey']
        s.headers = data['headers']
        s.type = data['type']
        s.updated = datetime.datetime.now()
        s.save()
        return redirect('/servers/')

    return render(request, "servers/add.html", {})


# JavaScript AJAX functions


@csrf_exempt
def svrget(request, svrid):
    # get current list of ontologies on server
    sonts = svronts(svrid)
    return JsonResponse(sonts, safe=False, status=200)


@csrf_exempt
def ontupd(request, svrid):
    # load DB with a list of ontologies on server
    svrload(svrid)
    return redirect('/servers/view/' + str(svrid))


@csrf_exempt
def updontcnt(request, svrid):
    onts = svronts(svrid)
    output = []
    for ont in onts:
        o = Onts.objects.get(ns=ont['ns'], server_id=svrid)
        o.trmcnt = ont['trmcnt']
        o.save()
        ostr = ont['ns'] + " updated"
        output.append(ostr)
    return JsonResponse(output, safe=False, status=200)


@csrf_exempt
def updontvrs(request, svrid):
    onts = svronts(svrid)
    output = []
    for ont in onts:
        o = Onts.objects.get(ns=ont['ns'], server_id=svrid)
        o.version = ont['version']
        o.updated = datetime.now()
        o.save()
        ostr = ont['ns'] + " updated"
        output.append(ostr)
    return JsonResponse(output, safe=False, status=200)

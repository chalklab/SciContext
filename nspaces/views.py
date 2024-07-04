""" namespaces view file """
from django.shortcuts import render, redirect
from config.functions import *


def index(request):
    """view to generate list of namespaces"""
    spaces = getnsps()
    return render(request, "nspaces/index.html", {'spaces': spaces})


def view(request, nspid):
    """view to show all data about a namespace"""
    space = getnsp(nspid)
    return render(request, "nspaces/view.html", {'space': space})


def add(request):
    """view to add data about a namespace"""
    if request.method == "POST":
        # save new namespace
        data = request.POST
        nspace = Nspaces()
        nspace.name = data['name']
        nspace.ns = data['alias']
        nspace.path = data['path']
        nspace.homepage = data['homepage']
        nspace.save()
        return redirect('/nspaces/')

    aliases = nsaliases()
    oonts = olsonts()  # list of tuples (four values)
    oonts.sort(key=lambda tup: tup[1])
    return render(request, "nspaces/add.html", {'aliases': aliases, 'onts': oonts})

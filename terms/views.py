""" terms view file """
from django.shortcuts import render, redirect
from config.functions import *


# Create your views here.
def index(request):
    """view to generate list of namespaces"""
    termz = gettrms()
    return render(request, "terms/index.html", {'terms': termz})


def view(request, trmid):
    """view to show all data about an ont term"""
    term = gettrm(trmid)
    nsiri = term.ont.ns + ':' + term.code
    return render(request, "terms/view.html", {'term': term, 'nsiri': nsiri})


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

    onts = Onts.objects.all().values_list('id', 'name').order_by('name')
    aliases = ontaliases()
    kept = []
    # remove entries that are not in the namespace list
    for i, ont in enumerate(onts):
        if ont[0] in aliases:
            kept.append(ont)
    return render(request, "terms/add.html",
                  {'onts': onts, 'kept': kept, 'aliases': aliases})

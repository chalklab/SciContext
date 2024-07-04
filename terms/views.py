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
    space = getnsp(term.nspace_id)
    uri = term.url.replace(space.ns + ':', space.path)
    return render(request, "terms/view.html", {'term': term, 'uri': uri})


def add(request):
    """view to show all data about a term"""
    if request.method == "POST":
        # save new namespace
        data = request.POST
        term = Terms()
        term.title = data['title']
        term.definition = data['definition']
        term.code = data['code']
        term.nspace_id = data['nsid']
        ns = Nspaces.objects.get(id=data['nsid'])
        term.url = ns.ns + ':' + data['code']
        term.save()
        return redirect('/terms/')

    sdsects = [('methodology', 'Methodology (the "how" section)'), ('system', 'System (the "what" section)'),
               ('dataset', 'Dataset (the "data" section)')]
    subsects = [('procedure', 'methodology', 'Procedure'), ('chemical', 'system', 'Chemical'),
                ('exptdata', 'dataset', 'Experimental data')]

    nss = Nspaces.objects.all().values_list('id', 'name').order_by('name')
    if not nss:
        # load ols ontologies into the nspaces table
        ols = olsonts()
        olsload(ols)
        nss = Nspaces.objects.all().values_list('id', 'name').order_by('name')
    aliases = nsaliases()
    onts = olsonts()  # list of tuples (four elements)
    kept = []
    onts.sort()
    # remove entries that are not in the namespace list
    for i, ont in enumerate(onts):
        if ont[0] in aliases:
            kept.append(ont)
    return render(request, "terms/add.html",
                  {'nss': nss, 'sdsects': sdsects, 'subsects': subsects, 'onts': kept, 'aliases': aliases})

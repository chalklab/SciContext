""" servers view file """
from django.shortcuts import render, redirect
from config.functions import *


# Create your views here.
def index(request):
    """view to generate list of ontology servers"""
    projects = getprjs()
    return render(request, "projects/index.html", {'projects': projects})


def view(request, prjid):
    """view to show all data about an ontology server"""
    project = getprj(prjid)
    return render(request, "projects/view.html", {'project': project})


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
        p = Projects()
        p.name = data['name']
        p.description = data['desc']
        p.prefix = data['prefix']
        p.prjurl = data['prjurl']
        p.updated = datetime.datetime.now()
        p.save()
        return redirect('/projects/')

    return render(request, "servers/add.html", {})

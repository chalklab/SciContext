""" fields view file """
from django.shortcuts import render
from config.functions import *


def index(request):
    """view to generate list of namespaces"""
    fields = getflds()
    return render(request, "fields/index.html", {'fields': fields})


def view(request, fldid):
    """view to show all data about a namespace"""
    field = getfld(fldid)
    return render(request, "fields/view.html", {'field': field})

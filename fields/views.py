""" fields view file """
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from config.functions import *
from datetime import datetime
import json


def index(request):
    """view to generate list of namespaces"""
    fields = getflds()
    return render(request, "fields/index.html", {'fields': fields})


def view(request, fldid):
    """view to show all data about a namespace"""
    field = getfld(fldid)
    return render(request, "fields/view.html", {'field': field})


@csrf_exempt
def add(request):
    # save new field
    if request.method == "POST":
        data = request.POST
        ctxid = data['ctxid']
        fld = Fields()
        fld.name = data['name']
        fld.term_id = data['term_id']
        fld.category = data['category']
        fld.container = json.dumps(data['container'])
        fld.datatype = data['datatype']
        fld.updated = datetime.now()
        fld.save()
        if ctxid != "":
            # save join table entry
            cf = ContextsFields()
            cf.context_id = ctxid
            cf.field_id = fld.id
            cf.updated = datetime.now()
            cf.save()
        return redirect('/fields/view/' + str(fld.id))

    trms = Terms.objects.all()
    return render(request, "fields/add.html", {'trms': trms})

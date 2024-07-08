""" fields view file """
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from config.functions import *
from datetime import datetime


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
    """view to add data about a field"""
    if request.method == "POST":
        # save new field
        data = request.POST
        cwkid = data['cwkid']
        cxtid = data['cxtid']
        fld = Fields()
        fld.name = data['name']
        fld.description = data['description']
        fld.filename = data['filename']
        fld.updated = datetime.now()
        fld.save()
        status = "success"
        if not fld.id:
            status = "error"
            fld.id = None
        # TODO: save field entries that have not been saved?
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': status, 'fldid': fld.id})
        else:
            return redirect('/fields/view/' + str(fld.id))
    else:
        return render(request, "fields/add.html")
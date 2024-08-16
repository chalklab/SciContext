""" fields view file """
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from config.functions import *
from datetime import datetime
from django.http import JsonResponse
import json


def index(request):
    """view to generate list of namespaces"""
    flds = getflds()
    return render(request, "fields/index.html", {'flds': flds})


def view(request, fldid):
    """view to show all data about a namespace"""
    field = getfld(fldid)
    ctxids = field.contextsfields_set.all().values_list('context_id', flat=True)
    ctxs = Contexts.objects.filter(id__in=ctxids)
    ctxlist = []
    for ctx in ctxs:
        ctxlist.append(ctx.id)
    allctxs = Contexts.objects.all()
    return render(request, "fields/view.html",
                  {'field': field, 'ctxs': ctxs, 'allctxs': allctxs, 'ctxlist': ctxlist})


def edit(request, fldid):
    # edit field
    if request.method == "POST":
        data = request.POST
        fld = Fields.objects.get(id=fldid)
        fld.name = data['name']
        fld.term_id = data['term_id']
        fld.category = data['category']
        fld.container = ",".join(data.getlist('container'))
        fld.datatype = data['datatype']
        fld.updated = datetime.now()
        fld.save()
        return redirect('/fields/view/' + fldid)

    # send data to view
    field = getfld(fldid)
    ctxids = field.contextsfields_set.all().values_list('context_id', flat=True)
    ctxs = Contexts.objects.filter(id__in=ctxids)
    ctxlist = []
    for ctx in ctxs:
        ctxlist.append(ctx.id)
    allctxs = Contexts.objects.all()
    trms = gettrms()
    return render(request, "fields/edit.html",
                  {'fld': field, 'ctxs': ctxs, 'allctxs': allctxs, 'ctxlist': ctxlist,
                   'act': 'Edit', 'trms': trms})


def delete(request):
    if request.method == "POST":
        fldid = request.POST['fldid']
        ctxid = request.POST['ctxid']
        fcjoin = ContextsFields.objects.get(field_id=fldid, context_id=ctxid)
        fcjoin.delete()
        resp = "success"
    else:
        resp = "error"
    return JsonResponse(resp, safe=False, status=200)


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
        fld.container = data['container']
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
            return redirect('/contexts/view/' + str(ctxid))
        else:
            return redirect('/fields/view/' + str(fld.id))

    trms = Terms.objects.all()
    return render(request, "fields/add.html", {'trms': trms, 'act': 'Add'})


@csrf_exempt
def read(request, fldid):
    """TODO: field updating in the context view page"""
    field = getfld(fldid)
    output = {}
    output.update({"name": field.name})
    output.update({"category": field.category})
    output.update({"datatype": field.datatype})
    output.update({"term_id": field.term_id})
    output.update({"container": json.loads(field.container)})
    return JsonResponse(output, safe=False, status=200)


@csrf_exempt
def join(request):
    """ add a link between a context and a field"""
    if request.method == "POST":
        data = request.POST
        link = ContextsFields(field_id=data['fldid'], context_id=data['ctxid'], updated=datetime.now())
        link.save()
        if link.id:
            return JsonResponse("success", safe=False, status=200)
        else:
            return JsonResponse("error", safe=False, status=200)
    else:
        return redirect('/fields')

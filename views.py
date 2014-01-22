from django.core.cache import cache
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponsePermanentRedirect
from base64 import b64encode, b64decode
from hkgmcwl.jsonapi import *
from random import randint
import json

def index(request):
    return render(request, 'index.html', {})
    
def error(request, code):
    errorMsg = "Error code {0}".format(code)
    context = {"error": errorMsg}
    return render(request, 'index.html', context)
    
def confirmPage(request):
    try:
        int(request.GET["hkg_uid"])
    except:
        return HttpResponsePermanentRedirect("../error/1")
    jsonString = json.dumps({"hkg_uid": request.GET["hkg_uid"], "ig_name": request.GET["ig_name"]})
    base64encoded = b64encode(jsonString.encode())
    context = {"hkg_uid": request.GET["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14)}
    return render(request, 'confirm.html', context)
    
def confirmError(request):
    jsonString = json.dumps({"hkg_uid": request.GET["hkg_uid"], "ig_name": request.GET["ig_name"]})
    base64encoded = b64encode(jsonString.encode())
    context = {"hkg_uid": request.GET["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14)}
    return render(request, 'confirm.html', context)
    
def confirm(request):
    jsonString = json.dumps({"hkg_uid": request.GET["hkg_uid"], "ig_name": request.GET["ig_name"]})
    base64encoded = b64encode(jsonString.encode())
    context = {"hkg_uid": request.GET["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14)}
    return render(request, 'confirm.html', context)
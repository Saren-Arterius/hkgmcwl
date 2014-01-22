from django.core.cache import cache
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import StreamingHttpResponse, HttpRequest
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
    json = json.dumps({"hkg_uid": HttpRequest.GET["hkg_uid"], "ig_name": HttpRequest.GET["ig_name"]})
    base64encoded = base64.b64encode(json)
    context = {"hkg_uid": HttpRequest.GET["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14)}
    return render(request, 'confirm.html', context)
    
def confirmError(request):
    json = json.dumps({"hkg_uid": HttpRequest.GET["hkg_uid"], "ig_name": HttpRequest.GET["ig_name"]})
    base64encoded = base64.b64encode(json)
    context = {"hkg_uid": HttpRequest.GET["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14)}
    return render(request, 'confirm.html', context)
    
def confirm(request):
    json = json.dumps({"hkg_uid": HttpRequest.GET["hkg_uid"], "ig_name": HttpRequest.GET["ig_name"]})
    base64encoded = base64.b64encode(json)
    context = {"hkg_uid": HttpRequest.GET["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14)}
    return render(request, 'confirm.html', context)
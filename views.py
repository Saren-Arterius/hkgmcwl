from django.core.cache import cache
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponsePermanentRedirect
from base64 import b64encode, b64decode
from hkgmcwl.jsonapi import *
from random import randint
from re import findall
import json

def index(request):
    return render(request, 'index.html', {})
    
def error(request, code):
    errorMsg = "Error code {0}".format(code)
    context = {"error": errorMsg}
    return render(request, 'index.html', context)
    
def confirmPage(request):
    try:
        isValid(request.GET)
    except Exception as e:
        return HttpResponsePermanentRedirect("../error/{0}".format(e))
    jsonString = json.dumps({"hkg_uid": request.GET["hkg_uid"], "ig_name": request.GET["ig_name"]})
    base64encoded = b64encode(jsonString.encode())
    context = {"hkg_uid": request.GET["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14)}
    return render(request, 'confirm.html', context)

def confirm(request, base64encoded)):
    jsonString = b64decode(base64encoded.decode())
    data = json.loads(jsonString)
    raise Exception(data)


def confirmError(request, base64encoded):
    jsonString = b64decode(base64encoded.decode())
    data = json.loads(jsonString)
    raise Exception(data)

def isValid(dict):
    try:
        dict["hkg_uid"]
    except:
        raise Exception("1") #Not exist
        
    try:
        dict["ig_name"]
    except:
        raise Exception("2") #Not exist
        
    try:
        int(dict["hkg_uid"])
    except:
        raise Exception("3") #Not correct
        
    if len(str(dict["hkg_uid"])) > 6:
        raise Exception("4") #Too long
        
    if len(dict["ig_name"]) not in range(3,21):
        raise Exception("5") #Username 3-20

    if findall("^[A-Za-z0-9_]+$", dict["ig_name"]) == 0:
        raise Exception("6") #Regex not match
        
    return True
    
from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hkgmcwl.models import *
from hkgmcwl.views_errormsgs import *
from pyquery import PyQuery as pq
from random import randint
from re import findall
import urllib.request
import json

def password(request):
    if request.GET:
        try:
            Whitelist.objects.filter(hkg_uid = dict["hkg_uid"])
        except Exception as e:
            return HttpResponseRedirect("error/{0}".format(e))
        jsonString = json.dumps({"hkg_uid": request.GET["hkg_uid"], "mc_name": request.GET["mc_name"]})
        base64encoded = b64encode(jsonString.encode())
        return HttpResponseRedirect(base64encoded)
    else:
        return render(request, 'password.html', {})

def passwordValidatePage(request, base64encoded):
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    try:
        isValid(data)
    except Exception as e:
        return HttpResponseRedirect("../error/{0}".format(e))
    context = {"hkg_uid": data["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14)}
    return render(request, 'validate.html', context)

def passwordValidateError(request, code):
    errorMsg = "Error code {0}: {1}".format(code, errorMsgs[code])
    context = {"error": errorMsg}
    return render(request, 'password.html', context)
    
def passwordValidateDo(request, code):
    pass
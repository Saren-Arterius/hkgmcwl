from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hkgmcwl.models import *
from hkgmcwl.methods.errormsgs import *
from hkgmcwl.methods.general import *
from pyquery import PyQuery as pq
from random import randint
from re import findall
import urllib.request
import json

def password(request):
    if request.GET:
        if not Whitelist.objects.filter(hkg_uid = request.GET["hkg_uid"]):
            return HttpResponseRedirect("error/{0}".format(11))
        else:
            return HttpResponseRedirect("{0}".format(request.GET["hkg_uid"]))
    else:
        return render(request, 'password.html', {})

def passwordError(request, code):
    errorMsg = "Error code {0}: {1}".format(code, errorMsgs[code])
    context = {"error": errorMsg}
    return render(request, 'password.html', context)
    
def passwordValidatePage(request, hkg_uid):
    if not Whitelist.objects.filter(hkg_uid = hkg_uid):
        return HttpResponseRedirect("error/{0}".format(11))
    validateString = genPassword(32)
    context = {"hkg_uid": hkg_uid, "validateString": validateString, "server": randint(1,14), "href": hkg_uid}
    return render(request, 'validate.html', context)

def passwordValidateError(request, code):
    errorMsg = "Error code {0}: {1}".format(code, errorMsgs[code])
    context = {"error": errorMsg}
    return render(request, 'password.html', context)
    
def passwordValidateDo(request, code):
    pass
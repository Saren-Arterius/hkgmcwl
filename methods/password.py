from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hkgmcwl.models import *
from hkgmcwl.methods.errormsgs import *
from hkgmcwl.methods.general import *
from base64 import b64encode, b64decode
from pyquery import PyQuery as pq
from random import randint
from re import findall
import urllib.request

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
    cache.add("password_recovery_{0}".format(hkg_uid), genPassword(24))
    validateString = cache.get("password_recovery_{0}".format(hkg_uid))
    context = {"hkg_uid": hkg_uid, "validateString": validateString, "server": randint(1,14), "href": hkg_uid}
    return render(request, 'validate.html', context)

def passwordValidateError(request, code, hkg_uid):
    if not Whitelist.objects.filter(hkg_uid = hkg_uid):
        return HttpResponseRedirect("error/{0}".format(11))
    errorMsg = "Error code {0}: {1}".format(code, errorMsgs[code])
    cache.add("password_recovery_{0}".format(hkg_uid), genPassword(24))
    validateString = cache.get("password_recovery_{0}".format(hkg_uid))
    context = {"hkg_uid": hkg_uid, "validateString": validateString, "server": randint(1,14), "href": hkg_uid, "error": errorMsg}
    return render(request, 'validate.html', context)
    
def passwordValidateDo(request, hkg_uid):
    if not Whitelist.objects.filter(hkg_uid = hkg_uid):
        return HttpResponseRedirect("error/{0}".format(11))

    field = False
    ip = getClientIP(request)
    reqTimesLeft = cache.get("reqTimesLeft_{0}".format(ip))
    if reqTimesLeft is None:
        cache.add("reqTimesLeft_{0}".format(ip), 10, 1800)
    elif reqTimesLeft > 0:
        cache.decr("reqTimesLeft_{0}".format(ip))
    else:
        return HttpResponseRedirect("error/{0}".format(50))

    for server in range(1,15):
        try:
            url = "http://forum{0}.hkgolden.com/ProfilePage.aspx?userid={1}".format(server, hkg_uid)
            request = urllib.request.urlopen(url)
            page = request.read().decode("big5", "replace")
            field = pq(page)("#ctl00_ContentPlaceHolder1_tc_Profile_tb0_lb_website").html()
            break
        except:
            pass

    if not field and field != "":
        return HttpResponseRedirect("error/{0}".format(100)) #Down server
    elif field != cache.get("password_recovery_{0}".format(hkg_uid)):  
        return HttpResponseRedirect("error/{0}".format(101)) #Wrong string
    
    data = Whitelist.objects.filter(hkg_uid = hkg_uid).all()
    for i in data:
        payload = {"password": i.init_password, "mc_name": i.mc_name}
    jsonString = json.dumps(payload)
    base64encoded = b64encode(jsonString.encode()).decode()
    cache.delete("reqTimesLeft_{0}".format(ip))
    return HttpResponseRedirect("../../success/{0}".format(base64encoded))
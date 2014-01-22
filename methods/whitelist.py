from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hkgmcwl.jsonapi import *
from hkgmcwl.models import *
from hkgmcwl.methods.errormsgs import *
from pyquery import PyQuery as pq
from base64 import b64encode, b64decode
from random import randint
from time import time
from re import findall
import urllib.request
import json

def index(request):
    if request.GET:
        try:
            isValid(request.GET)
        except Exception as e:
            return HttpResponseRedirect("error/{0}".format(e))
        jsonString = json.dumps({"hkg_uid": request.GET["hkg_uid"], "mc_name": request.GET["mc_name"]})
        base64encoded = b64encode(jsonString.encode())
        return HttpResponseRedirect(base64encoded)
    else:
        return render(request, 'index.html', {})

def error(request, code):
    errorMsg = "Error code {0}: {1}".format(code, errorMsgs[code])
    context = {"error": errorMsg}
    return render(request, 'index.html', context)

def validatePage(request, base64encoded):
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    try:
        isValid(data)
    except Exception as e:
        return HttpResponseRedirect("../error/{0}".format(e))
    context = {"hkg_uid": data["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14)}
    return render(request, 'validate.html', context)

def validateError(request, base64encoded, code):
    errorMsg = "Error code {0}: {1}".format(code, errorMsgs[code])
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    try:
        isValid(data)
    except Exception as e:
        return HttpResponseRedirect("../error/{0}".format(e))
    context = {"hkg_uid": data["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14), "error": errorMsg}
    return render(request, 'validate.html', context)

def validateDo(request, base64encoded):
    ip = getClientIP(request)

    reqTimesLeft = cache.get("reqTimesLeft_{0}".format(ip))
    if reqTimesLeft is None:
        cache.add("reqTimesLeft_{0}".format(ip), 10, 1800)
    elif reqTimesLeft > 0:
        cache.decr("reqTimesLeft_{0}".format(ip))
    else:
        return HttpResponseRedirect("error/{0}".format(50))
        
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    password = genPassword(16)
    field = False
    try:
        isValid(data)
    except Exception as e:
        return HttpResponseRedirect("error/{0}".format(e))
        
    for server in range(1,15):
        try:
            url = "http://forum{0}.hkgolden.com/ProfilePage.aspx?userid={1}".format(server, data["hkg_uid"])
            request = urllib.request.urlopen(url)
            page = request.read().decode("big5", "replace")
            field = pq(page)("#ctl00_ContentPlaceHolder1_tc_Profile_tb0_lb_website").html()
            break
        except:
            pass

    if not field:
        return HttpResponseRedirect("error/{0}".format(100)) #Down server
    elif field != base64encoded:  
        return HttpResponseRedirect("error/{0}".format(101)) #Wrong string
    try:
        conn = MinecraftJsonApi(host = 'localhost', port = 44446, username = 'admin', password = 'password')
        conn.call("players.name.whitelist", data["mc_name"])
        conn.call("server.run_command", "authme register {0} {1}".format(data["mc_name"], password))
    except:
        return HttpResponseRedirect("error/{0}".format(102)) #Failed to communicate with server
    else:
        newUser = Whitelist.objects.create(ip = ip, time = time(), mc_name = data["mc_name"], hkg_uid = data["hkg_uid"], init_password = password)
        newUser.save()
        payload = {"password": password, "mc_name": data["mc_name"]}
        jsonString = json.dumps(payload)
        base64encoded = b64encode(jsonString.encode()).decode()
        return HttpResponseRedirect("../success/{0}".format(base64encoded))
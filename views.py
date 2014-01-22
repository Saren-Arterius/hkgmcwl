from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hkgmcwl.jsonapi import *
from hkgmcwl.models import *
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
    errorMsg = "Error code {0}".format(code)
    context = {"error": errorMsg}
    return render(request, 'index.html', context)
    
def confirmPage(request, base64encoded):
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    try:
        isValid(data)
    except Exception as e:
        return HttpResponseRedirect("../error/{0}".format(e))
    context = {"hkg_uid": data["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14)}
    return render(request, 'confirm.html', context)

def confirmError(request, base64encoded, code):
    errorMsg = "Error code {0}".format(code)
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    try:
        isValid(data)
    except Exception as e:
        return HttpResponseRedirect("../error/{0}".format(e))
    context = {"hkg_uid": data["hkg_uid"], "base64encoded": base64encoded, "server": randint(1,14), "error": errorMsg}
    return render(request, 'confirm.html', context)

def confirmSuccess(request, base64encoded):
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    raise Exception(data)

def confirmDo(request, base64encoded):
    ip = getClientIP(request)
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
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
    except:
        return HttpResponseRedirect("error/{0}".format(102)) #Failed to communicate with server
    else:
        newUser = Whitelist.objects.create(ip = ip, time = time(), mc_name = data["mc_name"], hkg_uid = data["hkg_uid"])
        newUser.save()
        return HttpResponseRedirect("success")

def isValid(dict):
    try:
        dict["hkg_uid"]
    except:
        raise Exception("1") #Not exist
        
    try:
        dict["mc_name"]
    except:
        raise Exception("2") #Not exist
        
    try:
        int(dict["hkg_uid"])
    except:
        raise Exception("3") #Not correct
        
    if len(str(dict["hkg_uid"])) > 6:
        raise Exception("4") #Too long
    elif len(dict["mc_name"]) not in range(3,21):
        raise Exception("5") #Username 3-20
    elif len(findall("^[A-Za-z0-9_]+$", dict["mc_name"])) == 0:
        raise Exception("6") #Regex not match
    elif Whitelist.objects.filter(hkg_uid = dict["hkg_uid"]):
        raise Exception("7") #hkg_uid exists
    elif Whitelist.objects.filter(mc_name = dict["mc_name"]):
        raise Exception("8") #mc_name exists
    else:
        return True
    
def getClientIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
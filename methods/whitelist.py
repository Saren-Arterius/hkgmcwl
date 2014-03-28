from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponseRedirect
from hkgmcwl.jsonapi import *
from hkgmcwl.models import *
from hkgmcwl.methods.general import *
from pyquery import PyQuery as pq
from base64 import b64encode, b64decode
from random import randint
from time import time
from re import findall
import urllib.request
import json

@cache_page(60 * 15)
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
        return render(request, 'hkgmcwl/index.html', {})

@cache_page(60 * 15)
def error(request, code):
    context = {"error": getErrorMessage(code)}
    return render(request, 'hkgmcwl/index.html', context)

@cache_page(60 * 15)
def validatePage(request, base64encoded):
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    try:
        isValid(data)
    except Exception as e:
        return HttpResponseRedirect("../error/{0}".format(e))
    context = {"hkg_uid": data["hkg_uid"], "validateString": base64encoded, "server": randint(1,14), "href": base64encoded}
    return render(request, 'hkgmcwl/validate.html', context)

@cache_page(60 * 15)
def validateError(request, base64encoded, code):
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    try:
        isValid(data)
    except Exception as e:
        return HttpResponseRedirect("../error/{0}".format(e))
    context = {"hkg_uid": data["hkg_uid"], "validateString": base64encoded, "server": randint(1,14), "error": getErrorMessage(code), "href": base64encoded}
    return render(request, 'hkgmcwl/validate.html', context)

def validateDo(request, base64encoded):
    ip = getClientIP(request)

    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    password = genPassword(16)
    field = False
    try:
        isValid(data)
    except Exception as e:
        return HttpResponseRedirect("error/{0}".format(e))
        
    reqTimesLeft = cache.get("reqTimesLeft_{0}".format(ip))
    if reqTimesLeft is None:
        cache.add("reqTimesLeft_{0}".format(ip), 5, 900)
    elif reqTimesLeft > 0:
        cache.decr("reqTimesLeft_{0}".format(ip))
    else:
        return HttpResponseRedirect("error/{0}".format(50))
        
    from selenium import webdriver
    browser = webdriver.PhantomJS()
    for server in [randint(1,9) for i in range(3)]:
        try:
            url = "http://forum{0}.hkgolden.com/ProfilePage.aspx?userid={1}".format(server, data["hkg_uid"])
            browser.get(url)
            elem = browser.find_element_by_xpath("//*")
            html = elem.get_attribute("outerHTML")
            field = pq(html)("#ctl00_ContentPlaceHolder1_tc_Profile_tb0_lb_website").html()
            break
        except:
            pass
    browser.close()

    if not field and field != "":
        return HttpResponseRedirect("error/{0}".format(100)) #Down server
    elif field != base64encoded:  
        return HttpResponseRedirect("error/{0}".format(101)) #Wrong string
    try:
        conn = MinecraftJsonApi(host = 'localhost', port = 6510, username = 'admin', password = 'password')
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
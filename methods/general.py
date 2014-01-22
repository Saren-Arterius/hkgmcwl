from django.shortcuts import render
from hkgmcwl.models import *
from string import ascii_uppercase, ascii_lowercase, digits
from base64 import b64encode, b64decode
from random import choice
from re import findall
import json

def success(request, base64encoded):
    jsonString = b64decode(base64encoded).decode()
    data = json.loads(jsonString)
    context = {"mc_name": data["mc_name"], "password": data["password"]}
    return render(request, 'success.html', context)

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
    
def genPassword(len):
    return ''.join(choice(ascii_uppercase + ascii_lowercase+ digits) for x in range(len))
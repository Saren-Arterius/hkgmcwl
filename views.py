from django.core.cache import cache
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import StreamingHttpResponse
from hkgmcwl.jsonapi import *

def index(request):
    return render(request, 'index.html', {})
    
def new(request, base64string):
    conn = MinecraftJsonApi(host = '192.168.0.1', port = 44446, username = 'admin', password = 'password')
    a = conn.call("players.name.whitelist", "saren")
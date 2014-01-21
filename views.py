from django.core.cache import cache
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import StreamingHttpResponse
from jsonapi import *

def index(request):
    #return render(request, 'stockprice/index.html', {})
    conn = MinecraftJsonApi(host='localhost', port=44446, username='admin', password='password')
    conn.call("players.name.send_message", "saren", "test")
    return StreamingHttpResponse("terst")
from django.core.cache import cache
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import StreamingHttpResponse

def index(request):
    #return render(request, 'stockprice/index.html', {})
    return StreamingHttpResponse("terst")
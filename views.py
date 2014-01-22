from hkgmcwl.methods.whitelist import *
from hkgmcwl.methods.password import *
from django.http import HttpResponse

def errorHandler(request):
    return HttpResponse(request.META['REQUEST_URI'])
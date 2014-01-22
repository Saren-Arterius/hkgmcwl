from hkgmcwl.methods.whitelist import *
from hkgmcwl.methods.password import *
from django.http import HttpResponseRedirect
from os.path import dirname

def errorHandler(request):
    return HttpResponseRedirect(dirname(request.META['REQUEST_URI']))
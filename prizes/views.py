# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.template.context import Context, RequestContext
from erp.misc.util import *
from erp.prizes.models import Prize

def prize_details(request,owner_name=None):
    prizes=Prize.objects.filter(event=request.user.get_profile ().department).order_by('-pk')
    return render_to_response('prizes/prize_base.html',locals(),context_instance=global_context(request))

def prize_assign(request,owner_name=None):
    prizes=Prize.objects.filter(event=request.user.get_profile ().department)
    return render_to_response('prizes/prize_assign.html',locals(),context_instance=global_context(request))

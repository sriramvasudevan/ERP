# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.utils.translation import ugettext as _
from django.core.mail import send_mail,EmailMessage,SMTPConnection
from django.contrib.sessions.models import Session
from erp.dashboard import forms
from erp.dashboard.models import teamdetails
from erp.misc.util import *
from erp.settings import *
import sha,random,datetime

# Create your views here.
def home (request):
    redirected=session_get(request,"from_url")
    access_denied = session_get (request, "access_denied")
    logged_in = session_get (request, "logged_in")
    already_logged = session_get (request, "already_logged")
    return render_to_response('dashboard/home.html', locals(), context_instance= global_context(request)) 


def documents (request):
    details=teamdetails.objects.all()#still to be filtered according to dept
    memberform=forms.add_team_member()
    return render_to_response('dashboard/documents.html',locals() ,context_instance = global_context(request))

def addteammember(request):
    memberform=forms.add_team_member()
    message="Hello"
    details=teamdetails.objects.all()#still to be filtered according to dept
    print details
    if request.method=='POST':
        print "here"
        data=request.POST.copy()
        form=forms.add_team_member(data)
        if form.is_valid():
            addmember=teamdetails(
            name=models.User.objects.get(username=form.cleaned_data['name']) ,
            email_id=form.cleaned_data['email_id'],
            mobile_number=form.cleaned_data['mobile_number'],
            department=Department.objects.get(Dept_Name=request.session['department']),
            )
        try:
            addmember.save()
            message="team member added"
            print "peace"

        except:
            #message="team member could not be added"
            print "problem"
            pass

    else:
        message="team member could not be added"
    return render_to_response('dashboard/documents.html',locals() ,context_instance = global_context(request))


def deleteteammember(request):
    memberform=forms.add_team_member()
    message = "could not delete the team member "
    details=teamdetails.objects.all()
    if "d" in request.GET:
        number=request.GET['d']
        delete=teamdetails.objects.filter(id=number)
        print delete

        delete.delete();
        details=teamdetails.objects.all()
        message = "Team member deleted "
        print number
        print "yahoo"
        print delete



    return render_to_response('dashboard/documents.html',locals() ,context_instance = global_context(request))

"""
def editteammember(request):
    memberform=forms.add_team_member()
    message = "could not delete the team member "
    details=teamdetails.objects.all()
    button="Save"
        if "e" in request.GET:
            number=request.GET['e']
            edit=teamdetails.objects.filter(id=number)
    return render_to_response('dashboard/documents.html',locals() ,context_instance = global_context(request))
            
                
"""    
      

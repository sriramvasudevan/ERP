# Create your views here.
from django.http import *
from django.shortcuts import *
from django.template import *
from erp.misc.helper import is_core, is_coord, get_page_owner
from feedback.forms import *
from erp.users.models import *
from django.http import Http404
from erp.feedback.models import *
from django.db.models import Q
from django.core.urlresolvers import reverse


def answer(request):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    if is_core(curr_user):
        is_core1=True
        is_visitor1=False
        if str(curr_userprofile.department) == "QMS":
            qms_core=True    
        curr_department=curr_userprofile.department
        coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords')
        questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Coord').exclude(answered_by='Vol')
        answers=Answer.objects.filter(creator=curr_userprofile)
    if is_coord(curr_user):
        curr_department=curr_userprofile.department
        coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords').exclude(user=request.user)
        questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Core').exclude(answered_by='Vol')
        answers=Answer.objects.filter(creator=curr_userprofile)           
    return render_to_response('feedback/feedback.html',locals(),context_instance=RequestContext(request))

def display(request):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    if is_core(curr_user):
        if str(curr_userprofile.department) == "QMS":
            is_core1=True
            is_visitor1=False
            qms_core=True
            questions=Question.objects.all()
        else:
            raise Http404
    else:
        raise Http404            
    return render_to_response('feedback/display.html',locals(),context_instance=RequestContext(request))

def add_question(request):
    if is_core(request.user):
        curr_userprofile=userprofile.objects.get(user=request.user)
        owner_name=None
        page_owner = get_page_owner (request, owner_name)
        if str(curr_userprofile.department) == "QMS":
            is_core1=True
            is_visitor1=False
            qms_core=True
            if request.method == 'POST':
                questionform=QuestionForm(request.POST)
                question_added=False
                if questionform.is_valid():
                    questionform.save()
                    question_added= True
                else:
                    error=True
            questionform=QuestionForm()
            return render_to_response('feedback/question.html',locals(),context_instance=RequestContext(request))
        else:
            raise Http404
    else:
        raise Http404   

def display_questions(request,coord_id):
	curr_user=request.user
	curr_userprofile=userprofile.objects.get(user=request.user)
	owner_name=None
	page_owner = get_page_owner (request, owner_name)
	curr_department=curr_userprofile.department
	curr_coord_userprofile=userprofile.objects.get(id=coord_id)
	if is_core(curr_user):
		if str(curr_userprofile.department) == "QMS":
			is_core1=True
			is_visitor1=False
			qms_core=True
		questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Coord').exclude(answered_by='Vol')
		answers=Answer.objects.filter(creator=curr_userprofile)
		
	
	if is_coord(curr_user):
		questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Core').exclude(answered_by='Vol')
		answers=Answer.objects.filter(creator=curr_userprofile)

	return render_to_response('feedback/display_questions.html',locals(),context_instance=RequestContext(request))

def answer_questions(request,coord_id,question_id):
	curr_user=request.user
	curr_userprofile=userprofile.objects.get(user=request.user)
	owner_name=None
	is_core1=False
	qms_core=False
	page_owner = get_page_owner (request, owner_name)
	curr_department=curr_userprofile.department
	answers=Answer.objects.filter(creator=curr_userprofile)
	question1=Question.objects.filter(id=question_id)
	if question1:
		question2=Question.objects.get(id=question_id)
	curr_coord_userprofile=userprofile.objects.get(id=coord_id)
	if is_core(curr_user):
		if str(curr_userprofile.department) == "QMS":
			is_core1=True
			is_visitor1=False
			qms_core=True
		questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Coord').exclude(answered_by='Vol')
		if request.method == 'POST':
			answer=Answer.objects.filter(question = question2).filter(creator=curr_userprofile).filter(owner=curr_coord_userprofile)
			if answer:
				for answer1 in answer:
					answerform=AnswerForm(request.POST, instance=answer1)
					if answerform.is_valid():
						answerform.save()
			else:
				answerform=AnswerForm(request.POST)
				if answerform.is_valid():
					answer1=Answer(rating=request.POST['rating'],question=question2,owner=curr_coord_userprofile,creator=curr_userprofile,answered=True)
					answer1.save()

	
	if is_coord(curr_user):
		questions=Question.objects.filter(departments=curr_department).exclude(answered_by='Core').exclude(answered_by='Vol')
		if request.method=='POST':
			answer=Answer.objects.filter(question=question2).filter(creator=curr_userprofile).filter(owner=curr_coord_userprofile)
			if answer:
				for answer1 in answer:
					answerform=AnswerForm(request.POST, instance=answer1)
					if answerform.is_valid():
						answerform.save()
			else:
				answerform=AnswerForm(request.POST)
				if answerform.is_valid():
					answer1=Answer(rating=request.POST['rating'],question=question2,owner=curr_coord_userprofile,creator=curr_userprofile,answered=True)
					answer1.save()
				
	answerform=AnswerForm()
	return render_to_response('feedback/answer_questions.html',locals(),context_instance=RequestContext(request))
"""
def rate(request, coord_name, question_id):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
	
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    curr_department=curr_userprofile.department
    coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords')
    curr_question=Question.objects.get(id=question_id)
    curr_coord_userprofile = userprofile.objects.get (name=coord_name)
#   curr_answer=Answer.objects.get(Q(question=curr_question),Q(owner=curr_coord_userprofile))
    try:
        curr_answer=Answer.objects.get(Q(question=curr_question),Q(owner=curr_coord_userprofile))
        return HttpResponseRedirect('/erp/feedback/edit/'+str(curr_coord_userprofile.name)+'/'+str(curr_question.id)+'/'+str(curr_answer.id)+'/')
    except Answer.DoesNotExist:    
        if curr_userprofile.department == curr_coord_userprofile.department:
        #Lot of repitition of code, use or statement etc. Just for checking case by case that it is foolproof
            if is_core(request.user):
                is_core1=True
                is_visitor1=False
                if str(curr_userprofile.department) == "QMS":
                    qms_core=True
                if curr_question.answered_by == 'Core':       
                    
                    if request.method == 'POST':
                       answerform=AnswerForm(request.POST)
                       if answerform.is_valid():
                           answer = answerform.save(commit=False)
                           answer.question = curr_question
                           answer.owner = curr_coord_userprofile
                           answer.creator = curr_userprofile
                           answer.answered = True
                           answer.save()
                           return HttpResponseRedirect("/erp/feedback/answer")
                       else:
                           error=True
                    answerform=AnswerForm()
                    return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))
    
        
            if is_core(request.user):
                is_core1=True
                is_visitor1=False
                if str(curr_userprofile.department) == "QMS":
                    qms_core=True
                if curr_question.answered_by == 'All':       
                    
                    if request.method == 'POST':
                       answerform=AnswerForm(request.POST)
                       if answerform.is_valid():
                           answer = answerform.save(commit=False)
                           answer.question = curr_question
                           answer.owner = curr_coord_userprofile
                           answer.creator = curr_userprofile
                           answer.answered = True
                           answer.save()
                           return HttpResponseRedirect("/erp/feedback/answer")
                       else:
                           error=True
                    answerform=AnswerForm()
                    return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))
    
                    
            if is_coord(request.user):
                if curr_question.answered_by == 'Coord':       
                    
                    if request.method == 'POST':
                       answerform=AnswerForm(request.POST)
                       if answerform.is_valid():
                           answer = answerform.save(commit=False)
                           answer.question = curr_question
                           answer.owner = curr_coord_userprofile
                           answer.creator = curr_userprofile
                           answer.answered = True
                           answer.save()
                           return HttpResponseRedirect("/erp/feedback/answer")
                       else:
                           error=True
                    answerform=AnswerForm()
                    return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))
             
                        
            if is_coord(request.user):
                if curr_question.answered_by == 'All':
                    
                    if request.method == 'POST':
                       answerform=AnswerForm(request.POST)
                       if answerform.is_valid():
                           answer = answerform.save(commit=False)
                           answer.question = curr_question
                           answer.owner = curr_coord_userprofile
                           answer.creator = curr_userprofile
                           answer.answered = True
                           answer.save()
                           return HttpResponseRedirect("/erp/feedback/answer")
                       else:
                           error=True
                    answerform=AnswerForm()
                    return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))        

        else:
            raise Http404
"""

"""
def edit(request, coord_name, question_id, answer_id):
    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)
    users_profile=userprofile.objects.all()
    owner_name=None
    page_owner = get_page_owner (request, owner_name)
    curr_department=curr_userprofile.department
    coord_profiles = userprofile.objects.filter (department= curr_department,user__groups__name = 'Coords')
    curr_question=Question.objects.get(id=question_id)
    curr_coord_userprofile = userprofile.objects.get (name=coord_name)
    curr_answer=Answer.objects.get(id=answer_id)
    if curr_userprofile.department == curr_coord_userprofile.department:
        #Lot of repitition of code, use or statement etc. Just for checking case by case that it is foolproof
        if is_core(request.user):
            is_core1=True
            is_visitor1=False
            if str(curr_userprofile.department) == "QMS":
                qms_core=True
            if curr_question.answered_by == 'Core':       
                
                if request.method == 'POST':
                   answerform=AnswerForm(request.POST, instance=curr_answer)
                   if answerform.is_valid():
                       answerform.save()
                       return HttpResponseRedirect("/erp/feedback/answer")
                   else:
                       error=True
                answerform=AnswerForm(instance=curr_answer)
                return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))
    
        
        if is_core(request.user):
            is_core1=True
            is_visitor1=False
            if str(curr_userprofile.department) == "QMS":
                qms_core=True
            if curr_question.answered_by == 'All':       


                if request.method == 'POST':
                   answerform=AnswerForm(request.POST, instance=curr_answer)
                   if answerform.is_valid():
                       answerform.save()
                       return HttpResponseRedirect("/erp/feedback/answer")
                   else:
                       error=True
                answerform=AnswerForm(instance=curr_answer)
                return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))

                    
        if is_coord(request.user):
            if curr_question.answered_by == 'Coord':       
                 
                if request.method == 'POST':
                   answerform=AnswerForm(request.POST, instance=curr_answer)
                   if answerform.is_valid():
                       answerform.save()
                       return HttpResponseRedirect("/erp/feedback/answer")
                   else:
                       error=True
                answerform=AnswerForm(instance=curr_answer)
                return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))
           
                        
        if is_coord(request.user):
            if curr_question.answered_by == 'All':
                if request.method == 'POST':
                   answerform=AnswerForm(request.POST, instance=curr_answer)
                   if answerform.is_valid():
                       answerform.save()
                       return HttpResponseRedirect("/erp/feedback/answer")
                   else:
                       error=True
                answerform=AnswerForm(instance=curr_answer)
                return render_to_response('feedback/rate.html',locals(),context_instance=RequestContext(request))     

    else:
       raise Http404
       

"""
        
def delete_question(request, question_id):
    if is_core(request.user):
        curr_userprofile=userprofile.objects.get(user=request.user)
        owner_name=None
        page_owner = get_page_owner (request, owner_name)
        if str(curr_userprofile.department) == "QMS":
            q = Question.objects.get(id=question_id)
            answers = q.answer_set.all()
            for ans in answers:
                ans.delete()
            q.delete()    
            return HttpResponseRedirect("/erp/feedback/display")
        else:
            raise Http404
    else:
        raise Http404

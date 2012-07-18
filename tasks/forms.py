from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
from chosen import forms as chosenforms
from chosen import widgets as chosenwidgets

class TaskCommentForm (ModelForm):
    class Meta:
        model = TaskComment
        exclude = ('author', 'task')
        

class SubTaskCommentForm (ModelForm):
    class Meta:
        model = SubTaskComment
        exclude = ('author', 'subtask')                

class UpdateForm (ModelForm):
    class Meta:
        model = Update
        exclude = ('author')

class TaskForm (ModelForm):
    class Meta:
        model = Task
        exclude = ('creator', )
        

class SubTaskForm (ModelForm):
    class Meta:
        model = SubTask
        exclude = ['creator', 'description', 'department', 'task']

#hack if these fields need to be formatted        
#    def __init__(self, *args, **kwargs):
#        super(SubTaskForm, self).__init__(*args, **kwargs)
#        self.fields['subject'].widget.attrs['rows'] = '500'
#        self.fields['subject'].widget.attrs['cols'] = '500'
        

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from erp.department.models import *

# Create your models here.

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
)
#List of Department Choices

#DEP_CHOICES    = (
#	("Events", "Events"),
#	("QMS", "Quality Management"),
#	("Finance", "Finance"),
#	("Sponsorship", "Sponsorship"),
#	("Evolve", "Evolve"),
#	("Facilities", "Facilities"),
#	("Webops", "Web Operations"),
#	("Hospitality", "Hospitality"),
#	("Publicity", "Publicity"),
#	("Design", "Design"),
#)

#This is the initial users model
#Author-Krishna Shrinivas

class userprofile(models.Model):
    user = models.ForeignKey(User, unique=True)
    nickname=models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    emailid     =models.EmailField()
    last_name = models.CharField(max_length=30)
    department= models.ForeignKey(Department,related_name="dept_user_belong")
    chennai_number = models.CharField(max_length=15)
    summer_number = models.CharField(max_length=15)
    summerstay  =models.CharField(max_length=30)
    #We are changing to groups right? so, i removed the flags.
 
    #i Havent written the methods as yet, do we use them as methods in a class or in views?
    class Meta:
	
        permissions=(
            ("is_core",("Can give Task to coords")),
            ("is_coord",("Can give tasks to vols")),
            ("is_vol",("Can view the page")),
            )
    def __str__(self):

        return self.user.username

    class Admin:
        pass

#author : vivek kumar bagaria

class Materials(models.Model):
    user		=models.ForeignKey(User, unique=True, related_name="item_borrower")#name of the  person who asked or gave
    item		=models.CharField(max_length=50)# the material which has been asked for
    item_no		=models.IntegerField(default=1)#no. of items borrowed
    borrowed_time   =models.DateTimeField(null=True ,blank=True)#time of borrow
    return_time 	=models.DateTimeField(null=True ,blank=True)#time of return
    item_got	=models.BooleanField(default=False)#if the person got/given the item this will be true
    item_returned	=models.BooleanField(default=False)#if the person returns/takes the item this will be true
    user_2		=models.ForeignKey(User , unique=True, related_name="item_lender")#name of the person/hostel/deptartment borrowed/lent from
    
    def __str__(self):
	       
        return self.item


    class Admin:
        pass


class invitation(models.Model):
    core            =models.ForeignKey(User , related_name="the core who has invited the user")
    invitee         =models.CharField(max_length=50)
    emailid         =models.EmailField()
    time            =models.DateField()

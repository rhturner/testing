from __future__ import unicode_literals
from django.contrib import messages
from datetime import date,datetime

from django.db import models

import re
import bcrypt

DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')
emailcheck=re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
namecheck=re.compile(r'^[A-za-z ]{3}[A-za-z ]*')
passwordcheck=re.compile(r'\w{8,}')
itemcheck=re.compile(r'\w{3,}')

class UserManager(models.Manager):
    def login(self, request):
        print "Running login code"
        password=request.POST['password'].encode()
        try:
            user_object=User.objects.get(email=request.POST['email'])
            if bcrypt.hashpw(password.encode(),user_object.pwh.encode())==user_object.pwh:
                request.session['id']=user_object.id
                request.session['name']=user_object.f_name
                request.session['logged_in']=True
                return True
        except:
            messages.error(request, "The credentials supplied were not correct.")
            return False

    def validate(self, request):

        password_hash=''

        status=True
        print "Checking Password"
        if request.POST['password'] == request.POST['confirm_password']:
            if not passwordcheck.match(request.POST['password']):
                messages.error(request, "Your password must be at least 8 characters long.")
                status=False
        else:
            messages.error(request, "Your passwords did not match")
            status=False
        print "Checking First Name Length"
        if not namecheck.match(request.POST['f_name']):
            messages.error(request, "Your first name must be 2 characters or longer")
            status=False
        print "Checking Last Name Length"
        if not namecheck.match(request.POST['l_name']):
            messages.error(request, "Your last name must be 2 characters or longer")
            status=False
        print "Checking for email validity"
        if not emailcheck.match(request.POST['email']):
            messages.error(request, "Your email does not appear to be valid")
            status=False
        print "Checking for email uniqueness"
        try:
            User.objects.get(email=request.POST['email'])
            messages.error(request, "Your email is not unique")
            status=False
        except:
            print "Email is valid"
        print "Checking the bd submitted"
        try:
            datetime.strptime(request.POST['bd'], '%d-%m-%Y')
        except:
            messages.error(request, "You did not submit your birthday in the correct format")
            status=False
        print "Done with checks...  Returning..."
        if not status:
            return (status, request, password_hash)

        password = request.POST['password']
        password = password.encode()
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

        return (status, request, password_hash)

    def validate_id(self,request, id):
        try:
            user=User.objects.get(id=id)
            return True
        except:
            messages.error(request, "The user ID you presented does not exist in our system")
            return False

class AppointmentManager(models.Manager):
    def validate(self, request):
        try:
            status=True
            if not request.POST['task']:
                status=False
                messages.error(request, "Your task cannot be blank")
            if not request.POST['date']:
                statyus=False
                messages.error(request, "Your date cannot be blank")
            if not request.POST['time']:
                status=False
                messages.error(request, "Your time cannot be blank")
            submitted_date=request.POST['date']
            submitted_time=request.POST['time']
            combined=submitted_date+' ' +submitted_time
            combined=datetime.strptime(combined, '%Y-%m-%d %H:%M')
            now=datetime.now()
            if now>combined:
                status=False
                messages.error(request, "You cannot have an appointment in the past")

            return status
                    #  = now.replace(hour=8, minute=0, second=0, microsecond=0)
        except:
            messages.error(request, "We were unable to process your request")
            return False
            
    def validate_edit (self, request, id):
        try:
            Appointment.objects.get(user__id=request.session['id'], id=id)
            return True
        except:
            messages.error(request, "You are not authorized for this edit")
            return False

class User(models.Model):
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    bd = models.CharField(max_length=10)
    pwh = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Appointment(models.Model):
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    date = models.DateField()
    time = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=AppointmentManager()

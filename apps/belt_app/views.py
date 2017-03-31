from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date
from .models import User, Appointment


def index(request):
    if request.session.get('logged_in'):
        return redirect('/dashboard')
    return render(request, 'belt_app/index.html')

def process_registration(request):
    status, request, password_hash = User.objects.validate(request)
    print "Status: ", status
    if status:
        print "*"*50
        print "First Name: ", request.POST['f_name']
        print "Last Name: ", request.POST['l_name']
        print "Email: ", request.POST['email']
        print "Hash: ", password_hash
        print "birthday", request.POST['bd']
        print "*"*50
        User.objects.create(f_name=request.POST['f_name'], l_name=request.POST['l_name'], email=request.POST['email'], bd=request.POST['bd'], pwh=password_hash)
        User.objects.login(request)
        messages.success(request, "You have successfully registered and have been logged into the system")
        return redirect('/dashboard')
    else:
        return redirect('/')


def dashboard(request):
    if request.session.get('logged_in'):
        user_object=User.objects.get(id=request.session['id'])
        context = {
            'everything' : Appointment.objects.filter(user__id=request.session['id']).exclude(date=date.today()).order_by('-date'),
            'today' : Appointment.objects.filter(user__id=request.session['id'], date=date.today()),
            'date' : date.today(),
        }
        print "Hello"
        print context
        return render(request, 'belt_app/dashboard.html', context)
    if request.POST:
        if User.objects.login(request):
            return redirect('/dashboard')
    else:
        return redirect('/')

def create(request):
    if not request.session.get('logged_in'):
        return redirect('/')
    if request.POST:
        if Appointment.objects.validate(request):
            user_object=User.objects.get(id=request.session['id'])
            result=Appointment.objects.create(task=request.POST['task'], time=request.POST['time'], date=request.POST['date'], status='Pending', user=user_object)
            messages.success(request, "Appointment Added")
    return redirect('/dashboard')

def delete(request, id):
    if not request.session.get('logged_in'):
        return redirect('/')
    if Appointment.objects.validate_edit(request, id):
        del_object=Appointment.objects.get(id=id)
        del_object.delete()
    return redirect('/dashboard')

def edit(request, id):
    if not request.session.get('logged_in'):
        return redirect('/')
    if Appointment.objects.validate_edit(request, id):
        context = {
        'appointment' : Appointment.objects.get(id=id)
        }
    return render(request, 'belt_app/edit.html', context)

def update(request, id):
    if not request.session.get('logged_in'):
        return redirect('/')
    if Appointment.objects.validate_edit(request, id):
        if Appointment.objects.validate(request):
            update_object=Appointment.objects.get(id=id)
            update_object.task=request.POST['task']
            update_object.date=request.POST['date']
            update_object.time=request.POST['time']
            update_object.status=request.POST['status']
            update_object.save()
            messages.success(request, "Appointment updated")
    return redirect('/dashboard')

def logout(request):
    if not request.session.get('logged_in'):
        return redirect('/')
    del request.session['logged_in']

    return redirect('/')

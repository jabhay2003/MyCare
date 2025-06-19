from datetime import date, datetime
from email.message import EmailMessage
import random
from sqlite3 import DataError
from telnetlib import LOGOUT
from django.conf import settings
from django.views.generic import ListView
from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.views.generic.base import TemplateView
from django.contrib import messages
from .models import Appointment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import context
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User



def Homepage(request):
     return render(request,'index.html')

def patientHomepage(request):
     return render(request,'patienthome.html')     

def hospitaltHomepage(request):
     return render(request,'hospitalhome.html')  

def Sign_up_page(request):

    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration.html', { 'form': form})   
    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully login.')
            login(request, user)
            return redirect('login')
        else:
            return render(request, 'registration.html', {'form': form})

def Loginpage(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                
                return render(request,'patienthome.html')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'login.html',{'form': form})  
    
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')    

def aboutpage(request):
    return render(request,'about.html')

def blogpage(request):
    return render(request,'blog.html')

def contactpage(request):
    return render(request,'contact.html')

def departmentpage(request):
    return render(request,'department.html')

def hospitalpage(request):
    return render(request,'hospital.html')

def elementspage(request):
    return render(request,'elements.html')

def upload_document(request):
    if request.method == 'POST' and request.FILES['document']:
        document = request.FILES['document']
        fs = FileSystemStorage()
        filename = fs.save(document.name, document)
        document_url = fs.url(filename)
        return render(request, 'show_document.html', {'document_url': document_url})
    return render(request, 'upload_document.html')

 
class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request, *args, **kwargs):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        sent_date=request.POST.get("sent_date")
        branch=request.POST.get("branch")
        message = request.POST.get("request")
        
        
        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            sent_date=sent_date,
            branch=branch,
            request=message
        )

        appointment.save()
        sent_date = datetime.strptime(sent_date, "%Y-%m-%dT%H:%M")
        if (sent_date < datetime.now()):
            messages.success(request, 'Please select a date and time in the future.')
            return render(request, 'appointment.html')
            
            
        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making and appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)


class ManageAppointmentTemplateView(LoginRequiredMixin, ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    paginate_by = 3

    '''
    def post(self, request, *args, **kwargs):
        sent_date = request.POST.get("sent_date")
        appointment_id= request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date= datetime.now()
        appointment.save()

        data = {
            "fname": appointment.first_name,
            "sent_date": sent_date,
        }

        message = render_to_string('email.html', data)
        
        send_mail(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            ['websitemycare@gmail.com'],
            html_message=message,
        )

        messages.add_message(request, messages.SUCCESS, f"{date}")
        return HttpResponseRedirect(request.path)
        '''
    
    def post(self, request, *args, **kwargs):
        sent_date = request.POST.get("sent_date")
        appointment_id= request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date= datetime.now()
        appointment.rejected = False
        appointment.save()

        data = {
            "fname": appointment.first_name,
            "sent_date": appointment.sent_date,
        }

        message = render_to_string('email.html', data)
        
        send_mail(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            ['websitemycare@gmail.com'],
            html_message=message,
        )

        messages.add_message(request, messages.SUCCESS, f"Successfully Accept Appointment")
        return HttpResponseRedirect(request.path)
        


    def get_context_data(self, *args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        appointments=Appointment.objects.all()
        context.update({
            "appointments":appointments,
        })
        return context
    
from django.http import HttpResponseRedirect
from django.urls import reverse

class HospitalTemplateView(TemplateView):
    template_name = "hospitalsignup.html"    

    def post(self, request, *args, **kwargs):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        # Remove the 'password' field from here

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email, 
            # Remove the 'password' field from here
        )

        appointment.save()

        # Redirect to a success page or any other appropriate page
        return HttpResponseRedirect(reverse('success_page'))

def success_page(request):
    return render(request, 'hospital.html')

def Hospitalsigninpage(request):
     return render(request,'hospitalsignin.html')


# ----------------------------------- USER REGISTRATION -----------------------------------------
def user_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('registerFirstName')
        last_name = request.POST.get('registerLastName')
        email = request.POST.get('registerEmail')
        username = request.POST.get('registerUsername')
        password = request.POST.get('registerPassword')
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return render(request, 'hospitalsignup.html', {'error_message': 'Username is already taken'})

        # Create the user
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return redirect('hospitallogin')  # Redirect to the login page after successful registration

    return render(request, 'hospitalsignup.html')


# ------------------------------ USER LOGIN --------------------------------------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('loginUsername')
        password = request.POST.get('loginPassword')
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                # Redirect superuser to admin panel
                return redirect('/admin/')
            return redirect('manage-appointment')  # Redirect to the home page after successful login
        else:
            print("user is noat auth")
    return render(request, 'hospitallogin.html', )



def email_page(request):
    if request.method == "POST":
       user_email=request.POST.get('email')
       if User.objects.filter(email=user_email):
            print("Email Already Exists")
            context={
                'email_exist':'Email already exists'
            }
            return render(request,'email_verification.html',context)
       else:
            send_otp(request, user_email)
            request.session['email']= user_email
            return redirect('verification')
    return render(request,'email_verification.html')

def send_otp(request, email):
    otp = random.randint(1000,9999)
    request.session['otp'] = otp
    msg= f"Your one time password is {otp}"
    send_mail(
        'OTP',
        msg,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )

def verification(request):
    if request.method=="POST":
        user_otp=request.POST.get('otp')
        otp=request.session.get('otp')
        if otp == int(user_otp):
            return redirect('signup')
        else:
            context={
                'invalid_otp:Invalid otp'
            }
            messages.add_message(request, messages.SUCCESS, f"Wrong OTP")
            #return render(request,'verification.html',context)
    return render(request,'verification.html')
    
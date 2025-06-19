from django.contrib import admin
from django.urls import path
from Home import views
from .views import HospitalTemplateView, Sign_up_page, Loginpage, AppointmentTemplateView, ManageAppointmentTemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.Sign_up_page, name='signup'),
    path('login/', views.Loginpage, name='login'),
    path('logout/', views.handelLogout, name="handelLogout"),
    path('', views.Homepage, name='home'),
    path('patienthome/', views.patientHomepage, name='patienthome'),
    path('about/', views.aboutpage, name='about'),
    path('contact/', views.contactpage, name='contact'),
    path('department/', views.departmentpage, name='department'),
    path('hospital/', views.hospitalpage, name='hospital'),
    path('elements/', views.elementspage, name='elements'),
    path('blog/', views.blogpage, name='blog'),
    path('appointment/', AppointmentTemplateView.as_view(), name='appointment'),
    #path('hospitalsignup/', HospitalTemplateView.as_view(), name='hospitalsignup'),
    path('hospitalhome/', views.hospitaltHomepage, name='hospitalhome'),
    #path('hospitalsignin/', views.Hospitalsigninpage, name='hospitalsignin'),
    path('success/', views.success_page, name='success_page'),
    path('manage-appointment/', views.ManageAppointmentTemplateView.as_view(), name='manage-appointment'),
    path('upload/', views.upload_document, name='upload_document'),
    path('hospitallogin/', views.user_login, name='hospitallogin'),
    path('hospitalsignup/', views.user_register, name='hospitalsignup'),
    path('authentication/',views.email_page, name="email_page"),
    path('email-verify/',views.verification,name='verification'),
]

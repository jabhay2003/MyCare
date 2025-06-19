from datetime import datetime
from django.db import models
from django.utils.translation import gettext as _

branch = [
    ('naroda', 'NARODA'),
    ('satellite', 'SATELLITE'),
    ('ranip', 'RANIP'),
    ('maninagar', 'MANINAGAR'),
]

# Create your models here.
class Appointment(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    email= models.CharField(max_length=50)
    phone= models.CharField(max_length=50)
    request= models.TextField(blank=True)
    sent_date = models.DateTimeField()
    branch = models.CharField(max_length=50, choices=branch, default='naroda')
    accepted = models.BooleanField(default=False)
    accepted_date =models.DateTimeField(_("Date"), default=datetime.today)
    rejected=models.BooleanField(default=False)
    rejected_date =models.DateTimeField(_("Date"), default=datetime.today) 


    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ["sent_date"]

class Hospital(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    email= models.CharField(max_length=50) 
    #password= models.CharField(max_length=50)       

    def __str__(self):
        return self.first_name
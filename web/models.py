from django.db import models  
from django.conf import settings  
from django.contrib.auth.models import User  
from django.utils import timezone 
import django_jalali.db.models as jmodels
from django import forms
from django_recaptcha.fields import ReCaptchaField
import uuid

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()

class Passwordresetcodes(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length=120)
    time = models.DateTimeField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='custom_auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}_token".format(self.user)
        
class Expense(models.Model):  
    text = models.CharField(max_length=255)  
    date = models.DateTimeField()  
    amount = models.BigIntegerField()  
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  

    def __str__(self):  
        return "{} - {}".format(self.date, self.amount)
class Income(models.Model):  
    text = models.CharField(max_length=255)  
    date = models.DateTimeField()
    amount = models.BigIntegerField()  
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  

    def __str__(self):  
        return "{} - {}".format(self.date, self.amount)  

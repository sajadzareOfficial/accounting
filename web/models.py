from django.db import models  
from django.contrib.auth.models import User  
from django.utils import timezone  

class Token(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=48)

    def __str__(self):  
        return "{}_token".format(self.User)  


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
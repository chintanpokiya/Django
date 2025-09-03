# Create your models here.
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

    
class Becholer(models.Model):
    oid=models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True) 
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    mail=models.EmailField()
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    theme_name = models.CharField(max_length=100)
    addr=models.CharField(max_length=50)
    sugg=models.CharField(max_length=50)  
    status = models.CharField(max_length=50, default='Pending')  # Pending, Completed
    invoice_sent = models.BooleanField(default=False)
    booked_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'{self.fname}'


class Wedding(models.Model):
    oid=models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    gname=models.CharField(max_length=20)
    bname=models.CharField(max_length=20)
    mail=models.EmailField()
    mobile_number = models.CharField(max_length=15)
    date = models.DateField(default="DD-MM-YYYY")
    time = models.TimeField()
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    venue=models.CharField(max_length=30)
    sugg=models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Pending')  # Pending, Completed
    invoice_sent = models.BooleanField(default=False)  
    booked_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'{self.fname}'
    
    
class Reception(models.Model):
    oid=models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    gname=models.CharField(max_length=20)
    bname=models.CharField(max_length=20)
    mail=models.EmailField()
    mobile_number = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    venue=models.CharField(max_length=30)
    sugg=models.CharField(max_length=50) 
    status = models.CharField(max_length=50, default='Pending')  # Pending, Completed
    invoice_sent = models.BooleanField(default=False)   
    booked_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'{self.fname}'    
    
    

    
    
    
    
    
    
    
    
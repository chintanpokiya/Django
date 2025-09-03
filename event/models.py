from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Contact(models.Model):
    MARK_AS = ((True, 'Open'), (False, 'Closed'))
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField()
    contact_number = models.CharField(max_length=25)
    message = models.TextField()
    email_sent = models.BooleanField(default=False)  # New field to track email status

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="profile",null=True)
    mobile = models.CharField(max_length=200, null=True)
    alternate = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Create your models here.
class userModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

class UserVerification(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.description


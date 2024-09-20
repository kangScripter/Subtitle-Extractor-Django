from django.db import models
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import AbstractUser
# Create your models here.

User = get_user_model()
class Video(models.Model):
    Fkey = models.ForeignKey(User,on_delete=models.CASCADE)
    video_filename = models.CharField(max_length=100)
    
class Substitle(models.Model):
    Fkey = models.ForeignKey(Video,on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    lang = models.CharField(max_length=100)
    subtitles_file = models.FileField(upload_to='subtitles')
    video_file_name = models.CharField(max_length=100)


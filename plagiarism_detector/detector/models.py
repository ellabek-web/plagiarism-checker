from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FileRepository(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='uploads/')
 

 

class FileRepositoryI(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    college = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    degree_level = models.CharField(max_length=255)
    catagory = models.CharField(max_length=255)
    file_name = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name.name





class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
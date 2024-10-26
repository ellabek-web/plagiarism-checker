from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    comment = models.TextField()

    def save(self, *args, **kwargs):
        if self.user is None:
            self.user = self.request.user
        super().save(*args, **kwargs)
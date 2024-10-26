from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FileRepositoryI, Notification
from django.contrib.auth.models import User


@receiver(post_save, sender=FileRepositoryI)
def notify_coordinators(sender, instance, created, **kwargs):
    if created:
        coordinators = User.objects.filter(is_staff=True)
        for coordinator in coordinators:
            Notification.objects.create(
                recipient=coordinator,
                message=f"A new file has been uploaded by {instance.user.username}."
            )
from django.contrib import admin
from .models import FileRepository, FileRepositoryI, Notification

# Register your models here.


class FileRepositoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file')

admin.site.register(FileRepository, FileRepositoryAdmin)


@admin.register(FileRepositoryI)
class FileRepositoryIAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'user', 'status', 'uploaded_at')
    search_fields = ('file_name', 'user__username', 'status')
    list_filter = ('status',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'created_at', 'read')
    search_fields = ('recipient__username', 'message')
    list_filter = ('read',)
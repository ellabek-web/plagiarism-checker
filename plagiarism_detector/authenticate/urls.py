from django.contrib import admin
from django.urls import path,include
from .views import index, logout_view,profile_view,confirm_registration
from .views import feedback_view
from django.contrib.auth import views as auth_views
import detector 


urlpatterns = [
    #path('admin/', admin.site.urls),
    path("accounts/",include("django.contrib.auth.urls")),
    path("", index, name="index"),
    # path("accounts/register/", registration_view, name="register"),

    path('accounts/profile/', profile_view, name='profile'),
      #  path('profile/', profile, name='profile')
     
    path('logout/', logout_view, name='logout'),
    path('confirm-registration/<int:user_id>/', confirm_registration, name='confirm_registration'),


 
    # path('register/', register_user, name='register_user'),
    # Other URL patterns...
    path('feedback/', feedback_view, name='feedback'),


    path('Check_page/', detector.views.upload_file_for_plagiarism_check, name='upload_file'),
    # path('', views.home, name='home'),
    path('user/',  detector.views.user, name='Home'),
    path('Upload/',  detector.views.upload_file, name='upload'),
    path('coordinator/',  detector.views.coordinator, name='Home'),
    path('about/',  detector.views.about, name='about'),
    #path('contact/',  detector.views.contact, name='contact'),
    path('plagiarism/<int:pk>/',  detector.views.plagiarism_result, name='plagiarism_result'),
    
    path('download_file/<str:file_id>/',  detector.views.download_file, name='download_file'),
    path('check_plagiarism/<str:file_id>/',  detector.views.plagiarism_check, name='check_plagiarism'),
    
    
    path('notification_view/',  detector.views.notification_view_read, name='Notification'),

    path('mark_as_read/<int:notification_id>/', detector.views.mark_as_read, name='mark_as_read'),

    path('open/<int:file_id>/', detector.views.open_file, name='open_file'),

    path('contact/',  feedback_view, name='contact'),

    path('file_repo/',  detector.views.file_repo, name='File Reository'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]
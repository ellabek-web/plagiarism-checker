from audioop import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from detector.views import coordinator,user
from django.contrib import messages


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# def registration_view(request):
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("index")
#     else:
#         form = RegistrationForm()

#     return render(request, "registration/register.html", {"form": form})


def index(request):
    return render(request, "registration/login.html")
    # if request.user.is_authenticated:
    #     return redirect(profile_view)
    # else:
    #     return redirect(logout_view)
    # return render(request, "index.html")


def profile_view(request):
    # Fetch the user's profile data

    if request.user.is_staff:
        if request.user.is_superuser:
          return redirect('admin:index')
        # User is a staff member
        # return render(request, 'registration/second.html')
        return redirect(coordinator)
    
    else:
        # User is not a staff member
        return redirect(user)
        # return render(request, 'registration/profile.html')
    
    
    
def logout_view(request):
    logout(request)
    return render(request, "registration/login.html")
    # return redirect('login')  # Replace 'login' with the name of your login page URL
def confirm_registration(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Perform any necessary logic to confirm the registration
    # For example, you can update a field on the user object to mark it as confirmed
    user.is_active = True
    user.save()
    # Render a template to display a confirmation message to the user
    return render(request, 'registration/confirmation.html')

# views.py


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'feedback.html', {'form': form, 'success_message': 'Thank you for your feedback!'})
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
           
            success_message ="thank you for your feedback"
            form = FeedbackForm()
            return render(request, 'feedback.html', {'form': form, 'success_message': success_message})
            # return redirect('contact')
    else:
        form = FeedbackForm()

    # success_message ="thank you for your feedback"
    # messages.get_messages(request)
    return render(request, 'feedback.html',{'form': form,})
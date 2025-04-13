from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator as generate_token
from django.core.mail import EmailMessage, BadHeaderError, get_connection
from django.conf import settings
from django.views import View
import smtplib
import ssl
from socket import error as socket_error

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pass1")
        confirm_password = request.POST.get("pass2")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("/auth/signup/")

        if User.objects.filter(username=email).exists():
            messages.info(request, "Email is already registered")
            return redirect("/auth/signup/")

        try:
            user = User.objects.create_user(
                username=email, email=email, password=password
            )
            user.is_active = False
            user.save()
        except IntegrityError:
            messages.error(request, "Account creation failed. Please try again.")
            return redirect("/auth/signup/")

        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return redirect("/auth/signup/")

    return render(request, "signup.html")



def handlelogin(request):
    return render(request, "login.html")


def handlelogout(request):
    return redirect("/auth/login/")

from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import random
import re
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from .models import Password

br = Browser()
br.set_handle_robots(False)
fernet = Fernet(settings.KEY)


def home(request):
    if request.method == "POST":
        if "signup-form" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            #if password are not identical
            if password != password2:
                msg = "Please make sure you're using the same password!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            #if username exists
            elif User.objects.filter(username=username).exists():
                msg = f"{username} already exists!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            #if email exists
            elif User.objects.filter(email=email).exists():
                msg = f"{email} already exists!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                User.objects.create_user(username, email, password)
                new_user = authenticate(request, username=username, password=password2)
                if new_user is not None:
                    login(request, new_user)
                    msg = f"{username}. Thanks for subscribing."
                    messages.success(request, msg)
                    return HttpResponseRedirect(request.path)
        elif "logout" in request.POST:
            msg = f"{request.user}. You logged out."
            logout(request)
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)

        elif 'login-form' in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            new_login = authenticate(request, username=username, password=password)
            if new_login is None:
                msg = f"Login failed! Make sure you're using the right account."
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                login(request, User.objects.get(username=new_login))
                msg = f"{request.user} welcome again."
                messages.success(request, msg)
                return HttpResponseRedirect(request.path)
        
        elif "add-password" in request.POST:
            url = request.POST.get("url")
            email = request.POST.get("email")
            password = request.POST.get("password")
            #ecrypt data
            encrypted_email = fernet.encrypt(email.encode())
            encrypted_password = fernet.encrypt(password.encode())
            #get title of the website
            try:
                br.open(url)
                title = br.title()
            except:
                title = url
            #get the logo's URL
            try:
                icon = favicon.get(url)[0].url
            except:
                icon = "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"
            #Save data in database
            new_password = Password.objects.create(
                user=request.user,
                name=title,
                logo=icon,
                email=encrypted_email.decode(),
                password=encrypted_password.decode(),
            )
            s = request.POST.get("password")
            l, u, p, d = 0, 0, 0, 0

            if (len(s) >= 8):
                for i in s:
 
            # counting lowercase alphabets
                    if (i.islower()):
                        l+=1           
 
            # counting uppercase alphabets
                    if (i.isupper()):
                        u+=1           
 
            # counting digits
                    if (i.isdigit()):
                        d+=1           
 
            # counting the mentioned special characters
                    if(i=='@'or i=='$' or i=='_' or i=='!' or i=='#' or i=='%' or i==''):
                        p+=1          
            if (l>=1 and u>=1 and p>=1 and d>=1):
                msg = f"{title} added successfully. Password Is Strong"
                messages.success(request, msg)
            else:
                msg = f"{title} added successfully. Password Is weak"
                messages.success(request, msg)
            
            

        elif "delete" in request.POST:
            to_delete = request.POST.get("password-id")
            msg = f"{Password.objects.get(id=to_delete).name} deleted."
            Password.objects.get(id=to_delete).delete()
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
        
        elif "generator" in request.POST:
            passw = request.POST.get("txt")
            editpass = passw.replace("a", "@").replace("k", "l<").replace("o","()").replace("w","vv").replace("W","VV").replace("Q","Ó").replace("U","l_l").replace("u","i_i").replace("b","!ↄ").replace("B","!ↄ").replace("c","ↄ").replace("C","ↄ")
            temp = editpass[0:2]
            sumnum = 0
            for i in range(0,2):
                temp2 = ord(temp[i])
                sumnum = temp2 + sumnum
            editpass = editpass + str(sumnum)
            msg = f"{editpass} is the new password"
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)

            
    context = {}
    if request.user.is_authenticated:
        passwords = Password.objects.all().filter(user=request.user)
        for password in passwords:
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(password.password.encode()).decode()
        context = {
            "passwords":passwords,
        }   



    return render(request, "home.html", context)

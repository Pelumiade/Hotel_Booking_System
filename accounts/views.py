from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse 
from .forms import CustomerCreationForm
from accounts.models import CustomUser




# @user_passes_test(lambda u: u.is_superuser)
# @login_required(login_url='/login/')

# def admin_dashboard(request):
#     return render(request, 'accounts/admin_dashboard.html')
@login_required(login_url='/login/')
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('login')
    return render(request, 'accounts/admin_dashboard.html')

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('bookings:login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render(request, 'accounts/login.html', {'error_message': error_message})
    else:
        return render(request, 'accounts/login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')



def customer_signup(request):
   form = CustomerCreationForm()
   page = "customer_signup"
   if request.method == 'POST':
      form = CustomerCreationForm(request.POST)
      if form.is_valid():
         my_user = form.save(commit=False)
         my_user.is_active = True
         my_user.save()
         my_user = CustomUser.active_objects.get(email=request.POST.get("email"))
         login(request, my_user)
         return HttpResponseRedirect(reverse(""))
   context = {
      "form": form,
      "page": page
   }

   return render(request, "accounts/customer_login.html", context)

def customer_login(request):
   email = request.POST.get("email")
   password = request.POST.get("password")
   page = "customer_login"

   if request.method == "POST":
      try:
         user = CustomUser.active_objects.get(email=email)

      except:
         messages.error(request, "Email does not exist, you should sign up or try checking your e-mail")
         return render(request, "accounts/customer_login.html", {"page": page})

      user = authenticate(email=email, password=password)

      if user is not None:
         login(request, user)

         return HttpResponseRedirect(reverse("garbage:home_page"))
      messages.error(request, "Invalid login details")
      return render(request, "accounts/customer_login.html", {"page": page})
   
   elif request.method == "GET":
      return render(request, "accounts/customer_login.html", {"page": page})



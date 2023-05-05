from django.shortcuts import render

# Create your views here.


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

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
            return render(request, 'admin_module/login.html', {'error_message': error_message})
    else:
        return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

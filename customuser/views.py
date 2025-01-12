from django.shortcuts import render, redirect

from customuser.forms import UserRegistrationForm


def get_main_page(request):
    return render(request,'main_page.html')

def register(request):
    if request.method == 'POST':
        form =  UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def auth_login(request):
    return render(request, 'login.html')

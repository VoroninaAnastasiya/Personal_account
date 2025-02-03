import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from customuser.forms import UserRegistrationForm, LoginForm, ProfileForm
from customuser.models import ProfileUser, UserImage


def get_main_page(request):
    return render(request,'main_page.html')

def register(request):
    if request.method == 'POST':
        form =  UserRegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            profile = ProfileUser(user=user)
            profile.save()
            photo = UserImage(image='no_photo/no_photo.jpg', is_main=True, user_profile=profile)
            photo.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(form)
            email = form.cleaned_data.get('username')
            print(email)
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('main_page') # Пользователь найден, выполняем вход
        else:
            form = AuthenticationForm()
            return render(request, 'login.html', {'form': form}) # Пользователь не найден
    return render(request, 'login.html', {'form': form})


def profile_user(request):
    user = request.user
    print(user) # только для идентифицированного пользователя
    profile = ProfileUser.objects.get(user=user)
    # print(profile)
    image = UserImage.objects.filter(user_profile=profile)
    form = ProfileForm(instance=profile)
    context = {
        'profile': profile,
        'image': image,
        'form': form
    }
    if request.method == 'POST':
        if 'delete_image' in request.POST:
            print(request.POST)
            image_id = request.POST.get('image_id')
            print(image_id)
            delete_image = image.get(id=image_id)
            path = delete_image.image
            delete_image.delete()# удаляем ссылку на файл
            os.remove(f'./{path}')# удаляем файл

        if 'delete_main_image' in request.POST:
            main_image = image.get(is_main=True)
            if main_image.image != 'no_photo.jpg':
                path = main_image.image
                os.remove(f'./{path}')
                main_image.image = 'no_photo.jpg'
                main_image.save()

        if 'make_main_image' in request.POST:
            main_image = image.get(is_main=True)
            image_id = request.POST.get('image_id')
            make_new_image = image.get(id=image_id)
            make_new_image.is_main = True
            make_new_image.save()
            print(main_image.image)
            if main_image.image == 'no_photo/no_photo.jpg':
                print('Работает++++++')
                main_image.delete()
            else:
                main_image.is_main = False
                main_image.save()

        else:
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                print(form)
                return redirect('main_page')
            else:
                form = ProfileForm(instance=profile)
                context.update({"form": form})
                return render(request, 'profile.html', context)

        print(context)
    return render(request, 'profile.html', context)

def user_logout(request):
    logout(request)
    return  redirect('main_page')
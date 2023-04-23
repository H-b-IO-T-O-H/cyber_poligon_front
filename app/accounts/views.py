from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.forms import LoginForm, RegistrationForm, SettingsForm

User = get_user_model()


def registration_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/registration.html',
                      {'form': RegistrationForm})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES or None)
        if not form.is_valid():
            return render(request, 'accounts/registration.html', {'form': form})
        avatar = form.cleaned_data['avatar']
        password = form.cleaned_data['password']
        username = form.cleaned_data['username']
        user = User.objects.create_user(email=form.cleaned_data['email'],
                                        password=password,
                                        username=username,
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        avatar=avatar,
                                        )
        if user is not None:
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('articles:Cat In Hat')
        else:
            return render(request, 'accounts/registration.html',
                          {'form': form, 'error': 'Server error'})
    else:
        return HttpResponse(status=405)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('articles:Cat In Hat')
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
                      {'form': LoginForm})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is None:
                return render(request, 'accounts/login.html',
                              {'error': 'Wrong login or/and password', 'form': form})
            login(request, user)
            prev_link = request.META['HTTP_REFERER'].replace(request.get_full_path(), '')
            print(request.META['HTTP_REFERER'])
            return redirect(prev_link)
        return render(request, 'accounts/login.html',
                      {'error': 'Full out the forms correctly', 'form': form})
    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('accounts:login')


def settings_view(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'accounts/settings.html', {'form': form})
        user = request.user
        check_user = authenticate(request, username=user.username, password=form.cleaned_data['password'])
        if check_user is None:
            return render(request, 'accounts/settings.html', {'form': form, 'error': 'Wrong password'})
        User.objects.update_user(user, form)
        return redirect('accounts:settings')

    form = SettingsForm()
    if request.user.is_authenticated:
        return render(request, 'accounts/settings.html', {'form': form})
    return redirect('articles:Cat In Hat')

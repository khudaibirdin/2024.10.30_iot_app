from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def page_auth(request):
    """
    Авторизация пользователя, POST-запрос при вводе логина и пароля и нажатии на кнопку.
    """
    if request.POST:
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            dj_login(request, user)
            return redirect('/')
    return render(request, 'users/page_auth.html')

def logout(request):
    if request.POST:
        dj_logout(request)
    return render(request, 'users/page_auth.html')

@login_required(login_url='/page_auth/')
def page_account(request):
    """
    Страница авторизации
    """
    return render(request, 'users/page_account.html')

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль сменен успешно')
            return redirect('/account')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/page_password_change.html', {'form': form})
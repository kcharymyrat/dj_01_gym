from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.conf import settings
from django.contrib.auth.decorators import login_required


from .forms import LoginForm, RegisterForm


User = get_user_model()

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        User.objects.create_user(username=username, email=email, password=password)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    context = {"form": form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            form = LoginForm()
    context = { 'form': form }
    return render(request, "accounts/login.html", context)


@login_required
def logout_view(request):
    # if not request.user.is_authenticated:
    #     return redirect('%s?next=%s' % ('/',settings.LOGIN_URL))
    logout(request)
    return redirect('login')
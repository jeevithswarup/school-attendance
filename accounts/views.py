from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from .forms import LoginForm, UserCreateForm, UserUpdateForm
from .models import User


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'accounts/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
        return render(request, 'accounts/profile.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserListView(View):
    def get(self, request):
        if not request.user.is_admin():
            return redirect('dashboard')
        users = User.objects.all().order_by('role', 'username')
        return render(request, 'accounts/user_list.html', {'users': users})


@method_decorator(login_required, name='dispatch')
class UserCreateView(View):
    def get(self, request):
        if not request.user.is_admin():
            return redirect('dashboard')
        return render(request, 'accounts/user_form.html', {'form': UserCreateForm()})

    def post(self, request):
        if not request.user.is_admin():
            return redirect('dashboard')
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('user_list')
        return render(request, 'accounts/user_form.html', {'form': form})

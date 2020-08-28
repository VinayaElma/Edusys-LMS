
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from accounts.forms import RegistrationForm, EditProfileForm

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

@login_required(login_url='login')
def home_screen(request):
	context={}
	return render(request, 'home.html',{})

def profilePage(request):
	context={}
	return render(request, 'accounts/profilePage.html',{})

class RegisterPage(View):
	def post(self, request):
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('home')
		context = {'form':form}
		return render(request, 'accounts/register.html', context)	
	def get(self, request):
		form = RegistrationForm()	
		context = {'form':form}
		return render(request, 'accounts/register.html', context)

def loginPage(request):
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')
		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('profile')
	else:
		form = EditProfileForm(instance=request.user)
	context= {'form':form}
	return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url='login')
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Your password was successfully updated!')
			return redirect('home')
	else:
		form = PasswordChangeForm(user=request.user)
		context= {'form':form}
		return render(request, 'accounts/change_password.html', context)
	
			
	


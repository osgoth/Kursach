from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
cursor = connection.cursor()


def index(request):
	print( request.user )
	context = {'res': request}
	return render(request, 'index.html', context)

def contacts(request):
	return render(request, 'contacts.html')


def portfolio(request):
	return render(request, 'portfolio.html')

def logout_view(request):
    logout(request)
    return redirect('main_page')


def services(request, category, types):
	if types:
		cards = Services.objects.filter(types=types.replace('_',' '))
	elif category and types == None:
		cards = Services.objects.filter(category=category)
	else:
		cards = Services.objects.all()
		
	context = {'cards': cards}
	return render(request, 'services.html', context)

def service_detail(request, service_id):
	cards = Services.objects.filter(id=service_id)
	context = {'cards': cards}
	return render(request, 'service_detail.html', context)




def basket(request):
	return render(request, 'basket.html')

def confirm(request):
	return render(request, 'confirm.html')

def conditions(request):
	return render(request, 'conditions.html')


def sign_in(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect(index)
	else:
		form = AuthenticationForm()

	return render(request, 'customer/sign_in.html', {'form':form})

def sign_up(request):
	print(request.method)
	if request.method == 'POST':
		request.POST._mutable = True
		email = request.POST['email']
		del request.POST['email']

		print(request.POST)
		form = UserCreationForm(request.POST)
		print(form.is_valid())


		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect(index)
	else:
		form = UserCreationForm()

	return render(request, 'customer/sign_up.html', {'form':form})



def profile(request):
	return render(request, 'customer/profile.html')




def profile_settings(request):
	data = Customers.objects.filter(email=email)
	if request.method == 'POST':
		form = ProfileChanges(data=request.POST)
		if form.is_valid():
			user = form.save()
			return redirect(profile_settings)
	return render(request, 'customer/profile_settings.html')





def profile_orders(request):
	return render(request, 'customer/profile_orders.html')

def employee_profile(request):
	email = request.user.email
	EmployeeInfo = Employee.objects.filter(email=email)
	print(EmployeeInfo)
	return render(request, 'employee/employee_profile.html')

def employee_requests(request):
	return render(request, 'employee/employee_requests.html')

def employee_projects(request):
	return render(request, 'employee/employee_projects.html')

def employee_sign_in(request):
	return render(request, 'employee/employee_sign_in.html')
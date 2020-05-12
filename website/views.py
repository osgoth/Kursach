from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Group

from datetime import datetime

cursor = connection.cursor()


def index(request):
    context = {"res": request}
    return render(request, "index.html", context)


def contacts(request):
    return render(request, "contacts.html")


def portfolio(request):
    return render(request, "portfolio.html")


def logout_view(request):
    logout(request)
    return redirect("main_page")


def services(request, category=None, types=None):
    if types:
        cards = Services.objects.filter(types=types.replace("_", " "))
    elif category and types is None:
        cards = Services.objects.filter(category=category)
    else:
        cards = Services.objects.all()

    context = {"cards": cards}
    return render(request, "services.html", context)


def service_detail(request, service_id=None):
    cards = Services.objects.filter(id=service_id)
    context = {"cards": cards, 'res': request}
    return render(request, "service_detail.html", context)


def basket(request):
    return render(request, "basket.html")


def confirm(request, service_id=None):
    service = Services.objects.get(id=service_id)
    customer = Customers.objects.get(username=request.user.username)

    deal = Deals.objects.create(
        status ='processing'
        )

    requestt = Requests.objects.create(
        deal = deal,
        customer = customer,
        service = service,
        reg_date = datetime.now()
        )

    
    return render(request, "confirm.html")


def conditions(request):
    return render(request, "conditions.html")


@csrf_protect
def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()            
            login(request, user)
            return redirect(index)
    else:
        form = AuthenticationForm()

    return render(request, "customer/sign_in.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        request.POST._mutable = True
        email = request.POST["email"]
        username = request.POST["username"]
        new_user = Customers.objects.create(
            username=username, email=email, reg_date=datetime.now()
        )
        del request.POST["email"]
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            Group.objects.get(name='Users').user_set.add(user)
            login(request, user)
            return redirect(index)
    else:
        form = UserCreationForm()

    return render(request, "customer/sign_up.html", {"form": form})


def profile(request):
    username = request.user.username
    user = Customers.objects.get(username=username)
    context = {"user": user}
    return render(request, "customer/profile.html", context)


@csrf_protect
def profile_settings(request):
    username = request.user.username
    user = Customers.objects.get(username=username)
    if request.method == "GET":
        day = user.birthday.strftime("%d")
        year = user.birthday.strftime("%Y")
        month = user.birthday.strftime("%m")
        check_year = datetime.now().strftime("%Y")
        check_month = datetime.now().strftime("%m")

        return render(
            request,
            "customer/profile_settings.html",
            context={"user": user, "day": day, "month": month, "year": year},
        )
    if request.method == "POST":
        user.update(request.POST)
        return redirect(profile_settings)


def profile_orders(request):
    return render(request, "customer/profile_orders.html")



def admin_settings_dep(request):
    return render(request, "admin/admin_settings_dep.html")

def admin_settings_empl(request):
    cards = Employee.objects.all()
    context = {"cards": cards}
    return render(request, "admin/admin_settings_empl.html", context)

@csrf_protect
def admin_new_empl(request):
    if request.method == "POST":
        department = Departments.objects.get(name=request.POST['department'])
        new_employee = Employee.objects.create(
            username = request.POST['username'],
            department = department,
            name =  request.POST['name'],
            surname = request.POST['surname'],
            email = request.POST['email'] ,
            birthday = date(int(request.POST["year"]), int(request.POST["month"]), int(request.POST["day"])),
            gender = request.POST['gender'],
            phone = request.POST['phone'],
            position = request.POST['position'],
            reg_date = datetime.now()
        )

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if request.POST['position'] == 'manager':
                Group.objects.get(name='Managers').user_set.add(user)
            else:
                Group.objects.get(name='Employees').user_set.add(user)
            
            return redirect(admin_settings_empl)

    if request.method == "GET":
        departments = Departments.objects.all()
        return render(request, "admin/admin_new_empl.html", {'departments': departments})

    return render(request, "admin/admin_new_empl.html")


def employee_profile(request):   
    EmployeeInfo = Employee.objects.get(username=request.user.username)
    context = {'empl':EmployeeInfo, 'request':request}
    return render(request, "employee/employee_profile.html", context)


def employee_requests(request):
    return render(request, "employee/employee_requests.html")


def employee_projects(request):
    return render(request, "employee/employee_projects.html")


def employee_sign_in(request):
    return render(request, "employee/employee_sign_in.html")




def requests_active(request):
    cursor.execute("""
        SELECT c.email, s.id, r.id as request_id, d.status, d.price, d.final_date, d.description, d.id as deal_id FROM "Deals" AS d
        JOIN "Requests" AS r ON r.deal_id = d.id
        JOIN "Customers" AS c ON r.customer_id = c.id
        JOIN "Services" AS s ON r.service_id = s.id;""")

    context = dictfetchall(cursor)
    context = {'context': context}
    return render(request, "employee/manager/requests_active.html", context)

def requests_done(request):
    return render(request, "employee/manager/requests_done.html")

def requests_settings(request, deal_id=None):
    if request.method == "POST":
        deal = Deals.objects.get(id=deal_id)
        deal.update(request.POST)
        return redirect(requests_active)

    else:
        cursor.execute(f"""
            SELECT c.email, s.id, s.name, r.id as request_id, d.status, d.price, d.final_date, d.description, d.id as deal_id FROM "Deals" AS d
            JOIN "Requests" AS r ON r.deal_id = d.id
            JOIN "Customers" AS c ON r.customer_id = c.id
            JOIN "Services" AS s ON r.service_id = s.id where d.id = {deal_id};""")
        context = dictfetchall(cursor)

        cursor.execute(f"""
            select distinct e.name, e.surname, e.username from "Employee" as e 
                join "Departments" as d  on e.department_id = d.id 
                join "Services" as s on s.department_id = d.id where s.id = {deal_id};""")
        employees = dictfetchall(cursor)

        context = {'context': context[0], 'empl': employees}    
        return render(request, "employee/manager/requests_settings.html", context)


# need for 'requests_active()' spirt
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
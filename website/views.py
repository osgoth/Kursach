from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.db import connection
from datetime import datetime
from .models import *
from .forms import *

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


def conditions(request):
    return render(request, "conditions.html")

# Получения списка всех услуг агенства
def services(request, category=None, types=None):
    if types:
        cards = Services.objects.filter(types=types.replace("_", " "))
    elif category and types is None:
        cards = Services.objects.filter(category=category)
    else:
        cards = Services.objects.all()

    context = {"cards": cards}
    return render(request, "services.html", context)

# Получение деталей про услугу, таких как название и другие
def service_detail(request, service_id=None):
    cards = Services.objects.filter(id=service_id)
    context = {"cards": cards, 'res': request}
    return render(request, "service_detail.html", context)

# Создание заявки клиентом
# Далее должна быть обработана менеджером
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


@csrf_protect
def sign_in(request):
    if request.method == "POST":
        # Данные получаемые из запроса отправляются
        # в предуставноленный метод AuthenticationForm
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # После того, как форма одобренна
            # происходит авторизация
            user = form.get_user()            
            login(request, user)
            if "Employees" or "Managers" in request.user.groups.all()[0]:
                return redirect("/foremployee")
            return redirect(index)
    else:
        form = AuthenticationForm()

    return render(request, "customer/sign_in.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        # Получаемые данные заполняются в таблицу Customers
        request.POST._mutable = True
        email = request.POST["email"]
        username = request.POST["username"]
        new_user = Customers.objects.create(
            username=username, email=email, reg_date=datetime.now()
        )
        del request.POST["email"]
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # После проверки формы пользователь
            # получает группы Users
            user = form.save()
            Group.objects.get(name='Users').user_set.add(user)
            login(request, user)
            return redirect(index)
    else:
        form = UserCreationForm()

    return render(request, "customer/sign_up.html", {"form": form})

# Получение информации про профиль клиента
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
        # необходимые ограничения для формы
        day = user.birthday.strftime("%d")
        year = user.birthday.strftime("%Y")
        month = user.birthday.strftime("%m")
        check_year = datetime.now().strftime("%Y")
        check_month = datetime.now().strftime("%m")
        context = {"user": user, "day": day, "month": month, "year": year}

        return render(request, "customer/profile_settings.html", context=context)

    if request.method == "POST":
        print(request.POST['date'])
        # Пользователь обновляет свои данные
        user.update(request.POST)
        return redirect(profile_settings)


def profile_orders(request):
    customer = Customers.objects.get(username=request.user.username)
    # Запрос на получение необходимой информации про заказы пользователя
    # Такие как услугу, номер заявки и дополнительная информация о сделке
    cursor.execute(f"""
        SELECT s.name, s.id as service_id, r.id as request_id, d.status, d.price, d.final_date
        FROM "Requests" AS r
        JOIN "Deals" AS d ON r.deal_id = d.id
        JOIN "Services" AS s ON r.service_id = s.id 
        where r.customer_id = {customer.id};""")

    context = dictfetchall(cursor)
    print(context)
    context = {'context': context}
    return render(request, "customer/profile_orders.html", context)


def admin_settings_empl(request):
    cards = Employee.objects.all()
    context = {"cards": cards}
    return render(request, "admin/admin_settings_empl.html", context)


@csrf_protect
def admin_new_empl(request):
    # Создание нового сотрудника через меню администратора
    if request.method == "POST":
        department = Departments.objects.get(name=request.POST['department'])
        datearr = request.POST['date'].split('/')
        new_employee = Employee.objects.create(
            username = request.POST['username'],
            department = department,
            name =  request.POST['name'],
            surname = request.POST['surname'],
            email = request.POST['email'] ,
            birthday = date(int(datearr[2]), int(datearr[0]), int(datearr[1])),
            gender = request.POST['gender'],
            phone = request.POST['phone'],
            position = request.POST['position'],
            reg_date = datetime.now()
        )

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # если должность сотрудника является менеджером
            # То он попадает в группу менеджеров
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


# Доступно только менеджерам
def requests_active(request):
    # просмотр всех активных заявок отдела
    empl = Employee.objects.get(username=request.user.username)
    cursor.execute(f"""
        SELECT c.email, s.id, r.id as request_id, d.status, d.price, d.final_date, d.description, d.id as deal_id FROM "Deals" AS d
        JOIN "Requests" AS r ON r.deal_id = d.id
        JOIN "Customers" AS c ON r.customer_id = c.id
        JOIN "Services" AS s ON r.service_id = s.id where not d.status = 'done' and s.department_id = {empl.department_id};""")

    context = dictfetchall(cursor)
    context = {'context': context}
    return render(request, "employee/manager/requests_active.html", context)


def requests_done(request):
     # просмотр всех выполенных заявок отдела
    empl = Employee.objects.get(username=request.user.username)
    cursor.execute(f"""
        SELECT c.email, s.id, r.id as request_id, d.status, d.price, d.final_date, d.description, d.id as deal_id FROM "Deals" AS d
        JOIN "Requests" AS r ON r.deal_id = d.id
        JOIN "Customers" AS c ON r.customer_id = c.id
        JOIN "Services" AS s ON r.service_id = s.id where  d.status = 'done' and s.department_id = {empl.department_id};;""")

    context = dictfetchall(cursor)
    context = {'context': context}
    return render(request, "employee/manager/requests_done.html", context)

# Доступно сотрудникам и менеджерам
def projects_active(request):
    # просмотр всех активных задач для определнного сотрудника
    empl = Employee.objects.get(username=request.user.username)
    cursor.execute(f"""
        SELECT c.email, s.id, r.id as request_id, d.status, d.price, d.final_date, d.description, d.id as deal_id FROM "Deals" AS d
        JOIN "Requests" AS r ON r.deal_id = d.id
        JOIN "Customers" AS c ON r.customer_id = c.id
        JOIN "Services" AS s ON r.service_id = s.id where not d.status = 'done' and d.employee_id = {empl.id};""")

    context = dictfetchall(cursor)
    context = {'context': context}
    return render(request, "employee/projects_active.html", context)


def projects_done(request):
    # просмотр всех выполненных задач для определнного сотрудника
    empl = Employee.objects.get(username=request.user.username)
    cursor.execute(f"""
        SELECT c.email, s.id, r.id as request_id, d.status, d.price, d.final_date, d.description, d.id as deal_id FROM "Deals" AS d
        JOIN "Requests" AS r ON r.deal_id = d.id
        JOIN "Customers" AS c ON r.customer_id = c.id
        JOIN "Services" AS s ON r.service_id = s.id where d.status = 'done' and d.employee_id = {empl.id};""")

    context = dictfetchall(cursor)
    context = {'context': context}
    return render(request, "employee/projects_done.html", context)


# Меню только менеджеру
def requests_settings(request, deal_id=None):
    # изменения касательно заявки пользователя
    # Данные вносятся после уточнения информации
    # о заказе у клиента
    if request.method == "POST":
        deal = Deals.objects.get(id=deal_id)        
        employee = Employee.objects.get(username=request.POST['employee'])
        deal.update(request.POST)
        deal.employee_id = employee.id
        deal.save()
        return redirect(requests_active)

    else:
        # Получение всех заявок для отдела
        cursor.execute(f"""
            SELECT c.email, s.id, s.name, s.department_id, r.id as request_id, d.status, d.price, d.final_date, d.description, d.id as deal_id FROM "Deals" AS d
            JOIN "Requests" AS r ON r.deal_id = d.id
            JOIN "Customers" AS c ON r.customer_id = c.id
            JOIN "Services" AS s ON r.service_id = s.id where d.id = {deal_id};""")
        context = dictfetchall(cursor)

        # Список сотрудников отдела
        cursor.execute(f"""
            select e.username from "Employee" as e
            join "Departments" as d on e.department_id = d.id 
            where d.id = {context[0]['department_id']};""")
        employees = dictfetchall(cursor)

        deal = Deals.objects.get(id=deal_id)
        if deal.employee_id:
            emp_active = Employee.objects.get(id=deal.employee_id)
        else:
            emp_active = {'username':''}
        context = {'context': context[0], 'empl': employees, 'emp_active': emp_active}    
        return render(request, "employee/manager/requests_settings.html", context)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
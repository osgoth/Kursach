from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Departments)
admin.site.register(Customers)
admin.site.register(Employee)
admin.site.register(Services)
admin.site.register(Requests)
admin.site.register(Deals)
admin.site.register(Chart)
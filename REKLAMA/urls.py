from django.contrib import admin
from django.urls import path
from website import views
from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_settings_empl/', views.admin_settings_empl),
    path('admin_new_empl/', views.admin_new_empl),
    path('admin_settings_dep/', views.admin_settings_dep),
    path('', views.index, name='main_page'),    
    path('contacts/', views.contacts, name='contacts'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('confirm/<int:service_id>', views.confirm, name='confirm'),
    path('conditions/', views.conditions, name='conditions'),    
    path('basket/', views.basket, name='basket'), 
    path('logout/', views.logout_view, name='basket'),   

    path('services/<int:service_id>/', views.service_detail, name='service_detail'), 
    re_path(r'^services(?:/(?P<category>\w+))?(?:/(?P<types>\w+))?/$', views.services, name='services'),

    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('profile/', views.profile, name='profile'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/orders/', views.profile_orders, name='profile_orders'),

    path('foremployee/sign_in/', views.employee_sign_in, name='employee_sign_in_'),
    path('foremployee/', views.employee_profile, name='employee_profile'),
    path('foremployee/projects/', views.employee_projects, name='employee_projects'),
    path('foremployee/requests/', views.employee_requests, name='employee_requests'),

    path('requests/active/', views.requests_active),
    path('requests/done/', views.requests_done),
    path('requests/settings/<int:deal_id>/', views.requests_settings, name='requests_settings'), 
]

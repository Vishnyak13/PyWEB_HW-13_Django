from django.urls import path
from . import views

app_name = 'financeapp'

urlpatterns = [
    path('', views.main, name='main'),

]
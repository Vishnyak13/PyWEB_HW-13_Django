from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_income/', views.add_income, name='add_income'),
    path('delete_expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('delete_income/<int:id>/', views.delete_income, name='delete_income'),
    path('edit_expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('edit_income/<int:id>/', views.edit_income, name='edit_income'),
    path('add_category/', views.add_category, name='add_category'),
    path('report/', views.get_report, name='report'),
    path('categories', views.get_all_categories, name='categories'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    ]
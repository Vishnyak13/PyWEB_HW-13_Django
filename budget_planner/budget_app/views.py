from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.timezone import now

from .models import Category, Expense, Income


# Create your views here.
def index(request):
    context = {
        'expenses': Expense.objects.all(),
        'incomes': Income.objects.all(),
    }
    return render(request, 'budget_app/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST,
    }
    if request.method == 'GET':
        return render(request, 'budget_app/add_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'budget_app/add_expense.html', context)

        description = request.POST['description']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'budget_app/add_expense.html', context)

        date_expense = request.POST['date']
        if not date_expense:
            date_expense = now()

        category = request.POST['category']
        Expense.objects.create(amount=amount, description=description, date=date_expense,
                               category=Category.objects.filter(name=category).first())
        messages.success(request, 'Expense saved successfully')
        return redirect('index')


def add_income(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST,
    }
    if request.method == 'GET':
        return render(request, 'budget_app/add_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'budget_app/add_income.html', context)

        description = request.POST['description']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'budget_app/add_income.html', context)

        category = request.POST['category']
        Income.objects.create(amount=amount, description=description,
                              date=request.POST['date'] if request.POST['date'] else now(),
                              category=Category.objects.filter(name=category).first())
        messages.success(request, 'Expense saved successfully')
        return redirect('index')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed successfully')
    return redirect('index')


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income removed successfully')
    return redirect('index')


def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
    }
    if request.method == 'GET':
        return render(request, 'budget_app/edit_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'budget_app/edit_expense.html', context)

        description = request.POST['description']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'budget_app/edit_expense.html', context)

        date_expense = request.POST['date']
        if not date_expense:
            date_expense = now()

        category = request.POST['category']
        expense.amount = amount
        expense.description = description
        expense.date = date_expense
        expense.category = Category.objects.filter(name=category).first()
        expense.save()
        messages.success(request, 'Expense updated successfully')
        return redirect('index')


def edit_income(request, id):
    income = Income.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'income': income,
        'values': income,
        'categories': categories,
    }
    if request.method == 'GET':
        return render(request, 'budget_app/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'budget_app/edit_income.html', context)

        description = request.POST['description']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'budget_app/edit_income.html', context)

        category = request.POST['category']
        income.amount = amount
        income.description = description
        income.date = request.POST['date'] if request.POST['date'] else now()
        income.category = Category.objects.filter(name=category).first()
        income.save()
        messages.success(request, 'Income updated successfully')
        return redirect('index')


def add_category(request):
    if request.method == 'GET':
        return render(request, 'budget_app/add_category.html')
    if request.method == 'POST':
        name = request.POST['name']
        if not name:
            messages.error(request, 'Name category is required')
            return render(request, 'budget_app/add_category.html')
        Category.objects.create(name=name)
        messages.success(request, 'Category saved successfully')
        return redirect('index')
    return render(request, 'budget_app/add_category.html')


def get_report(request):
    if request.method == 'POST':
        date_started = request.POST['start_date']
        date_ended = request.POST['end_date']
        try:
            date_started = datetime.strptime(date_started, '%Y-%m-%d')
            date_ended = datetime.strptime(date_ended, '%Y-%m-%d')
        except ValueError:
            date_started = datetime.strptime(str(now().date()), '%Y-%m-%d')
            date_ended = datetime.strptime(str(now().date()), '%Y-%m-%d')
        expenses = Expense.objects.filter(date__gte=date_started, date__lte=date_ended)
        incomes = Income.objects.filter(date__gte=date_started, date__lte=date_ended)
        sum_expenses = sum([expense.amount for expense in expenses])
        sum_incomes = sum([income.amount for income in incomes])
        balance = sum_incomes - sum_expenses
        context = {
            'date_started': date_started,
            'date_ended': date_ended,
            'sum_expenses': sum_expenses,
            'sum_incomes': sum_incomes,
            'balance': balance,
        }
        return render(request, 'budget_app/report.html', context)
    else:
        return render(request, 'budget_app/report.html')


def get_all_categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'budget_app/categories.html', context)


def delete_category(request, id):
    category = Category.objects.get(pk=id)
    category.delete()
    messages.success(request, 'Category removed successfully')
    return redirect('categories')

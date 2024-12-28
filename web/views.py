import requests  
from django.conf import settings  
from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages  
from django.contrib.auth.models import User
# from .models import Passwordresetcodes, Income, Expense, Token
from .models import RegistrationForm, Income, Expense, PasswordResetCode, Token
from django.db import IntegrityError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login  
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.http import HttpRequest  
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import random
from .forms import RegistrationForm, IncomeForm, ExpenseForm
import string
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import uuid


random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))



def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

def get_client_ip(request: HttpRequest) -> str:  
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  
    if x_forwarded_for:  
        ip = x_forwarded_for.split(',')[0]  
    else:  
        ip = request.META.get('REMOTE_ADDR')  
    return ip  


@login_required  
def submit_income(request):  
    """Handles form submission for income."""  
    if request.method == 'POST':  
        try:  
            # بررسی کاربر  
            this_user = request.user  
            
            # دریافت اطلاعات از فرم  
            amount = request.POST.get('amount')  
            text = request.POST.get('text')  
            date_str = request.POST.get('date')  # اگر تاریخ هم به فرم اضافه شده است  
            
            # اعتبارسنجی ورودی‌ها  
            if not amount or not text:  
                return JsonResponse({'status': 'error', 'message': 'Amount and text are required.'}, status=400)  

            # تبدیل مقدار amount به نوع عددی  
            try:  
                amount = float(amount)  # یا int() بسته به نیاز شما  
            except ValueError:  
                return JsonResponse({'status': 'error', 'message': 'Invalid amount format.'}, status=400)  

            # پردازش تاریخ  
            date = timezone.now()  # تاریخ پیش‌فرض  
            if date_str:  
                try:  
                    date = timezone.make_aware(datetime.strptime(date_str, '%Y-%m-%d'))  # فرمت تاریخ باید با آنچه که دریافت می‌کنید، مطابقت داشته باشد  
                except ValueError:  
                    return JsonResponse({'status': 'error', 'message': 'Invalid date format.'}, status=400)  

            # ذخیره درآمد در پایگاه داده  
            Income.objects.create(user=this_user, amount=amount, text=text, date=date)  

            return redirect('/dashboard/')

        except Exception as e:  
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)  
    else:  
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)  

def submit_expense(request):  
    """Handles form submission for expenses."""  
    if request.method == 'POST':  
        try:  
            this_user = request.user  
            
            # دریافت اطلاعات از فرم  
            amount = request.POST.get('amount')  
            text = request.POST.get('text')  # استفاده از `text` به جای `description`  
            date_str = request.POST.get('date')  
            
            # اعتبارسنجی ورودی‌ها  
            if not amount or not text:  
                return JsonResponse({'status': 'error', 'message': 'Amount and description are required.'}, status=400)  

            # تبدیل مقدار amount به نوع عددی  
            try:  
                amount = float(amount)  
            except ValueError:  
                return JsonResponse({'status': 'error', 'message': 'Invalid amount format.'}, status=400)  

            # پردازش تاریخ  
            date = timezone.now()  # تاریخ پیش‌فرض  
            if date_str:  
                try:  
                    date = timezone.make_aware(datetime.strptime(date_str, '%Y-%m-%d'))  
                except ValueError:  
                    return JsonResponse({'status': 'error', 'message': 'Invalid date format.'}, status=400)  

            # ذخیره خرج در پایگاه داده  
            Expense.objects.create(user=this_user, amount=amount, text=text, date=date)  

            return redirect('/dashboard/')

        except Exception as e:  
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)  
    else:  
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
        
# Registration View
# Registration View
def register(request):  
    if request.method == 'POST':  
        form = RegistrationForm(request.POST)  
        if form.is_valid():  
            username = form.cleaned_data['username']  
            email = form.cleaned_data['email']  
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'register.html', {'form': form})

            if User.objects.filter(email=email).exists():  
                messages.error(request, 'This email is already in use.')
                return render(request, 'register.html', {'form': form})

            if User.objects.filter(username=username).exists():  
                messages.error(request, 'This username is already in use.')
                return render(request, 'register.html', {'form': form})

            # Create activation code
            code = uuid.uuid4().hex
            now = timezone.now()

            # Store activation data temporarily
            Passwordresetcodes.objects.create(email=email, time=now, code=code, username=username, password=password)

            activation_link = f"http://localhost:8009/activate/?email={email}&code={code}"

            send_mail(  
                'Account Activation',  
                f'Hello {username}, please click the link to activate your account: {activation_link}',  
                'admin@example.com',  
                [email],  
                fail_silently=False,  
            )  
            messages.success(request, 'A confirmation email has been sent.')
            return redirect('register')
    else:  
        form = RegistrationForm()  

    return render(request, 'register.html', {'form': form})

# Activation View
def activate(request):  
    email = request.GET.get('email')  
    code = request.GET.get('code')  

    try:  
        reset_code = Passwordresetcodes.objects.get(email=email, code=code)

        # Create user and delete reset code
        user = User.objects.create_user(username=reset_code.username, email=email, password=reset_code.password)  
        user.is_active = True 
        user.save()

        reset_code.delete()

        messages.success(request, 'Account activated successfully! Please log in.')
        return redirect('login')
    except Passwordresetcodes.DoesNotExist:  
        messages.error(request, 'Invalid activation code.')
        return redirect('register')

# Login View
def login_view(request):  
    if request.method == "POST":  
        username = request.POST.get("username")  
        password = request.POST.get("password")  
        user = authenticate(request, username=username, password=password)  
        if user is not None:  
            login(request, user)
            return redirect('dashboard')
        else:  
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')  
    return render(request, 'login.html')

# Logout View
def logout_view(request):  
    logout(request)  
    messages.success(request, 'You have been logged out.')
    return redirect('login')


from django.db import models  # Ensure this is added at the top of the file

@login_required(login_url='/login/')
def dashboard_view(request):
    if request.method == 'POST':
        if 'income_submit' in request.POST:
            return handle_income_submission(request)
        elif 'expense_submit' in request.POST:
            return handle_expense_submission(request)

    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    total_income = incomes.aggregate(total=models.Sum('amount'))['total'] or 0
    total_expense = expenses.aggregate(total=models.Sum('amount'))['total'] or 0

    context = {
        'income_form': IncomeForm(),
        'expense_form': ExpenseForm(),
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
    }
    return render(request, 'dashboard.html', context)

@login_required  
def dashboard_expense(request):  
    user_expenses = Expense.objects.filter(user=request.user)  
    total_expenses = sum(expense.amount for expense in user_expenses)  

    return render(request, 'dashboard_expense.html', {  
        'expenses': user_expenses,  
        'total_expenses': total_expenses,  
    })  
@login_required  
def dashboard_income(request):  
    user_income = Income.objects.filter(user=request.user)  
    total_income = sum(income.amount for income in user_income)  

    return render(request, 'dashboard_income.html', {
        'incomes': user_income,  
        'total_income': total_income,  
    })


def handle_income_submission(request):
    income_form = IncomeForm(request.POST)
    if income_form.is_valid():
        income = income_form.save(commit=False)
        income.user = request.user
        income.save()
        messages.success(request, 'Income successfully recorded.')
    else:
        messages.error(request, 'Error in income submission.')
    return redirect('dashboard')


def handle_expense_submission(request):
    expense_form = ExpenseForm(request.POST)
    if expense_form.is_valid():
        expense = expense_form.save(commit=False)
        expense.user = request.user
        expense.save()
        messages.success(request, 'Expense successfully recorded.')
    else:
        messages.error(request, 'Error in expense submission.')
    return redirect('dashboard')

'''
# Dashboard View
@login_required(login_url='/login/')
def dashboard_view(request):
    income_form = IncomeForm()
    expense_form = ExpenseForm()

    if request.method == 'POST':
        if 'income_submit' in request.POST:
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                income = income_form.save(commit=False)
                income.user = request.user
                income.date = timezone.now() 
                if not income_form.cleaned_data['date']:
                    income.date = timezone.now()
                else:
                    income.date = datetime.strptime(income_form.cleaned_data['date'], "%Y-%m-%d")
                income.save()
                messages.success(request, 'Income successfully recorded.')

        elif 'expense_submit' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user
                if not expense_form.cleaned_data['date']:
                    expense.date = timezone.now()
                else:
                    expense.date = datetime.strptime(expense_form.cleaned_data['date'], "%Y-%m-%d")
                expense.save()
                messages.success(request, 'Expense successfully recorded.')

    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)

    context = {
        'income_form': income_form,
        'expense_form': expense_form,
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
    }
    return render(request, 'dashboard.html', context)

'''
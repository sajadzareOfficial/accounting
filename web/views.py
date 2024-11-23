import requests  
from django.conf import settings  
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegistrationForm  
from django.contrib import messages  
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login  
from django.http import JsonResponse
from json import JSONEncoder
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from web.models import User, Expense, Income, Passwordresetcodes
from datetime import datetime
from django.http import HttpRequest  
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import random
from .forms import IncomeForm, ExpenseForm
import string
from django.views.generic import TemplateView  
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required


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

def submit_income(request):
    """ submits an income"""
    if request.method == 'POST':
        try:
            this_token = request.POST.get('token')
            this_user = User.objects.filter(token__token=this_token).first()
            
            if not this_user:
                return JsonResponse({'status': 'error', 'message': 'Invalid token.'}, status=400)

            if 'date' in request.POST:
                date = request.POST['date']
                print (date)
            else:
                date = timezone.now()

            amount = request.POST.get('amount')
            text = request.POST.get('text')
            if not amount or not text:
                return JsonResponse({'status': 'error', 'message': 'Amount and text are required.'}, status=400)

            Income.objects.create(
                user=this_user, amount=amount, text=text, date=date)

            print("I'm in submit expense")
            print(request.POST)

            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
        
def submit_expense(request):
    """ submits an expense"""
    if request.method == 'POST':
        try:
            this_token = request.POST.get('token')
            this_user = User.objects.filter(token__token=this_token).first()
            if not this_user:
                return JsonResponse({'status': 'error', 'message': 'Invalid token.'}, status=400)

            if 'date' in request.POST:
                date = request.POST['date']
            else:
                date = timezone.now()

            amount = request.POST.get('amount')
            text = request.POST.get('text')
            if not amount or not text:
                return JsonResponse({'status': 'error', 'message': 'Amount and text are required.'}, status=400)

            Expense.objects.create(
                user=this_user, amount=amount, text=text, date=date)

            print("I'm in submit expense")
            print(request.POST)

            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def register(request):  
    if request.method == 'POST':  
        form = RegistrationForm(request.POST)  
        if form.is_valid():  
            username = form.cleaned_data['username']  
            email = form.cleaned_data['email']  
            password = form.cleaned_data['password']  

            # چک کردن وجود کاربر با ایمیل یا نام کاربری  
            if User.objects.filter(email=email).exists():  
                return JsonResponse({'status': 'error', 'message': 'متاسفانه این ایمیل قبلا استفاده شده است.'})

            if User.objects.filter(username=username).exists():  
                return JsonResponse({'status': 'error', 'message': 'متاسفانه این نام کاربری قبلا استفاده شده است.'})

            # ایجاد کد و توکن  
            code = random_str(28)  
            now = timezone.now()  
            
            # ذخیره کد فعال‌سازی و نام کاربری و ایمیل، اما کاربران فعلی (User) را هنوز ذخیره نکنید  
            Passwordresetcodes.objects.create(email=email, time=now, code=code, username=username, password=password)  

            activation_link = "http://localhost:8009//activate/?email={}&code={}".format(email, code)  

            send_mail(  
                'فعال سازی اکانت',  
                f'سلام {username}، لطفاً بر روی لینک زیر کلیک کنید تا حساب خود را فعال کنید: {activation_link}',  
                'your-email@example.com',  
                [email],  
                fail_silently=False,  
            )  
            return JsonResponse({'status': 'success', 'message': 'ایمیل تایید برای شما ارسال شد.'})
        else:  
            return JsonResponse({'status': 'error', 'message': 'لطفاً با دقت فرم را پر کنید.'})
    else:  
        form = RegistrationForm()  

    return render(request, 'register.html', {  
        'form': form,  
    })

def activate(request):  
    email = request.GET.get('email')  
    code = request.GET.get('code')  

    try:  
        reset_code = Passwordresetcodes.objects.get(email=email, code=code)  
        
        user = User.objects.create_user(username=reset_code.username, email=email, password=reset_code.password)  
        user.is_active = True 
        user.save()  
        
        token, created = Token.objects.get_or_create(user=user)
        
        reset_code.delete()  

        return redirect('activate')
    except (User.DoesNotExist, Passwordresetcodes.DoesNotExist):  
        messages.error(request, 'این کد فعال‌سازی معتبر نیست. لطفا دوباره تلاش کنید.')  
        return render(request, 'login.html', {'token': None, 'error': 'این کد فعال‌سازی معتبر نیست. لطفا دوباره تلاش کنید.'})
@csrf_protect
def login_view(request):  
    if request.method == "POST":  
        username = request.POST.get("username")  
        password = request.POST.get("password")  
        user = authenticate(request, username=username, password=password)  
        if user is not None:  
            login(request, user) 
            return JsonResponse({"status": "success", "message": "ورود با موفقیت انجام شد."})  
        else:  
            return JsonResponse({"status": "error", "message": "نام کاربری یا رمز عبور صحیح نیست."})  
    return JsonResponse({"status": "error", "message": "روش درخواست نامعتبر است."})  
@login_required
def dashboard_view(request):
    income_form = IncomeForm()
    expense_form = ExpenseForm()

    if request.method == 'POST':
        if 'income_submit' in request.POST:
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                income = income_form.save(commit=False)
                income.user = request.user
                if not income_form.cleaned_data['date']:
                    income.date = timezone.datetime.now()
                income.save()
                messages.success(request, 'درآمد با موفقیت ثبت شد.')
                return redirect('dashboard')
        elif 'expense_submit' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user
                if not expense_form.cleaned_data['date']:
                    expense.date = timezone.datetime.now()
                expense.save()
                messages.success(request, 'هزینه با موفقیت ثبت شد.')
                return redirect('dashboard')

    incomes = Income.objects.filter(user=request.user).order_by('-date')
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

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
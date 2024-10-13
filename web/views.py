from django.shortcuts import render  
from django.http import JsonResponse  
from json import JSONEncoder  
from django.views.decorators.csrf import csrf_exempt  
from web.models import User, Expense, Income
from datetime import datetime  

@csrf_exempt  
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
            else:  
                date = datetime.now()

            amount = request.POST.get('amount')  
            text = request.POST.get('text')  
            if not amount or not text:  
                return JsonResponse({'status': 'error', 'message': 'Amount and text are required.'}, status=400)  

            Income.objects.create(user=this_user, amount=amount, text=text, date=date)  

            print("I'm in submit expense")  
            print(request.POST)  

            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)  

        except Exception as e:  
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)  
    else:  
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt  
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
                date = datetime.now()

            amount = request.POST.get('amount')  
            text = request.POST.get('text')  
            if not amount or not text:  
                return JsonResponse({'status': 'error', 'message': 'Amount and text are required.'}, status=400)  

            Expense.objects.create(user=this_user, amount=amount, text=text, date=date)  

            print("I'm in submit expense")  
            print(request.POST)  

            return JsonResponse({'status': 'ok'}, encoder=JSONEncoder)  

        except Exception as e:  
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)  
    else:  
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
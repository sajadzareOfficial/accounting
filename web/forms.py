from django import forms  
from django.contrib.auth.models import User  
from .models import Income, Expense


class RegistrationForm(forms.ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput)  
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='تأیید رمز عبور')  

    class Meta:  
        model = User  
        fields = ['username', 'email', 'password']  

    def clean(self):  
        cleaned_data = super().clean()  
        password = cleaned_data.get("password")  
        confirm_password = cleaned_data.get("confirm_password")  

        if password and confirm_password and password != confirm_password:  
            raise forms.ValidationError("رمز عبور و تأیید رمز عبور باید یکسان باشند.")
        

class IncomeForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)

    class Meta:
        model = Income
        fields = ['text', 'date', 'time', 'amount']

class ExpenseForm(forms.ModelForm):  
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)  
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)  

    class Meta:  
        model = Expense  
        fields = ['text', 'date', 'time', 'amount']  

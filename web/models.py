from django.db import models
from django.conf import settings
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django.utils.crypto import get_random_string
from django.utils import timezone

# Improved RegistrationForm with ReCaptcha for validation
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()

# Secure PasswordResetCodes model
class PasswordResetCode(models.Model):
    email = models.EmailField(max_length=120)
    code = models.CharField(max_length=64, default=get_random_string(64))  # Secure random string
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)  # Store hashed passwords

    class Meta:
        verbose_name = "Password Reset Code"
        verbose_name_plural = "Password Reset Codes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Password reset for {self.email} (created {self.created_at})"

# Token model for user authentication
class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True, default=get_random_string)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='custom_auth_token',
        on_delete=models.CASCADE  # Deletes token if user is deleted
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}_token"

# Expense model with enhanced structure
class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=15, decimal_places=2)  # Decimal for financial calculations

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.amount}"

# Income model with enhanced structure
class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = "Income"
        verbose_name_plural = "Incomes"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.amount}"
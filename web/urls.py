from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.dashboard_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('submit/expense/', views.submit_expense, name='submit_expense'),
    path('submit/income/', views.submit_income, name='submit_income'),
    path('register/', views.register, name='register'),
    path('activate/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
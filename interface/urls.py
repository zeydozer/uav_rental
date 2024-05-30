from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('login', TemplateView.as_view(template_name='login.html')),
    path('register', TemplateView.as_view(template_name='register.html')),
    path('uav', TemplateView.as_view(template_name='uav.html')),
    path('', TemplateView.as_view(template_name='rental.html')),
]

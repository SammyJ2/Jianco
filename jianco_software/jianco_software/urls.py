"""
URL configuration for jianco_software project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jianco.views import index, results, leakcheck, generate_regular_pdf, generate_premium_pdf
from jianco.views import clear_data, edit_day, months

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', index, name='index'),
    path('results/', results, name='results'),
    path('leakcheck/', leakcheck, name="leakcheck"),
    path('generate_pdf/', generate_regular_pdf, name="generate_regular_pdf"),
    path('generate_premium_pdf/', generate_premium_pdf, name="generate_premium_pdf"),
    path('clear_data/',clear_data, name="clear_data"),
    path('edit_day', edit_day, name="edit_day"),
    path('months', months, name="months"),
    ]
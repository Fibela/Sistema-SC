"""
URL configuration for Monitor project.

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
from django.http import HttpResponse
from django.urls import path
from monitor_ap.views import PredictView, formulario_analisis, realizar_analisis, metricas_tiempo_real

def home(request):
    return HttpResponse("Bienvenido al prototipo monitor")

urlpatterns = [
    path('', formulario_analisis, name='formulario_analisis'),
    path('realizar_analisis/<str:opcion>/', realizar_analisis, name='realizar_analisis'),
    path('metricas/', metricas_tiempo_real, name='metricas_tiempo_real'),
    path('admin/', admin.site.urls),
]

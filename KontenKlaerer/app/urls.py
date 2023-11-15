from django.urls import path
from . import views

urlpatterns = [
    path('', views.pageData, name='pageData'),
]

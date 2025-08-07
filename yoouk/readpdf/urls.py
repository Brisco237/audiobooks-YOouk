from django.urls import path
from .views import selectpdf, audiopdf

urlpatterns = [
    path('selectpdf/', selectpdf, name='selectpdf'),
    path('audiopdf/<slug:slug>', audiopdf, name='audiopdf'),
]
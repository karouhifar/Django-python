from django.urls import path
from . import views

urlpatterns = [
    path('hello/',views.say_hello),
    path('customer/',views.customer),
    path('loadData/',views.loadData),
]

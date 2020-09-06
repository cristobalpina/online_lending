from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('create_borrower', views.create_borrower),
    path('borrower/<int:id>', views.borrower_profile),
    path('create_lender', views.create_lender),
    path('lend', views.lend),
    path('lender/<int:id>', views.lender_profile),
    
]

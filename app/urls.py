from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('create_lender', views.create_lender),
    path('create_borrower', views.create_borrower),
    path('lender/<int:id>', views.lender_profile),
    path('borrower/<int:id>', views.borrower_profile),
    path('lend', views.lend),
]

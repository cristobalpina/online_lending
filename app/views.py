from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from django.contrib import messages
from .models import Lender, Profile, Borrower, Loan

def index(request):
    return redirect('/login')

def register(request):
    return render(request, 'register.html')

def lend(request):
    lender = request.user.profile.lender
    borrower = Borrower.objects.get(id=request.POST['borrower_id'])
    amount = int(request.POST['amount'])
    
    if lender.account_balance - amount < 0:
        messages.error(request, "Insufficient funds")
        return redirect('/lender/{}'.format(request.user.id))
    Loan.objects.create(lender=lender, borrower=borrower, amount=amount)
    return redirect('/lender/{}'.format(request.user.id))

def lender_profile(request, id):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.profile.is_lender:
        user_type = 'lender' if request.user.profile.is_lender else 'borrower'
        return redirect('/{}/{}'.format(user_type, request.user.id))
    context = {
        "borrowers": Borrower.objects.exclude(loans__lender_id=request.user.profile.lender.id)
    }
    return render(request, "lender.html", context)

def borrower_profile(request, id):
    if not request.user.is_authenticated:
        return redirect('/login')
    if not request.user.profile.is_borrower:
        user_type = 'lender' if request.user.profile.is_lender else 'borrower'
        return redirect('/{}/{}'.format(user_type, request.user.id))
    
    return render(request, "borrower.html")

def create_lender(request):
    try:
        user = User.objects.create_user(username=request.POST['email'],
                                    password=request.POST['password'],
                                    first_name=request.POST['first_name'],
                                    last_name=request.POST['last_name'])
    except:
        messages.error(request, 'Email already used')
        return redirect('/register')
    do_login(request, user)
    profile = Profile.objects.create(user=user, is_lender=True)
    lender = Lender.objects.create(profile=profile, money=request.POST['money'])
    return redirect('/lender/{}'.format(user.id))

def create_borrower(request):
    try:
        user = User.objects.create_user(username=request.POST['email'],
                                    password=request.POST['password'],
                                    first_name=request.POST['first_name'],
                                    last_name=request.POST['last_name'])
    except:
        messages.error(request, 'Email already used')
        return redirect('/register')
    do_login(request, user)
    profile = Profile.objects.create(user=user, is_borrower=True)
    borrower = Borrower.objects.create(
        profile=profile,
        need_money_for=request.POST['need_money_for'],
        description=request.POST['description'],
        amount_needed=request.POST['amount_needed']
    )
    return redirect('/borrower/{}'.format(user.id))

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_type = 'lender' if request.user.profile.is_lender else 'borrower'
            return redirect('/{}/{}'.format(user_type, request.user.id))
        return render(request, "login.html")
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        
        if user is not None:
            do_login(request, user)
            user_type = 'lender' if user.profile.is_lender else 'borrower'
            return redirect('/{}/{}'.format(user_type, user.id))
        
        messages.error(request, 'Invalid credentials')
        return redirect('/login')

def logout(request):
    do_logout(request)
    return redirect('/login')
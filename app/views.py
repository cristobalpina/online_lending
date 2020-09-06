from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import Lender, Borrower, Loan

def index(request):
    return redirect("/login")

def register(request):
    return render(request, "register.html")

def create_lender(request):
    pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
    Lender.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=pw_hash, money=request.POST["money"])
    return redirect("/login")

def create_borrower(request):
    pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
    Borrower.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        password=pw_hash,
        need_money_for=request.POST["need_money_for"],
        description=request.POST["description"],
        amount_needed=request.POST["amount_needed"],
    )
    return redirect("/login")

def borrower_profile(request, id):
    if id != request.session["userId"]:
        return redirect("/{}/{}".format(request.session['type'], request.session['userId']))
    borrower = Borrower.objects.get(id=id)
    context = {
        "borrower": borrower,
    }
    return render(request, "borrower.html", context)

def lender_profile(request, id):
    lender = Lender.objects.get(id=id)
    borrowers = Borrower.objects.all()
    context = {
        "lender": lender,
        "borrowers": borrowers
    }
    return render(request, "lender.html", context)

def lend(request):
    borrower = Borrower.objects.get(id=request.POST["borrower_id"])
    lender = Lender.objects.get(id=request.session["userId"])
    amount = int(request.POST["amount"])
    if lender.account_balance - amount < 0:
        messages.error(request, "Insufficient funds")
        return redirect("/{}/{}".format(request.session['type'], request.session['userId']))
    Loan.objects.create(borrower=borrower, lender=lender, amount=amount)
    return redirect("/{}/{}".format(request.session['type'], request.session['userId']))

# Auth
def login(request):
    if request.method == 'GET':
        if request.session['userId'] == None:
           return render(request, "login.html")
        return redirect("/{}/{}".format(request.session['type'], request.session['userId']))

    elif request.method == 'POST':
        user = None
        lender = Lender.objects.filter(email=request.POST['email'])
        if lender:
            request.session['type'] = 'lender'
            user = lender[0]
        else:
            borrower = Borrower.objects.filter(email=request.POST['email'])
            if borrower:
                request.session['type'] = 'borrower'
                user = borrower[0]
        if user:
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['userId'] = user.id
                return redirect("/{}/{}".format(request.session['type'], request.session['userId']))
        messages.error(request, "Incorrect username or password.")
        return redirect("/login")
    
def logout(request):
    request.session['userId'] = None
    request.session['type'] = None
    return redirect("/login")
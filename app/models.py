from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_lender = models.BooleanField(default=False)
    is_borrower = models.BooleanField(default=False)

class Lender(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    money = models.IntegerField()
    @property
    def account_balance(self):
        try:
            
            return self.money - Loan.objects.filter(lender_id=self.id).values("lender_id").annotate(total=Sum('amount'))[0]["total"]
        except:
            return self.money

    @property
    def debtors(self):
        debtors = Borrower.objects.filter(loans__lender_id=self.id).annotate(amount_lent=Sum("loans__amount"))
        return debtors

class Borrower(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    need_money_for = models.CharField(max_length=100)
    description = models.TextField()
    amount_needed = models.IntegerField()
    @property
    def amount_raised(self):
        try:
            return Loan.objects.filter(borrower_id=self.id).values("borrower_id").annotate(total=Sum("amount"))[0]["total"]
        except:
            return 0
       
    @property
    def creditors(self):
        creditors = Lender.objects.filter(loans__borrower_id=self.id).annotate(amount_lent=Sum("loans__amount"))
        return creditors

class Loan(models.Model):
    amount = models.IntegerField()
    lender = models.ForeignKey(Lender, related_name="loans", on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, related_name="loans", on_delete=models.CASCADE)
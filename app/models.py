from django.db import models
from django.db.models import Sum

# Transform this into OOP later
class Lender(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    money = models.IntegerField()

    @property
    def debtors(self):
        debtors = Borrower.objects.filter(loans__lender_id=self.id).annotate(amount_lent=Sum("loans__amount"))
        return debtors

    @property
    def account_balance(self):
        try:
            return self.money - Loan.objects.filter(lender_id=self.id).values("lender_id").annotate(amount_lent=Sum("amount"))[0]["amount_lent"]
        except:
            return self.money

class Borrower(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    need_money_for = models.CharField(max_length=255)
    description = models.TextField()
    amount_needed = models.IntegerField()

    @property
    def amount_raised(self):
        try:
            amount = Loan.objects.filter(borrower_id=self.id).values("borrower_id").annotate(total=Sum("amount"))[0]["total"]
        except:
            amount = 0
        return amount

    @property
    def creditors(self):
        creditors = Lender.objects.filter(loans__borrower_id=self.id).annotate(amount_lent=Sum("loans__amount"))
        return creditors

class Loan(models.Model):
    lender=models.ForeignKey(Lender, related_name="loans", on_delete=models.CASCADE)
    borrower=models.ForeignKey(Borrower, related_name="loans", on_delete=models.CASCADE)
    amount=models.IntegerField()
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    monthly_income = models.FloatField()
    phone_number = models.CharField(max_length=15)
    approved_limit = models.FloatField(default=0)
    current_debt = models.FloatField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()  
    monthly_repayment = models.FloatField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan {self.id} - {self.customer.first_name}"

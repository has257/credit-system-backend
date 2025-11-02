from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer ,Loan
from .serializers import CustomerSerializer

@api_view(['POST'])
def register_customer(request):
    """
    Register a new customer.
    Accepts: first_name, last_name, age, monthly_income, phone_number
    Calculates approved_limit as 36 * monthly_income
    Returns full customer details as JSON
    """
    serializer = CustomerSerializer(data=request.data)
    
    if serializer.is_valid():
        # Calculate approved_limit before saving
        monthly_income = serializer.validated_data['monthly_income']
        approved_limit = 36 * monthly_income
        
        # Create customer with calculated approved_limit
        customer = Customer.objects.create(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            age=serializer.validated_data['age'],
            monthly_income=monthly_income,
            phone_number=serializer.validated_data['phone_number'],
            approved_limit=approved_limit,
            current_debt=0
        )
        
        # Return full customer details
        response_serializer = CustomerSerializer(customer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.db.models import Sum
import math
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan

@api_view(['POST'])
def check_eligibility(request):
    """
    Check if a customer is eligible for a new loan.
    Accepts: customer_id, loan_amount, interest_rate, tenure
    Returns: approval status, credit score, interest rate, EMI, etc.
    """
    try:
        customer = Customer.objects.get(id=request.data['customer_id'])
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    loan_amount = float(request.data['loan_amount'])
    interest_rate = float(request.data['interest_rate'])
    tenure = int(request.data['tenure'])

    # 1️⃣ Calculate total existing debt
    existing_loans = Loan.objects.filter(customer=customer, is_approved=True)
    total_existing_debt = existing_loans.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0

    # 2️⃣ Simple credit score (0–100)
    credit_score = 100
    if total_existing_debt > customer.approved_limit * 0.8:
        credit_score -= 40
    elif total_existing_debt > customer.approved_limit * 0.5:
        credit_score -= 20

    # 3️⃣ Check eligibility
    if credit_score < 50 or loan_amount > (customer.approved_limit - total_existing_debt):
        return Response({
            "customer_id": customer.id,
            "approval": False,
            "credit_score": credit_score,
            "reason": "Credit score too low or exceeds approved limit"
        }, status=status.HTTP_200_OK)

    # 4️⃣ If eligible → calculate EMI (monthly payment)
    r = interest_rate / (12 * 100)
    EMI = (loan_amount * r * ((1 + r) ** tenure)) / (((1 + r) ** tenure) - 1)

    return Response({
        "customer_id": customer.id,
        "approval": True,
        "credit_score": credit_score,
        "interest_rate": interest_rate,
        "monthly_installment": round(EMI, 2)
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_loan(request):
    """
    Create a new loan for a customer if eligible.
    Accepts: customer_id, loan_amount, interest_rate, tenure
    Returns: loan details + approval status
    """
    try:
        customer = Customer.objects.get(id=request.data['customer_id'])
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    loan_amount = float(request.data['loan_amount'])
    interest_rate = float(request.data['interest_rate'])
    tenure = int(request.data['tenure'])

    # Calculate total existing debt
    existing_loans = Loan.objects.filter(customer=customer, is_approved=True)
    total_existing_debt = existing_loans.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0

    # Calculate credit score again (same logic as check_eligibility)
    credit_score = 100
    if total_existing_debt > customer.approved_limit * 0.8:
        credit_score -= 40
    elif total_existing_debt > customer.approved_limit * 0.5:
        credit_score -= 20

    # Eligibility check
    if credit_score < 50 or loan_amount > (customer.approved_limit - total_existing_debt):
        return Response({
            "customer_id": customer.id,
            "approval": False,
            "credit_score": credit_score,
            "message": "Loan cannot be approved due to low credit score or limit exceeded"
        }, status=status.HTTP_200_OK)

    # Calculate EMI
    r = interest_rate / (12 * 100)
    EMI = (loan_amount * r * ((1 + r) ** tenure)) / (((1 + r) ** tenure) - 1)

    # Create new loan record
    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        interest_rate=interest_rate,
        tenure=tenure,
        monthly_repayment=round(EMI, 2),
        is_approved=True
    )

    # Update customer's current debt
    customer.current_debt += loan_amount
    customer.save()

    return Response({
        "loan_id": loan.id,
        "customer_id": customer.id,
        "approval": True,
        "credit_score": credit_score,
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "tenure": tenure,
        "monthly_installment": round(EMI, 2),
        "message": "Loan approved successfully"
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def view_loan(request, loan_id):
    """
    Retrieve loan details using loan_id.
    """
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

    customer = loan.customer

    data = {
        "loan_id": loan.id,
        "customer_id": customer.id,
        "customer_name": f"{customer.first_name} {customer.last_name}",
        "loan_amount": loan.loan_amount,
        "interest_rate": loan.interest_rate,
        "tenure": loan.tenure,
        "monthly_repayment": loan.monthly_repayment,
        "is_approved": loan.is_approved,
        "start_date": loan.start_date,
        "end_date": loan.end_date
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_loans(request, customer_id):
    """
    Retrieve all loans for a specific customer.
    Returns a list of all loan details.
    """
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    loans = Loan.objects.filter(customer=customer)
    loan_list = []

    for loan in loans:
        loan_list.append({
            "loan_id": loan.id,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "tenure": loan.tenure,
            "monthly_repayment": loan.monthly_repayment,
            "is_approved": loan.is_approved,
            "start_date": loan.start_date,
            "end_date": loan.end_date
        })

    return Response({
        "customer_id": customer.id,
        "customer_name": f"{customer.first_name} {customer.last_name}",
        "total_loans": len(loan_list),
        "loans": loan_list
    }, status=status.HTTP_200_OK)

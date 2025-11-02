import pandas as pd
from api.models import Customer, Loan

def load_customer_data():
    df = pd.read_excel('credit_system/__pycache__/data/customer_data.xlsx')
    for _, row in df.iterrows():
        customer, _ = Customer.objects.get_or_create(
            id=row['Customer ID'],
            defaults={
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'age': row['Age'],
                'monthly_income': row['Monthly Salary'],
                'phone_number': row['Phone Number'],
                'approved_limit': row['Approved Limit'],
                'current_debt': row.get('Current Debt', 0),

            }
        )

def load_loan_data():
    import pandas as pd
    from api.models import Customer, Loan

    df = pd.read_excel('credit_system/__pycache__/data/loan_data.xlsx')

    for _, row in df.iterrows():
        try:

            customer_id = int(row['Customer ID'])
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            print(f"⚠️ Customer ID {customer_id} not found, skipping this loan.")
            continue

        # Update if loan exists, else create a new one
        Loan.objects.update_or_create(
            id=int(row['Loan ID']),
            defaults={
                'customer': customer,
                'loan_amount': float(row['Loan Amount']),
                'interest_rate': float(row['Interest Rate']),
                'tenure': int(row['Tenure']),
                'monthly_repayment': float(row['Monthly payment']),
                'is_approved': True,  # already approved in dataset
                'start_date': pd.to_datetime(row['Date of Approval']),
                'end_date': pd.to_datetime(row['End Date']),
            }
        )

    print("✅ Loan data loaded successfully!")


def run():
    load_customer_data()
    load_loan_data()
    print("✅ Data loaded successfully!")

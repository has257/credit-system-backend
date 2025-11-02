# 🏦 Credit Scoring & Loan Management System

A RESTful backend application built with *Django* and *Django REST Framework*, containerized using *Docker* and powered by *PostgreSQL*.  
This system manages customer registration, loan eligibility checks, loan creation, and viewing of loan details.

---

## 🚀 Features

- Customer Registration: Register new customers with automatic credit limit calculation.  
- Loan Eligibility Check: Evaluate customer eligibility based on income and credit data.  
- Loan Creation:Create and store loan details for eligible customers.  
- Loan Viewing: Fetch loan details for individual or multiple customers.  
- PostgreSQL Integration: Robust relational database via Docker.  
- Containerized Deployment: Fully Dockerized for consistent local and production environments.

---

## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | Django 5.2 + Django REST Framework |
| Database | PostgreSQL |
| Containerization | Docker, Docker Compose |
| Language | Python 3.10+ |
| API Testing | Postman |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
''' bash
git clone https://github.com/<your-username>/credit-system.git
cd credit-system '''

2. Build and Run using Docker
docker-compose up --build


This will automatically start:

A PostgreSQL container (db)

A Django web server (web) on port 8000


🧩 API Endpoints
Method	Endpoint	Description
POST	/register/	Register a new customer
POST	/check-eligibility/	Check loan eligibility for a customer
POST	/create-loan/	Create a new loan
GET	/view-loan/<loan_id>/	View details of a specific loan
GET	/view-loans/<customer_id>/	View all loans of a customer

🧪 Example Request

POST /register/

{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "monthly_income": 50000,
  "phone_number": "1234567890"
}

🐳 Notes

The app runs at http://127.0.0.1:8000/

Make sure Docker Desktop is running before executing the commands.

If you need to rebuild cleanly:

docker compose down
docker compose up --build

👩‍💻 Tech Stack

Django & Django REST Framework

PostgreSQL

Docker & Docker Compose
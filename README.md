Daily Expense Sharing Application
This is a backend application for managing and sharing daily expenses among multiple users. It provides functionalities for user authentication, creating and splitting expenses (equally, exactly, and by percentage), and generating balance sheets.

Features ----
  User registration and authentication (JWT-based).
  Included error handling and input validation.
  optimized performance for larger datasets
  Create expenses and split them equally, by exact amounts, or by percentage.
  Fetch expenses by user.
  Download a balance sheet as a PDF file.
Technologies Used ---
  Python 3.9+
  Django 4.x
  Django REST Framework
  PostgreSQL (or any other database of your choice)
  ReportLab (for PDF generation)
  Simple JWT (for authentication)
Getting Started
  Prerequisites
  Make sure you have the following installed on your local machine:
  
  Python 3.9+
  Django DRF
  Django

  
  step 1- Clone the repository
  step 2 -Install required dependencies 
  step 3 - cd expenseshare, then run python manage.py runserver (python manage.py test for testing)
  step 3 - Use postman or anyother api testing tools
  NOTE- GENERATE TOKEN FROM GET /API/TOKEN/  and when sending the payload set autorization as token bearer and add this key to the payload. There is a time limit on the token generation so you have to do it multiple times

  EVERY API ENDPOINT IS SECURED SO ENSURE YOU HAVE ADDED THE TOKEN TO THE PAYLOAD WHILE TESTING API ENDPOINTS  



API Endpoints
  Authentication:
  
  Login: /api/token/ (POST) — Obtain JWT token.
  Refresh Token: /api/token/refresh/ (POST) — Refresh the JWT token.
  Users:
  
  /users/ (GET, POST) — List and create users.
  /users/{id}/ (GET, PUT, DELETE) — Get, update, or delete a specific user.
  Expenses:
  
  /expenses/ (GET, POST) — List all expenses, create an expense.
  /expenses/user/{user_id}/ (GET) — Get expenses for a specific user.
  /expenses/overall/ (GET) — Get all expenses.
  /expenses/balancesheet/ (GET) — Download balance sheet as a PDF.
Running Tests
To run the test suite:

Ensure your database is set up for testing.

You can use the default SQLite for testing or configure your test database in settings.py.

Run the tests:

bash
Copy code
python manage.py test
This will run all the test cases, including tests for expense creation, user management, and balance sheet generation.




Contact
If you have any questions or suggestions, feel free to contact me at your-vardan21110@iiitd.ac.in


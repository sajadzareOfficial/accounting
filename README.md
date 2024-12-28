# Income and Expense Tracker  

## Description  
This project is a web application built with Django that allows users to track their income and expenses. Users can register, log in, and manage their financial records, including adding new income and expense entries, viewing their financial dashboard, and receiving email confirmations for account activation.  

## Features  
- User registration and authentication  
- Income and expense tracking  
- Dashboard for viewing total income and expenses  
- Email notifications for account activation  
- CSRF protection for secure form submissions  

## Technologies Used  
- Python  
- Django  
- SQLite (or any other database of your choice)  
- HTML/CSS for frontend  
- Django REST Framework (optional for API features)  

## Installation  

### Prerequisites  
- Python 3.x  
- pip (Python package installer)  
- Django  

### Steps to Install  
1. **Clone the repository:**  
   ```bash  
   git clone https://github.com/odriew3j/accounting.git  
   cd accounting
2. Create a virtual environment:
   ```bash  
    python -m venv venv  
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
4. Set up the setting:
   ```bash
   mv settings.py.sample settings.py  # On Windows use `ren settings.py.sample settings.py`
5. Set up the database:
   ```bash
   python manage.py migrate
6. Run the development server:
   ```bash
    python manage.py runserver  
7. Access the application:
Open your web browser and go to http://127.0.0.1:8000/.

Usage
Register a new account by filling out the registration form.
Activate your account using the link sent to your email.
Log in to access the dashboard.
Add income and expenses through the provided forms on the dashboard.
View your financial summary on the dashboard.
Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any inquiries, please contact [mohammad.mousavi3j@gmail.com].




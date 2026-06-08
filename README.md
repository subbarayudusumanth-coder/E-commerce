Online Shopping System (Python + MySQL)
Online Shopping System is a console-based e-commerce application developed using Python and MySQL. The system enables users to register, log in securely, browse products, search for items, manage shopping carts, place orders, and view order history. It also includes inventory management and password security using SHA-256 hashing.

Features
Feature	Description
User Registration	Allows new users to create an account
User Login	Authenticates users using username and password 
View Products	Displays all available products
Search Products	Enables users to search products by name
Add to Cart	Adds selected products to the shopping cart
View Cart	Displays products added to the cart
Remove from Cart	Removes products from the cart
Payment System	Processes payments for placed orders
Place Orders	Allows users to confirm and place orders
Order History	Displays previously placed orders
Stock Management	Updates and maintains product inventory
Logout	Safely logs out the current user
Database Design
The application uses MySQL as the backend database and consists of the following tables:

Table Name	Purpose
users	Stores user account information and hashed passwords
products	Stores product details such as name, price, stock, and category
cart	Stores products added to a user's shopping cart
orders	Stores order information and order status
payments	Stores payment details and transaction records
Database Relationships
One user can place multiple orders.
One user can have multiple cart items.
One order can contain multiple products.
Products are linked to inventory stock management.
Payments are associated with placed orders.
Tools & Technologies Used
Python
MySQL
SQL
Git
GitHub
Project Structure
Online-shop-Project
│
├── main.py
├── database.sql
├── requirements.txt
└── Project screenshots

How to Run the Project
Install Python
Install MySQL
Create database CREATE DATABASE onlineshop;
Run the SQL file
database.sql

Install dependency
pip install -r requirements.txt

Run the program
python main.py

Project Screenshots
Registration
![Registration](Project screenshots/Registration.png)

Login
![Login](Project screenshots/Login.png)

View Products
![View Products](Project screenshots/View_Products.png)

Search Products
![Search Products](Project screenshots/Search_Products.png)

Add To Cart
![Add To Cart](Project screenshots/Add_to_Cart.png)

View Cart
![View Cart](Project screenshots/View_cart.png)

Remove From Cart
![Remove From Cart](Project screenshots/Remove_From_cart.png)

Payment
![Payment](Project screenshots/Payment.png)

Place Order
![Place Order](Project screenshots/Place_Order.png)

Order History
![Order History](Project screenshots/Order_History.png)

Logout
![Logout](Project screenshots/Logout.png)

Exit
![Exit](Project screenshots/Exit.png)

Author
Sumanth

AIML Student | Python Developer | Aspiring Software Engineer

GitHub: https://github.com/subbarayudusumanth-coder

LinkedIn:https://www.linkedin.com/in/sumanth-thurpunati-a2048b346/

 
# ---------------- DATABASE CONNECTION ----------------

import mysql.connector 
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="parnikaa",
    database="onlineshop"
)
cursor=conn.cursor()
print("connected succesfullyy")
 
 
 
# ---------------- USER REGISTER ----------------

def register():
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    query = "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)"
    cursor.execute(query,(name,email,password))
    conn.commit()

    print("Registration Successful")


# ---------------- USER LOGIN ----------------

def login():

    email = input("Enter Email: ")
    password = input("Enter Password: ")

    query = "SELECT user_id FROM users WHERE email=%s AND password=%s"
    cursor.execute(query,(email,password))

    user = cursor.fetchone()

    if user:
        print("Login Successful")
        return user[0]
    else:
        print("Invalid Login")
        return None
#------------------ ADMIN LOGIN ----------------

def admin_login():
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")

    if username == "admin" and password == "admin123":
        print("Admin Login Successful")
        return True
    else:
        print("Invalid Admin Credentials")
        return False
    
# ---------------- VIEW PRODUCTS ----------------

def view_products():

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    print("\nAvailable Products\n")

    for p in products:
        print("ID:",p[0],"Name:",p[1],"Price:",p[2],"Stock:",p[3])

# ---------------- SEARCH PRODUCT ----------------    
    
def search_product():

    keyword = input("Enter Product Name To Search: ")

    query = """
    SELECT * FROM products
    WHERE product_name LIKE %s
    """

    cursor.execute(query, ("%" + keyword + "%",))

    products = cursor.fetchall()

    if products:

        print("\nSearch Results\n")

        for p in products:
            print("ID:", p[0], "Name:", p[1],
                  "Price:", p[2], "Stock:", p[3])

    else:
        print("No Products Found")


# ---------------- ADD TO CART ----------------

def add_to_cart(user_id):

    product_id = int(input("Enter Product ID: "))
    quantity = int(input("Enter Quantity: "))

    query = "INSERT INTO cart(user_id,product_id,quantity) VALUES(%s,%s,%s)"

    cursor.execute(query,(user_id,product_id,quantity))
    conn.commit()

    print("Product Added To Cart")


# ---------------- VIEW CART ----------------

def view_cart(user_id):
  
    query = """
    SELECT products.product_name, products.price, cart.quantity
    FROM cart
    JOIN products
    ON cart.product_id = products.product_id
    WHERE cart.user_id=%s
    """

    cursor.execute(query,(user_id,))
    items = cursor.fetchall()

    print("\nYour Cart\n")

    for item in items:
        name, price, quantity = item
        print(name,"Price:",price,"Qty:",quantity)


# ---------------- PLACE ORDER ----------------

def place_order(user_id):

    query = """
    SELECT cart.product_id, cart.quantity, products.price
    FROM cart
    JOIN products
    ON cart.product_id = products.product_id
    WHERE cart.user_id=%s
    """

    cursor.execute(query,(user_id,))
    items = cursor.fetchall()

    total = 0

    for item in items:

        product_id, quantity, price = item

 

        # check stock
        cursor.execute("SELECT stock FROM products WHERE product_id=%s",(product_id,))
        stock = cursor.fetchone()

        if not stock:
                print("Product not found")
                return

        stock = stock[0]

        if quantity > stock:
            print("Not enough stock for product ID:",product_id)
            return

        total += quantity * price
 
        cursor.execute(
        "INSERT INTO orders(user_id,product_id,quantity) VALUES(%s,%s,%s)",
        (user_id,product_id,quantity)
        )
        # reduce stock
        cursor.execute("update products set stock=stock-%s where product_id=%s",(quantity,product_id))

    conn.commit()

    print("Order Placed Successfully")
    print("Total Amount:",total)

    return total


# ---------------- PAYMENT ----------------

def make_payment(user_id,total):

    method = input("Enter Payment Method (UPI/Card/COD): ")

    query = """
    INSERT INTO payments(user_id,amount,payment_method,payment_status)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(query,(user_id,total,method,"Success"))
    conn.commit()

    print("Payment Successful")


# ---------------- MOVE TO ORDER HISTORY ----------------

def move_to_history(user_id):

    query = """
    INSERT INTO order_history(user_id,product_id,quantity,order_date,status)
    SELECT user_id,product_id,quantity,order_date,'Completed'
    FROM orders
    WHERE user_id=%s
    """

    cursor.execute(query,(user_id,))
     
    cursor.execute("DELETE FROM orders WHERE user_id=%s",(user_id,))
    conn.commit()

    print("Order Saved In History")


# ---------------- VIEW ORDER HISTORY ----------------

def view_order_history(user_id):

    query = """
    SELECT products.product_name,
           order_history.quantity,
           order_history.order_date,
           order_history.status
    FROM order_history
    JOIN products
    ON order_history.product_id = products.product_id
    WHERE order_history.user_id=%s
    """

    cursor.execute(query,(user_id,))
    orders = cursor.fetchall()

    print("\nOrder History\n")

    for o in orders:
        name, qty, date, status = o
        print(name,"Qty:",qty,"Date:",date,"Status:",status)


# ---------------- MAIN PROGRAM ----------------

while True:

    print("\n===== ONLINE SHOPPING SYSTEM =====")
    print("1 Register")
    print("2 Login")
    print("3 ADMIN LOGIN")
    print("4 EXIT")

    choice = input("Enter Choice: ")

    if choice == "1":
        register()

    elif choice == "2":

        user_id = login()

        if user_id:
            total = 0 

            while True:

                print("\n----- USER MENU -----")
                print("1 View Products")
                print("2 Search Products")
                print("3 Add To Cart")
                print("4 View Cart")
                print("5 Place Order")
                print("6 Payment")
                print("7 Order History")
                print("8 Logout")

                ch = input("Enter Choice: ")

                if ch == "1":
                    view_products()

                elif ch == "2":
                    search_product()

                elif ch == "3":
                    add_to_cart(user_id)

                elif ch == "4":
                    view_cart(user_id)

                elif ch == "5":
                    total = place_order(user_id)
                elif ch == "6":
                 if total > 0:
                  make_payment(user_id,total)
                  move_to_history(user_id)
                  total = 0
                 else:
                   print("No order placed yet")

                # elif ch == "5":
                #     make_payment(user_id,total)
                #     move_to_history(user_id)

                elif ch == "7":
                    view_order_history(user_id)

                elif ch == "8":
                    print("Logged out")
                    break
    elif choice == "3":

      if admin_login():

        while True:

            print("\n----- ADMIN MENU -----")
            print("1 View Products")
            print("2 LOGOUT")
            ch=input("Enter choice:")
            if ch == "1":
                view_products()
                
            elif ch == "2":
                break
    elif choice == "4":
        print("Thank You")
        break
 
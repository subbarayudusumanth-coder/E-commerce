 
# ---------------- DATABASE CONNECTION ----------------

import mysql.connector 
import hashlib
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
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    query = "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)"
    cursor.execute(query,(name,email,hashed_password))
    conn.commit()

    print("Registration Successful")

# ---------------- USER LOGIN ----------------

def login():

    email = input("Enter Email: ")
    password = input("Enter Password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    query = "SELECT user_id FROM users WHERE email=%s AND password=%s"
    cursor.execute(query,(email,hashed_password))

    user = cursor.fetchone()

    if user:
        print("Login Successful")
        return user[0]
    else:
        print("Invalid Login")
        return None

  # ---------------- ADMIN LOGIN ----------------  
    
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
        
# ---------------- ADD PRODUCT ----------------
        
def add_product():

    name = input("Enter Product Name: ")
    price = float(input("Enter Price: "))
    stock = int(input("Enter Stock: "))

    query = """
    INSERT INTO products(product_name,price,stock)
    VALUES(%s,%s,%s)
    """

    cursor.execute(query,(name,price,stock))
    conn.commit()

    print("Product Added Successfully")

# ---------------- DELETE PRODUCT ----------------  

def delete_product():

    product_id = int(input("Enter Product ID To Delete: "))

    cursor.execute(
        "SELECT * FROM cart WHERE product_id=%s",
        (product_id,)
    )

    item = cursor.fetchone()

    if item:
        print("Product exists in carts. Cannot delete.")
        return

    cursor.execute(
        "DELETE FROM products WHERE product_id=%s",
        (product_id,)
    )

    conn.commit()

    print("Product Deleted Successfully")

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
    total=0

    for item in items:
        name, price, quantity = item
        print(name,"Price:",price,"Qty:",quantity)
        total += price*quantity
        
    print("Total cart amount:",total)
    
# ---------------- REMOVE FROM CART ----------------
    
def remove_from_cart(user_id):

    product_id = int(input("Enter Product ID to remove: "))

    query = """
    DELETE FROM cart
    WHERE user_id=%s AND product_id=%s
    """

    cursor.execute(query, (user_id, product_id))
    conn.commit()

    print("Product removed from cart successfully")
    
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
        cursor.execute(
        "UPDATE products SET stock = stock - %s WHERE product_id=%s",
        (quantity,product_id)
        )

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
    
    cursor.execute("DELETE FROM cart WHERE user_id=%s",(user_id,))

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
    print("3 Admin Login")
    print("4 Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        register()

    elif choice == "2":

        user_id = login()

        if user_id:
            total=0

            while True:

                print("\n----- USER MENU -----")
                print("1 View Products")
                print("2 Search Product")
                print("3 Add To Cart")
                print("4 View Cart")
                print("5 Remove From Cart")
                print("6 Place Order")
                print("7 Payment")
                print("8 Order History")
                print("9 Logout")

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
                    remove_from_cart(user_id)

                elif ch == "6":
                    total = place_order(user_id)

                elif ch == "7":
                #     make_payment(user_id,total)
                #     move_to_history(user_id)elif ch == "5":
                   if total > 0:
                       
                        make_payment(user_id,total)
                        move_to_history(user_id)
                        total = 0
                   else:
                      print("No order placed yet")

                elif ch == "8":
                    view_order_history(user_id)

                elif ch == "9":
                    print("Thank You For Shopping!")
                    break

    elif choice == "3":

      if admin_login():

        while True:

            print("\n----- ADMIN MENU -----")
            print("1 View Products")
            print("2 Add Product")
            print("3 Delete Product")
    #         print("4 Delete Product")
    #         print("5 View Users")
    #         print("6 View Orders")
            print("4 Logout")
            
            ch = input("Enter Choice: ")

            if ch == "1":
                view_products()
                
            if ch == "2":
                add_product()
                
            if ch == "3":
                delete_product()
                
            elif ch == "4":
                break


    elif choice == "4":
        print("Thank You")
        break
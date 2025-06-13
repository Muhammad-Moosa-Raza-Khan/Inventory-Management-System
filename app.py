import datetime
from flask import Flask, abort, redirect, render_template, request, url_for
import pyodbc

app = Flask(__name__)

# MS SQL Server Connection Configuration
SERVER = 'MOOSA'
DATABASE = 'Inventory Management System'
DRIVER = '{SQL Server}'

# Construct the connection string
conn_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Configuration=True;'

@app.route("/", methods=["GET", "POST"])  # Modified route
def products():
    search_term = request.args.get("search")  # Get search term from query parameters
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    if search_term:
        # Search query (using LIKE for partial matches)
        cursor.execute("""
            SELECT product_id, name, selling_price, current_quantity
            FROM Products
            WHERE name LIKE ? OR description LIKE ?
        """, f"%{search_term}%", f"%{search_term}%")  # Use parameterized query
    else:
        cursor.execute("SELECT product_id, name, selling_price, current_quantity FROM Products")
    products = cursor.fetchall()
    conn.close()
    return render_template("products.html", products=products, search_term=search_term) # Pass search term to template

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE product_id = ?", product_id)
    product = cursor.fetchone()
    conn.close()
    if product is None:
        abort(404)
    return render_template("product_detail.html", product=product)

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE product_id = ?", product_id)
    product = cursor.fetchone()
    if product is None:
        conn.close()
        return "Product not found", 404

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        category_id = request.form.get("category_id") or None
        supplier_id = request.form["supplier_id"]
        cost_price = request.form["cost_price"]
        selling_price = request.form["selling_price"]
        current_quantity = request.form["current_quantity"]
        minimum_quantity = request.form["minimum_quantity"]
        reorder_quantity = request.form["reorder_quantity"]
        unit = request.form["unit"]

        cursor.execute("""
            UPDATE Products 
            SET name = ?, description = ?, category_id = ?, supplier_id = ?, 
                cost_price = ?, selling_price = ?, current_quantity = ?,
                minimum_quantity = ?, reorder_quantity = ?, unit = ?
            WHERE product_id = ?""",
                       name, description, category_id, supplier_id, cost_price, selling_price, current_quantity, minimum_quantity, reorder_quantity, unit, product_id)
        conn.commit()
        conn.close()
        return redirect(url_for("products"))

    conn.close()
    return render_template("edit_product.html", product=product)

@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM Products WHERE product_id = ?", product_id)
    if not cursor.fetchone():
        conn.close()
        return "Product not found", 404
    
    cursor.execute("DELETE FROM Products WHERE product_id = ?", product_id)
    conn.commit()
    conn.close()
    return redirect(url_for("products"))

@app.route("/add_product", methods=["GET", "POST"])
def add_product_route():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        category_id = request.form.get("category_id") or None
        supplier_id = request.form["supplier_id"]
        cost_price = request.form["cost_price"]
        selling_price = request.form["selling_price"]
        current_quantity = request.form["current_quantity"]
        minimum_quantity = request.form["minimum_quantity"]
        reorder_quantity = request.form["reorder_quantity"]
        unit = request.form["unit"]

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (name, description, category_id, supplier_id, cost_price, selling_price, current_quantity, minimum_quantity, reorder_quantity, unit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        name, description, category_id, supplier_id, cost_price, selling_price, current_quantity, minimum_quantity, reorder_quantity, unit)
        conn.commit()
        conn.close()
        return redirect(url_for("products"))

    return render_template("add_product.html")

# Categories Routes
@app.route("/categories")
def categories():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Categories")
    categories = cursor.fetchall()
    conn.close()
    return render_template("categories.html", categories=categories)

@app.route("/categories/add", methods=["GET", "POST"])
def add_category_route():
    if request.method == "POST":
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        name = request.form["name"]
        description = request.form["description"]
        cursor.execute("INSERT INTO Categories (name, description) VALUES (?, ?)", name, description)
        conn.commit()
        conn.close()
        return redirect(url_for("categories"))
    return render_template("add_category.html")

@app.route("/categories/edit/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Categories WHERE category_id = ?", category_id)
    category = cursor.fetchone()
    if category is None:
        conn.close()
        abort(404)
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        cursor.execute("UPDATE Categories SET name = ?, description = ? WHERE category_id = ?", name, description, category_id)
        conn.commit()
        conn.close()
        return redirect(url_for("categories"))
    conn.close()
    return render_template("edit_category.html", category=category)

@app.route("/categories/delete/<int:category_id>", methods=["POST"])
def delete_category_route(category_id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Categories WHERE category_id = ?", category_id)
    conn.commit()
    conn.close()
    return redirect(url_for("categories"))

@app.route("/transactions")
def transactions():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TransactionHistory")
    transactions = cursor.fetchall()
    conn.close()
    return render_template("transactions.html", transactions=transactions)

@app.route("/transactions/add", methods=["GET", "POST"])
def add_transaction():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("SELECT product_id, name FROM Products")
    products = cursor.fetchall()
    cursor.execute("SELECT location_id, name FROM Locations")
    locations = cursor.fetchall()
    cursor.execute("SELECT customer_id, name FROM Customers")
    customers = cursor.fetchall()
    conn.close()

    if request.method == "POST":
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        product_id = request.form["product_id"]
        transaction_type = request.form["transaction_type"]
        quantity = request.form["quantity"]
        unit_price = request.form["unit_price"]
        location_id = request.form["location_id"] or None #Handles empty location_id
        customer_id = request.form["customer_id"] or None #Handles empty customer_id

        cursor.execute("INSERT INTO Transactions (product_id, transaction_type, quantity, unit_price, location_id, customer_id) VALUES (?, ?, ?, ?, ?, ?)", product_id, transaction_type, quantity, unit_price, location_id, customer_id)
        conn.commit()
        conn.close()
        return redirect(url_for("transactions"))

    return render_template("add_transaction.html", products=products, locations=locations, customers=customers)

@app.route("/reports/low_stock")
def low_stock_report():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM LowStockProducts")
    low_stock_products = cursor.fetchall()
    conn.close()
    return render_template("low_stock_report.html", low_stock_products=low_stock_products)

@app.route("/reports/inventory_valuation")
def inventory_valuation_report():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM InventoryValuation")
    inventory_valuation = cursor.fetchall()
    conn.close()
    return render_template("inventory_valuation_report.html", inventory_valuation=inventory_valuation)

@app.route("/reports/transaction_history")
def transaction_history_report():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TransactionHistory")
    transaction_history = cursor.fetchall()
    conn.close()
    return render_template("transaction_history_report.html", transaction_history=transaction_history)

if __name__ == "__main__":
    app.run(debug=True)
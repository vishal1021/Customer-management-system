from flask import Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Function to create a database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change as needed
        password="your_password",  # Change as needed
        database="CustomerManagement"  # Your database name
    )

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        mobile_no = request.form['mobile_no']
        age = request.form['age']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name, address, mobile_no, age) VALUES (%s, %s, %s, %s)", 
                       (name, address, mobile_no, age))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('show_customers'))
    return render_template('add_customer.html')

@app.route('/show_customers')
def show_customers():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('show_customers.html', customers=customers)

@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('search_customer.html', customer=customer)
    return render_template('search_customer.html', customer=None)

@app.route('/update_customer', methods=['POST'])
def update_customer():
    data = request.get_json()
    customer_id = data['id']
    name = data['name']
    address = data['address']
    mobile_no = data['mobile_no']
    age = data['age']
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = %s, address = %s, mobile_no = %s, age = %s WHERE id = %s",
                   (name, address, mobile_no, age, customer_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Customer updated successfully!"})


@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    customer_id = request.form['customer_id']
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('show_customers'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
import pymysql
from datetime import date

app = Flask(__name__)

# Connect to DB
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='blooddonation',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                bs.blood_type,
                bb.blood_bank_name,
                bb.baddress,
                bs.units_available
            FROM blood_stock bs
            JOIN blood_bank bb ON bs.blood_bank_id = bb.blood_bank_id
            ORDER BY bb.blood_bank_name, bs.blood_type
        """)
        blood_data = cursor.fetchall()
    conn.close()
    return render_template('home.html', blood_data=blood_data)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['name']
        phone = request.form['phone']

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, phone) VALUES (%s, %s)", (username, phone))
                conn.commit()
                return "✅ Registered successfully"
        except Exception as e:
            conn.rollback()
            return f"❌ Registration failed: {e}"
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/request_blood', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        phone = request.form['phone']
        blood_type = request.form['blood_type']
        units_requested = int(request.form['units'])

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 1. Get user
                cursor.execute("SELECT id FROM users WHERE phone = %s", (phone,))
                user = cursor.fetchone()
                if not user:
                    return "❌ User not found. Please register first."

                # 2. Check blood stock with sufficient units
                cursor.execute("""
                    SELECT blood_type, blood_bank_id, units_available
                    FROM blood_stock
                    WHERE blood_type = %s AND units_available >= %s
                    ORDER BY units_available DESC
                    LIMIT 1
                """, (blood_type, units_requested))
                stock = cursor.fetchone()

                if not stock:
                    return "❌ Not enough stock available."

                # 3. Create blood request
                cursor.execute("""
                    INSERT INTO blood_request (user_id, blood_type, units_requested, request_date, status)
                    VALUES (%s, %s, %s, %s, 'Pending')
                """, (user['id'], blood_type, units_requested, date.today()))

                # 4. Update blood_stock
                new_units = stock['units_available'] - units_requested
                cursor.execute("""
                    UPDATE blood_stock 
                    SET units_available = %s 
                    WHERE blood_type = %s AND blood_bank_id = %s
                """, (new_units, stock['blood_type'], stock['blood_bank_id']))

                conn.commit()
                return "✅ Blood request submitted successfully!"

        except Exception as e:
            conn.rollback()
            return f"❌ Error: {e}"
        finally:
            conn.close()

    return render_template('request_blood.html')

@app.route('/view_requests', methods=['GET', 'POST'])
def view_requests():
    if request.method == 'POST':
        phone = request.form['phone']
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE phone = %s", (phone,))
                user = cursor.fetchone()
                if not user:
                    return "❌ No user found with this phone number."

                cursor.execute("SELECT * FROM blood_request WHERE user_id = %s", (user['id'],))
                requests = cursor.fetchall()
                return render_template("view_requests.html", requests=requests)
        finally:
            conn.close()

    return render_template("view_requests_form.html")

@app.route('/register_donor', methods=['GET', 'POST'])
def register_donor():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'phone': request.form['phone'],
            'dob': request.form['dob'],
            'gender': request.form['gender'],
            'address': request.form['address'],
            'weight': int(request.form['weight']),
            'bp': int(request.form['bp']),
            'iron': int(request.form['iron']),
            'doctor_id': int(request.form['doctor_id']),
        }

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO donor (
                        donor_name, phone_no, DOB, gender, address, 
                        weight, blood_pressure, iron_content, doctor_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    data['name'], data['phone'], data['dob'], data['gender'],
                    data['address'], data['weight'], data['bp'], data['iron'], data['doctor_id']
                ))
                conn.commit()
                return "✅ Donor registered successfully!"
        except Exception as e:
            conn.rollback()
            return f"❌ Error: {e}"
        finally:
            conn.close()

    return render_template('register_donor.html')

@app.route('/cancel_request', methods=['POST'])
def cancel_request():
    request_id = request.form['request_id']
    phone = request.form['phone']

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get user
            cursor.execute("SELECT id FROM users WHERE phone = %s", (phone,))
            user = cursor.fetchone()
            if not user:
                return "❌ User not found."

            # Check ownership
            cursor.execute("SELECT * FROM blood_request WHERE request_id = %s AND user_id = %s", 
                           (request_id, user['id']))
            req = cursor.fetchone()
            if not req:
                return "❌ Request not found or unauthorized."

            # Delete request
            cursor.execute("DELETE FROM blood_request WHERE request_id = %s", (request_id,))
            conn.commit()
            return "✅ Request cancelled."
    except Exception as e:
        conn.rollback()
        return f"❌ Error: {e}"
    finally:
        conn.close()

@app.route('/donate_blood', methods=['GET', 'POST'])
def donate_blood():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM blood_bank")
            banks = cursor.fetchall()
    finally:
        conn.close()

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        blood_type = request.form['blood_type']
        units = int(request.form['units'])
        blood_bank_id = int(request.form['blood_bank_id'])

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO donor_log (donor_name, phone, blood_type, units, donate_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, phone, blood_type, units, date.today()))

                # Check if stock already exists for this blood type and bank
                cursor.execute("""
                    SELECT * FROM blood_stock WHERE blood_type = %s AND blood_bank_id = %s
                """, (blood_type, blood_bank_id))
                stock = cursor.fetchone()

                if stock:
                    cursor.execute("""
                        UPDATE blood_stock SET units_available = units_available + %s
                        WHERE blood_type = %s AND blood_bank_id = %s
                    """, (units, blood_type, blood_bank_id))
                else:
                    cursor.execute("""
                        INSERT INTO blood_stock (blood_type, blood_bank_id, units_available)
                        VALUES (%s, %s, %s)
                    """, (blood_type, blood_bank_id, units))

                conn.commit()
                return "🙏 Thank you for donating! Your blood was added to the selected blood bank."
        except Exception as e:
            conn.rollback()
            return f"❌ Donation failed: {e}"
        finally:
            conn.close()

    return render_template('donate_blood.html', banks=banks)



if __name__ == '__main__':
    app.run(debug=True)

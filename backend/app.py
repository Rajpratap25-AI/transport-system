from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from config import DB_CONFIG
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate

# ---------------- Utility ----------------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ---------------- Home ----------------
@app.route('/')
def home():
    return "Backend is running!"

# ---------------- Admin Login ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Example admin credentials
    admins = {
        "Avtar Singh": "Avtar72",
        "admin2": "truckboss",
        "admin3": "logistics321"
    }

    if username in admins and admins[username] == password:
        return jsonify({"message": "Login successful", "success": True})
    else:
        return jsonify({"message": "Invalid username or password", "success": False}), 401


# ---------------- Add Truck ----------------
@app.route('/add-truck', methods=['POST'])
def add_truck():
    data = request.json
    truck_number = data['truck_number']
    capacity = data['capacity']
    details = data.get('details', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO trucks (truck_number, capacity, details) VALUES (%s, %s, %s)",
        (truck_number, capacity, details)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Truck added successfully"})

# ---------------- Get Trucks ----------------
@app.route('/trucks', methods=['GET'])
def get_trucks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trucks")
    trucks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(trucks)

# ---------------- Delete Truck ----------------
@app.route('/delete-truck/<int:truck_id>', methods=['DELETE'])
def delete_truck(truck_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM trucks WHERE id = %s", (truck_id,))
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"message": str(err)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Truck deleted successfully"})

# ---------------- Add Trip ----------------
@app.route('/add-trip', methods=['POST'])
def add_trip():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO trips (truck_id, trip_date, origin, destination, goods, quantity) VALUES (%s, %s, %s, %s, %s, %s)",
        (
            data['truck_id'],
            data['trip_date'],
            data.get('origin', ''),
            data.get('destination', ''),
            data.get('goods', ''),
            data.get('quantity', 0)
        )
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Trip added successfully"})

# ---------------- Get Trips ----------------
@app.route('/trips', methods=['GET'])
def get_trips():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT trips.id, trucks.truck_number, trips.origin, trips.destination, trips.trip_date, trips.goods, trips.quantity "
        "FROM trips JOIN trucks ON trips.truck_id = trucks.id"
    )
    trips = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(trips)

# ---------------- Delete Trip ----------------
@app.route('/delete-trip/<int:trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM trips WHERE id = %s", (trip_id,))
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"message": str(err)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Trip deleted successfully"})

# ---------------- Delete All Trucks ----------------
@app.route('/delete-all-trucks', methods=['DELETE'])
def delete_all_trucks():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM trucks")
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"message": str(err)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "All trucks deleted successfully"})

# ---------------- Delete All Trips ----------------
@app.route('/delete-all-trips', methods=['DELETE'])
def delete_all_trips():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM trips")
        conn.commit()
    except mysql.connector.Error as err:
        return jsonify({"message": str(err)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "All trips deleted successfully"})

# ---------------- Run Flask ----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
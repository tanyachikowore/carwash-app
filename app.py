from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "secret123"

# Home
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = {
            "username": request.form['username'],
            "password": request.form['password']
        }

        try:
            with open('users.json', 'r') as f:
                data = json.load(f)
        except:
            data = []

        data.append(user)

        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)

        return redirect('/login')

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except:
            users = []

        for user in users:
            if user['username'] == username and user['password'] == password:
                session['user'] = username
                return redirect('/')

        return "Invalid login"

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# Book Appointment
@app.route('/book', methods=['POST'])
def book():

    wash_type = request.form['wash_type']

    prices = {
        "Basic Wash": 5,
        "Premium Wash": 10,
        "Interior Cleaning": 15,
        "Full Service": 20
    }

    price = prices.get(wash_type, 0)

    booking = {
        "user": session['user'],
        "name": request.form['name'],
        "phone": request.form['phone'],
        "address": request.form['address'],
        "day": request.form['day'],
        "time": request.form['time'],
        "car_type": request.form['car_type'],
        "wash_type": wash_type,
        "price": price,
        "status": "Pending",
        "worker": "Not Assigned",
        "payment_status": "Pending"
    }

    try:
        with open('bookings.json', 'r') as f:
            data = json.load(f)
    except:
        data = []

    data.append(booking)

    with open('bookings.json', 'w') as f:
        json.dump(data, f, indent=4)

    return redirect('/dashboard')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    try:
        with open('bookings.json', 'r') as f:
            bookings = json.load(f)
    except:
        bookings = []

    # FIX OLD DATA
    for b in bookings:
        if 'price' not in b:
            b['price'] = 0
        if 'worker' not in b:
            b['worker'] = "Not Assigned"
        if 'status' not in b:
            b['status'] = "Pending"
        if 'payment_status' not in b:
            b['payment_status'] = "Pending"

    return render_template('dashboard.html', bookings=bookings)

# Assign Worker
@app.route('/assign/<int:index>', methods=['POST'])
def assign_worker(index):
    worker = request.form['worker']

    with open('bookings.json', 'r') as f:
        data = json.load(f)

    data[index]['worker'] = worker
    data[index]['status'] = "Confirmed"

    with open('bookings.json', 'w') as f:
        json.dump(data, f, indent=4)

    return redirect('/dashboard')

# Payment
@app.route('/pay/<int:index>', methods=['POST'])
def pay(index):

    with open('bookings.json', 'r') as f:
        data = json.load(f)

    data[index]['payment_status'] = "Paid"

    with open('bookings.json', 'w') as f:
        json.dump(data, f, indent=4)

    return redirect('/dashboard')

app.run(debug=True)
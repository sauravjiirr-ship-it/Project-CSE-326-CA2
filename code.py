from flask import Flask, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "rideeasy_2026_secret_key"

DB_NAME = "rideeasy.db"


# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            vehicle TEXT NOT NULL,
            pickup_date TEXT NOT NULL,
            return_date TEXT NOT NULL,
            rental_days INTEGER NOT NULL,
            total_amount INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================================================
# COMMON CSS
# =========================================================

CSS = """
<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial, Helvetica, sans-serif;
}

html{
    scroll-behavior:smooth;
}

body{
    background:#f5f7fb;
    color:#172033;
}

nav{
    background:#111827;
    color:white;
    padding:17px 7%;
    display:flex;
    justify-content:space-between;
    align-items:center;
    position:sticky;
    top:0;
    z-index:1000;
}

.logo{
    font-size:25px;
    font-weight:bold;
    color:#38bdf8;
}

.nav-links{
    display:flex;
    align-items:center;
    gap:20px;
}

.nav-links a{
    color:white;
    text-decoration:none;
    font-size:15px;
}

.nav-links a:hover{
    color:#38bdf8;
}

.user-name{
    color:#38bdf8;
    font-weight:bold;
}

.hero{
    min-height:540px;
    padding:90px 7%;
    background:linear-gradient(135deg,#0f172a,#1d4ed8);
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
}

.hero-content{
    max-width:900px;
}

.hero h1{
    font-size:52px;
    margin-bottom:18px;
}

.hero p{
    font-size:19px;
    line-height:1.6;
    margin-bottom:32px;
    color:#e2e8f0;
}

.search-box{
    background:white;
    padding:18px;
    border-radius:16px;
    display:flex;
    gap:10px;
    max-width:850px;
    margin:auto;
    box-shadow:0 10px 35px rgba(0,0,0,.2);
}

input,
select{
    width:100%;
    padding:13px;
    border:1px solid #dbe1ea;
    border-radius:8px;
    outline:none;
}

input:focus,
select:focus{
    border-color:#2563eb;
}

button{
    border:none;
    background:#2563eb;
    color:white;
    padding:13px 20px;
    border-radius:8px;
    cursor:pointer;
    font-weight:bold;
    transition:.2s;
}

button:hover{
    background:#1d4ed8;
    transform:translateY(-1px);
}

.green-btn{
    background:#16a34a;
}

.green-btn:hover{
    background:#15803d;
}

.red-btn{
    background:#dc2626;
}

section{
    padding:65px 7%;
}

.section-title{
    text-align:center;
    margin-bottom:40px;
}

.section-title h2{
    font-size:32px;
    margin-bottom:10px;
}

.section-title p{
    color:#64748b;
}

.vehicles{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
    gap:25px;
}

.card{
    background:white;
    border-radius:18px;
    padding:25px;
    text-align:center;
    box-shadow:0 7px 25px rgba(0,0,0,.07);
    transition:.25s;
}

.card:hover{
    transform:translateY(-7px);
    box-shadow:0 12px 30px rgba(0,0,0,.12);
}

.vehicle-icon{
    font-size:65px;
    margin-bottom:15px;
}

.card h3{
    margin-bottom:10px;
}

.card p{
    color:#64748b;
    min-height:40px;
}

.price{
    color:#2563eb;
    font-size:21px;
    font-weight:bold;
    margin:18px 0;
}

.booking-box{
    max-width:700px;
    margin:auto;
    background:white;
    padding:32px;
    border-radius:18px;
    box-shadow:0 7px 25px rgba(0,0,0,.08);
}

.form-group{
    margin-bottom:17px;
}

.form-group label{
    display:block;
    margin-bottom:7px;
    font-weight:bold;
}

.booking-box button{
    width:100%;
    margin-top:5px;
}

.confirmation{
    display:none;
    max-width:700px;
    margin:auto;
    background:#dcfce7;
    border:1px solid #86efac;
    color:#166534;
    padding:30px;
    border-radius:18px;
}

.confirmation h2{
    margin-bottom:20px;
}

.confirmation p{
    margin:10px 0;
}

.why-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
    gap:20px;
}

.why-card{
    background:white;
    padding:28px;
    text-align:center;
    border-radius:16px;
    box-shadow:0 5px 20px rgba(0,0,0,.06);
}

.why-card .icon{
    font-size:40px;
    margin-bottom:12px;
}

.why-card p{
    color:#64748b;
    margin-top:8px;
}

footer{
    background:#111827;
    color:white;
    padding:40px 7%;
    text-align:center;
}

footer p{
    color:#cbd5e1;
    margin-top:8px;
}

.auth-page{
    min-height:calc(100vh - 70px);
    display:flex;
    align-items:center;
    justify-content:center;
    padding:40px 20px;
}

.auth-box{
    width:100%;
    max-width:430px;
    background:white;
    padding:35px;
    border-radius:18px;
    box-shadow:0 8px 30px rgba(0,0,0,.1);
}

.auth-box h2{
    text-align:center;
    margin-bottom:10px;
}

.auth-box .subtitle{
    text-align:center;
    color:#64748b;
    margin-bottom:25px;
}

.auth-box input{
    margin-bottom:15px;
}

.auth-box button{
    width:100%;
}

.auth-link{
    text-align:center;
    margin-top:18px;
}

.auth-link a{
    color:#2563eb;
    text-decoration:none;
}

.error{
    background:#fee2e2;
    color:#b91c1c;
    padding:10px;
    border-radius:8px;
    margin-bottom:15px;
    text-align:center;
}

.success{
    background:#dcfce7;
    color:#166534;
    padding:10px;
    border-radius:8px;
    margin-bottom:15px;
    text-align:center;
}

.hidden{
    display:none !important;
}

@media(max-width:700px){

    nav{
        padding:15px 5%;
        flex-direction:column;
        gap:12px;
    }

    .nav-links{
        gap:12px;
        flex-wrap:wrap;
        justify-content:center;
    }

    .hero{
        padding:70px 5%;
    }

    .hero h1{
        font-size:35px;
    }

    .hero p{
        font-size:16px;
    }

    .search-box{
        flex-direction:column;
    }

    section{
        padding:50px 5%;
    }

    .booking-box,
    .auth-box{
        padding:23px;
    }

}

</style>
"""


# =========================================================
# NAVIGATION
# =========================================================

def navigation():

    if "user_id" in session:

        return f"""
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="#vehicles">Vehicles</a>
            <a href="#why">Why Us</a>
            <a href="#contact">Contact</a>
            <span class="user-name">Hi, {session.get("user_name")}</span>
            <a href="/logout">Logout</a>
        </div>
        """

    return """
    <div class="nav-links">
        <a href="/">Home</a>
        <a href="#vehicles">Vehicles</a>
        <a href="#why">Why Us</a>
        <a href="#contact">Contact</a>
        <a href="/login">Login</a>
        <a href="/register">Register</a>
    </div>
    """


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    html = """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>RideEasy - Vehicle Rental Platform</title>

""" + CSS + """

</head>

<body>

<nav>

<div class="logo">
🚗 RideEasy
</div>

""" + navigation() + """

</nav>


<!-- HERO -->

<section class="hero">

<div class="hero-content">

<h1>Rent Your Ride Easily</h1>

<p>
Affordable cars, bikes and scooters for your journey.
Book your perfect vehicle quickly and easily.
</p>

<div class="search-box">

<select id="vehicleType">

<option value="all">
All Vehicles
</option>

<option value="car">
Cars
</option>

<option value="bike">
Bikes
</option>

<option value="scooter">
Scooters
</option>

</select>

<input
type="date"
id="searchDate"
>

<button onclick="searchVehicle()">
Search Vehicle
</button>

</div>

</div>

</section>


<!-- VEHICLES -->

<section id="vehicles">

<div class="section-title">

<h2>Available Vehicles</h2>

<p>
Choose a vehicle according to your journey.
</p>

</div>


<div class="vehicles" id="vehicleList">


<div class="card" data-type="car">

<div class="vehicle-icon">🚘</div>

<h3>Toyota Camry</h3>

<p>
Comfortable premium sedan
</p>

<div class="price">
₹2,500 / day
</div>

<button onclick="openBooking('Toyota Camry',2500)">
Book Now
</button>

</div>


<div class="card" data-type="car">

<div class="vehicle-icon">🚙</div>

<h3>Hyundai Creta</h3>

<p>
Powerful and comfortable SUV
</p>

<div class="price">
₹2,000 / day
</div>

<button onclick="openBooking('Hyundai Creta',2000)">
Book Now
</button>

</div>


<div class="card" data-type="car">

<div class="vehicle-icon">🚙</div>

<h3>Mahindra Thar</h3>

<p>
Adventure ready SUV
</p>

<div class="price">
₹3,000 / day
</div>

<button onclick="openBooking('Mahindra Thar',3000)">
Book Now
</button>

</div>


<div class="card" data-type="bike">

<div class="vehicle-icon">🏍️</div>

<h3>Royal Enfield</h3>

<p>
Classic motorcycle experience
</p>

<div class="price">
₹1,200 / day
</div>

<button onclick="openBooking('Royal Enfield',1200)">
Book Now
</button>

</div>


<div class="card" data-type="bike">

<div class="vehicle-icon">🏍️</div>

<h3>Yamaha R15</h3>

<p>
Sporty performance bike
</p>

<div class="price">
₹1,000 / day
</div>

<button onclick="openBooking('Yamaha R15',1000)">
Book Now
</button>

</div>


<div class="card" data-type="scooter">

<div class="vehicle-icon">🛵</div>

<h3>Honda Activa</h3>

<p>
Easy and economical scooter
</p>

<div class="price">
₹700 / day
</div>

<button onclick="openBooking('Honda Activa',700)">
Book Now
</button>

</div>


</div>

</section>


<!-- BOOKING -->

<section id="booking">

<div class="section-title">

<h2>Book Your Vehicle</h2>

<p>
Enter your details and confirm your booking.
</p>

</div>


<div class="booking-box">

<div class="form-group">

<label>
Customer Name
</label>

<input
type="text"
id="customerName"
placeholder="Enter your name"
>

</div>


<div class="form-group">

<label>
Phone Number
</label>

<input
type="tel"
id="phone"
placeholder="10 digit mobile number"
maxlength="10"
>

</div>


<div class="form-group">

<label>
Selected Vehicle
</label>

<input
type="text"
id="selectedVehicle"
readonly
placeholder="Select a vehicle first"
>

</div>


<div class="form-group">

<label>
Pickup Date
</label>

<input
type="date"
id="pickupDate"
onchange="calculateTotal()"
>

</div>


<div class="form-group">

<label>
Return Date
</label>

<input
type="date"
id="returnDate"
onchange="calculateTotal()"
>

</div>


<div class="form-group">

<label>
Rental Days
</label>

<input
type="number"
id="rentalDays"
value="1"
readonly
>

</div>


<div class="form-group">

<label>
Total Amount
</label>

<input
type="text"
id="totalAmount"
value="₹0"
readonly
>

</div>


<button onclick="confirmBooking()">
Confirm Booking
</button>

</div>

</section>


<!-- CONFIRMATION -->

<section>

<div class="confirmation" id="confirmation">

<h2>
🎉 Booking Confirmed!
</h2>

<p>
<b>Booking ID:</b>
<span id="bookingId"></span>
</p>

<p>
<b>Name:</b>
<span id="confirmName"></span>
</p>

<p>
<b>Phone:</b>
<span id="confirmPhone"></span>
</p>

<p>
<b>Vehicle:</b>
<span id="confirmVehicle"></span>
</p>

<p>
<b>Pickup Date:</b>
<span id="confirmPickup"></span>
</p>

<p>
<b>Return Date:</b>
<span id="confirmReturn"></span>
</p>

<p>
<b>Rental Days:</b>
<span id="confirmDays"></span>
</p>

<p>
<b>Total Amount:</b>
₹<span id="confirmTotal"></span>
</p>

<br>

<button onclick="newBooking()">
Book Another Vehicle
</button>

</div>

</section>


<!-- WHY US -->

<section id="why">

<div class="section-title">

<h2>
Why Choose RideEasy?
</h2>

<p>
Everything you need for a simple rental experience.
</p>

</div>


<div class="why-grid">

<div class="why-card">

<div class="icon">💰</div>

<h3>Affordable</h3>

<p>
Budget-friendly rental prices.
</p>

</div>


<div class="why-card">

<div class="icon">🚗</div>

<h3>Wide Variety</h3>

<p>
Cars, bikes and scooters.
</p>

</div>


<div class="why-card">

<div class="icon">⚡</div>

<h3>Fast Booking</h3>

<p>
Book your ride in seconds.
</p>

</div>


<div class="why-card">

<div class="icon">🔒</div>

<h3>Secure</h3>

<p>
Safe and simple platform.
</p>

</div>

</div>

</section>


<!-- CONTACT -->

<footer id="contact">

<h2>
RideEasy Vehicle Rental
</h2>

<p>
Email: support@rideeasy.com
</p>

<p>
Phone: +91 9876543210
</p>

<br>

<p>
© 2026 RideEasy. All Rights Reserved.
</p>

</footer>


<script>

let selectedPrice = 0;


function openBooking(vehicle, price){

    document.getElementById("selectedVehicle").value = vehicle;

    selectedPrice = price;

    document.getElementById("booking")
        .scrollIntoView({
            behavior:"smooth"
        });

    calculateTotal();
}


function calculateTotal(){

    let pickup =
        document.getElementById("pickupDate").value;

    let returnDate =
        document.getElementById("returnDate").value;


    if(!pickup || !returnDate){

        document.getElementById("rentalDays").value = 1;

        document.getElementById("totalAmount").value =
            "₹" + selectedPrice;

        return;
    }


    let start = new Date(pickup);

    let end = new Date(returnDate);


    let difference =
        Math.ceil(
            (end-start) /
            (1000*60*60*24)
        );


    if(difference < 1){

        difference = 1;

    }


    document.getElementById("rentalDays").value =
        difference;


    document.getElementById("totalAmount").value =
        "₹" + (difference * selectedPrice);

}


function searchVehicle(){

    let type =
        document.getElementById("vehicleType").value;


    let cards =
        document.querySelectorAll(".card");


    cards.forEach(function(card){

        if(
            type === "all" ||
            card.dataset.type === type
        ){

            card.style.display = "block";

        }
        else{

            card.style.display = "none";

        }

    });


    document.getElementById("vehicles")
        .scrollIntoView({
            behavior:"smooth"
        });

}


function confirmBooking(){

    let name =
        document.getElementById("customerName")
        .value.trim();


    let phone =
        document.getElementById("phone")
        .value.trim();


    let vehicle =
        document.getElementById("selectedVehicle")
        .value;


    let pickup =
        document.getElementById("pickupDate")
        .value;


    let returnDate =
        document.getElementById("returnDate")
        .value;


    let days =
        document.getElementById("rentalDays")
        .value;


    let total =
        document.getElementById("totalAmount")
        .value
        .replace("₹","");


    if(
        !name ||
        !phone ||
        !vehicle ||
        !pickup ||
        !returnDate
    ){

        alert("Please fill all booking details.");

        return;

    }


    if(!/^[0-9]{10}$/.test(phone)){

        alert(
            "Please enter a valid 10 digit phone number."
        );

        return;

    }


    if(new Date(returnDate) < new Date(pickup)){

        alert(
            "Return date cannot be before pickup date."
        );

        return;

    }


    let bookingId =
        "RE" +
        Math.floor(
            100000 +
            Math.random()*900000
        );


    document.getElementById("bookingId")
        .innerText = bookingId;


    document.getElementById("confirmName")
        .innerText = name;


    document.getElementById("confirmPhone")
        .innerText = phone;


    document.getElementById("confirmVehicle")
        .innerText = vehicle;


    document.getElementById("confirmPickup")
        .innerText = pickup;


    document.getElementById("confirmReturn")
        .innerText = returnDate;


    document.getElementById("confirmDays")
        .innerText = days;


    document.getElementById("confirmTotal")
        .innerText = total;


    document.querySelector(".booking-box")
        .style.display = "none";


    document.getElementById("confirmation")
        .style.display = "block";


    document.getElementById("confirmation")
        .scrollIntoView({
            behavior:"smooth"
        });

}


function newBooking(){

    location.reload();

}

</script>


</body>
</html>
"""

    return html


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:

            message = "Please fill all fields."

        elif len(password) < 6:

            message = "Password must contain at least 6 characters."

        else:

            try:

                conn = get_db()

                conn.execute(
                    """
                    INSERT INTO users
                    (name,email,password)
                    VALUES (?,?,?)
                    """,
                    (
                        name,
                        email,
                        generate_password_hash(password)
                    )
                )

                conn.commit()
                conn.close()

                return redirect("/login?registered=1")

            except sqlite3.IntegrityError:

                message = "This email is already registered."


    return """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Register - RideEasy</title>

""" + CSS + """

</head>

<body>

<nav>

<div class="logo">
🚗 RideEasy
</div>

<div class="nav-links">

<a href="/">
Home
</a>

<a href="/login">
Login
</a>

</div>

</nav>


<div class="auth-page">

<div class="auth-box">

<h2>
Create Account
</h2>

<p class="subtitle">
Join RideEasy today
</p>

""" + (
    '<div class="error">' + message + '</div>'
    if message else
    ""
) + """

<form method="POST">

<input
type="text"
name="name"
placeholder="Full Name"
required
>

<input
type="email"
name="email"
placeholder="Email Address"
required
>

<input
type="password"
name="password"
placeholder="Password (minimum 6 characters)"
required
>

<button type="submit">
Create Account
</button>

</form>


<div class="auth-link">

Already have an account?

<a href="/login">
Login
</a>

</div>


<div class="auth-link">

<a href="/">
← Back to Home
</a>

</div>

</div>

</div>

</body>
</html>
"""


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""
    success = ""

    if request.args.get("registered") == "1":

        success = "Registration successful. Please login."


    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email=?
            """,
            (email,)
        ).fetchone()

        conn.close()


        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            return redirect("/")


        message = "Invalid email or password."


    return """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Login - RideEasy</title>

""" + CSS + """

</head>

<body>

<nav>

<div class="logo">
🚗 RideEasy
</div>

<div class="nav-links">

<a href="/">
Home
</a>

<a href="/register">
Register
</a>

</div>

</nav>


<div class="auth-page">

<div class="auth-box">

<h2>
Welcome Back
</h2>

<p class="subtitle">
Login to your RideEasy account
</p>

""" + (
    '<div class="success">' + success + '</div>'
    if success else
    ""
) + """

""" + (
    '<div class="error">' + message + '</div>'
    if message else
    ""
) + """

<form method="POST">

<input
type="email"
name="email"
placeholder="Email Address"
required
>

<input
type="password"
name="password"
placeholder="Password"
required
>

<button type="submit">
Login
</button>

</form>


<div class="auth-link">

Don't have an account?

<a href="/register">
Create Account
</a>

</div>


<div class="auth-link">

<a href="/">
← Back to Home
</a>

</div>

</div>

</div>

</body>
</html>
"""


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )

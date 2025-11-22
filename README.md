# 🩸 Blood Bank Donation System
A lightweight, user-friendly web application built using Flask, HTML/CSS, and SQL (MySQL) that helps in managing blood donation, donor registration, blood requests, and request tracking in a simple interface.

# ⭐ Project Overview
The Blood Bank Donation System is designed to simplify the process of donating and requesting blood. It allows donors to register themselves, users to request blood, and admins to manage the availability of blood bags. This system is ideal for educational projects, mini-projects, and basic full-stack hands-on learning.

# 🚀 Features
👤 User Features
->User Registration & Login
->Register as a blood donor
->Request blood by selecting blood group & quantity
->View status of requests
->Cancel pending requests
🧑‍⚕️ Donor Features
->Register as donor
->Update donation details
->View donation facts (optional)
🔧 Admin Features
->View all blood requests
->Approve or reject blood requests
->Manage blood bag availability
->Add dummy data for testing (via SQL)

# 🛠️ Tech Stack
Component	Technology
Backend	Flask: (Python)
Frontend	:HTML, CSS
Database:	MySQL / SQLAlchemy
Tools	Jupyter Notebook: (dummy data), GitHub

#📂 Project Structure
mini-dbms/
│── app.py                    # Main Flask app
│── init.sql                  # MySQL database setup
│── home.html
│── register.html
│── login.html
│── request_blood.html
│── view_requests.html
│── donors.html
│── donate_blood.html
│── style.css                 # Frontend styling
│── dummy_data_adder.ipynb    # Testing data
│── project.txt               # Documentation
│── images/                   # Project images

#🔧 Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/mini-dbms.git
cd mini-dbms
2️⃣ Install Required Packages
pip install flask
pip install mysql-connector-python
3️⃣ Import Database
CREATE DATABASE bloodbank;
4️⃣ Run the Application
python app.py

#🗄️ Database Structure
Tables
 users – stores user credentials
 donors – donor details
 requests – blood requests
 blood_stock (if added) – available blood units
 Database schema included in init.sql
 
#🌱 Future Enhancements
Add SMS/Email notification
Add search for nearby donors
Add admin login with dashboard
Add charts for analytics (donations, availability)
Deploy on Render/Heroku/AWS

#📜 License
This project is for educational and academic use.
Feel free to modify and use it in your college projects.

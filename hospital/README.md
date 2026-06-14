# 🏥 Safe Care Hospital Management System

# 📌 Project Summary

Safe Care Hospital Management System is a full-stack healthcare platform built using **Python Django, Django REST Framework, JWT Authentication, MySQL, HTML, CSS, JavaScript, Bootstrap, Tailwind CSS and REST APIs**.

The system digitizes the complete hospital workflow by providing secure role-based access for Patients, Doctors, and Administrators, enabling appointment scheduling, patient management, prescriptions, laboratory workflows, report management, payment tracking, notifications, and healthcare record management.

This project simulates real-world hospital operations and demonstrates practical implementation of enterprise-level software architecture, secure authentication, database design, API development, workflow automation, and responsive frontend development.

---

# 🎯 Problem Statement

Traditional hospital processes often involve:

Manual appointment booking
Paper-based prescriptions
Difficulty tracking patient history
Delayed communication between doctors and patients
Inefficient report handling
Poor appointment management

Safe Care Hospital solves these problems by providing a centralized digital healthcare platform that streamlines hospital operations and improves communication between patients, doctors, and administrators.

# 🚀 Project Highlights

Key Achievements


✔ Complete Hospital Workflow Automation

✔ Role-Based Authentication & Authorization

✔ JWT Secure Authentication System

✔ RESTful API Development

✔ Dynamic Appointment Scheduling

✔ Smart Slot Availability Management

✔ Double Booking Prevention

✔ Prescription Management System

✔ Laboratory Test Workflow

✔ Medical Report Upload & Management

✔ Automated Notification System

✔ Invoice & Prescription PDF Generation

✔ Payment Tracking System

✔ Responsive Dashboard Design

✔ Scalable Database Architecture



# 🏗 System Architecture


The application follows a layered architecture:

Frontend (HTML, CSS, JavaScript, Bootstrap, Tailwind)

↓

REST API Layer (Django REST Framework)

↓

Business Logic Layer (Django Views)

↓

Authentication Layer (JWT)

↓

Database Layer (MySQL)

↓

Media Storage (Reports, Images, PDFs)


## User Roles

### Admin
Responsible for hospital management operations.

Admin Capabilities

* Approve Doctors
* Manage Departments,Appointments,Payments
* Manage Patients & Hospital Data
* View System Information
* Monitor Operations

### Doctor
Responsible for consultation and patient treatment workflows.

Doctor Capabilities

* Doctor Dashboard
* Profile Management
* View Assigned Appointments
* Accept Appointments
* Reject Appointments
* Reschedule Appointments
* Write Prescriptions
* Request Medical Tests
* View Patient Medical History
* Set availability schedules

### Patient
Responsible for appointment booking and healthcare record management.

Patient Capabilities


* Patient Dashboard
* Profile Management
* Appointment Booking
* View Appointment Status
* Cancel Appointments
* Download Prescriptions
* Upload Medical Reports
* View Reports
* View Test Requests
* Payment History
* Notification Center

---

# 🏥 Department Management

* Create Departments
* Department-wise Doctor Listing
* Dynamic Doctor Filtering
* Doctor Search by Department

Examples:

* Cardiology
* Neurology
* Orthopedics
* Dermatology
* Pediatrics
* General Medicine

---

# 👨‍⚕️ Doctor Management

* Doctor Registration
* Doctor Approval Workflow
* Doctor Profile Image Upload
* Doctor Qualifications
* Specializations
* Experience Tracking
* Consultation Fee Management
* Availability Schedule Management

---

# 📅 Appointment Management

### Patient Side

* Book Appointment
* Select Department
* Select Doctor
* Select Available Slot
* Add Consultation Reason

### Doctor Side

* Accept Appointment
* Reject Appointment
* Reschedule Appointment
* View Appointment Requests

### Smart Slot Management

* Dynamic Slot Generation
* Slot Availability Checking
* Double Booking Prevention
* Automatic Slot Blocking

---

# 📋 Prescription Management

Doctors can:

* Create Prescriptions
* Add Diagnosis
* Add Medicines
* Add Notes

Patients can:

* View Prescriptions
* Download Prescription PDF

---

# 🧪 Laboratory Test Management

Doctors can:

* Request Medical Tests

Patients can:

* View Requested Tests
* Upload Medical Reports
* Access Uploaded Reports

---

# 📁 Medical Report System

Features:

* File Upload Support
* Report Title Management
* Test Request Mapping
* PDF Report Storage
* Report Viewing

---

# 🔔 Notification System

Automated notifications for:

* Appointment Booking
* Appointment Acceptance
* Appointment Rejection
* Appointment Rescheduling

Features:

* Notification Counter
* Notification Dropdown
* Patient Notification Dashboard

---

# 💳 Payment Management

Features:

* Appointment Payment Tracking
* Payment History
* Invoice Generation
* Invoice PDF Download

---

# 📄 PDF Generation

System generates:

* Prescription PDF
* Payment Invoice PDF

---

# 📊 Dashboards

### Patient Dashboard

Displays:

* Profile Information
* Appointments
* Prescriptions
* Test Requests
* Reports
* Payment History
* Notifications

### Doctor Dashboard

Displays:

* Profile Information
* Appointment Requests
* Accepted Appointments
* Patient Information
* Prescription Management
* Test Request Management

---

# 🗄 Database Design

Major Models:

* User
* Profile
* PatientProfile
* DoctorProfile
* Department
* Appointment
* Prescription
* TestRequest
* MedicalReport
* Payment
* Notification

Relationships implemented using:

* OneToOneField
* ForeignKey
* Reverse Relations
* Related Names

---

# 🛠 Technology Stack

## Backend

* Python
* Django
* Django REST Framework
* JWT Authentication
* MySQL

## Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap 5
* Tailwind CSS

## Database

* MySQL

## API Testing

* Postman

## Authentication

* Simple JWT

## File Handling

* Django Media Storage

---

# 🔄 Complete Appointment Workflow

Step 1 — Patient Registration

A patient creates an account through the registration module.

The system:

Creates user credentials
Stores profile information
Creates Patient Profile
Step 2 — Patient Login

The patient logs in using JWT Authentication.

The system generates:

Access Token
Refresh Token

These tokens secure all future API requests.

Step 3 — Doctor Selection

Patient:

Selects Department
Selects Doctor

The system dynamically loads doctors based on department selection.

Step 4 — Slot Availability Check

The system:

Reads doctor availability schedule
Generates available slots
Removes already booked slots
Prevents duplicate appointments

Only available slots are displayed.

Step 5 — Appointment Booking

Patient submits:

Doctor
Date
Time
Consultation Reason

The system:

Validates data
Verifies slot availability
Creates appointment
Generates notification

Appointment Status:

Pending

Step 6 — Doctor Reviews Appointment

Doctor views appointment request.

Available actions:

Accept
Reject
Reschedule
Step 7A — Appointment Accepted

System:

Updates appointment status
Creates notification

Patient receives:

"Your appointment has been accepted."

Step 7B — Appointment Rejected

System:

Updates appointment status
Generates notification

Patient receives:

"Your appointment has been rejected."

Step 7C — Appointment Rescheduled

Doctor selects:

New Date
New Time

System stores:

Old Appointment Date
Old Appointment Time
New Appointment Date
New Appointment Time

Patient receives:

"Your appointment has been rescheduled."

Step 8 — Consultation

Doctor conducts consultation.

Doctor can:

Review patient history
View uploaded reports
Analyze previous records
Step 9 — Prescription Generation

Doctor creates:

Diagnosis
Medicines
Notes

System stores prescription.

Patient can:

View prescription
Download PDF prescription
Step 10 — Laboratory Test Request

Doctor may request:

Blood Test
Scan
Medical Examination

System creates Test Request.

Patient can view requested tests from dashboard.

Step 11 — Report Upload

Patient uploads:

Test Results
Medical Reports
Laboratory Documents

System:

Stores files securely
Links reports to test requests
Step 12 — Payment Processing

Patient completes payment.

System stores:

Payment Details
Amount
Status
Date

Invoice is generated.

Step 13 — Invoice Generation

System generates downloadable PDF invoice.

Patient can:

View payment history
Download invoice anytime
Step 14 — Notification System

Notifications are automatically generated for:

Appointment Booking
Appointment Acceptance
Appointment Rejection
Appointment Rescheduling

Patients can view notifications from dashboard.

# 📊 Major Modules

Authentication Module

Register
Login
Logout
JWT Tokens
Role Verification

Doctor Module

Doctor Registration
Doctor Approval
Availability Management
Appointment Management

Patient Module

Profile Management
Appointment Booking
Report Upload
Prescription Access

Appointment Module

Dynamic Slots
Double Booking Prevention
Status Tracking
Rescheduling

Prescription Module

Diagnosis
Medicines
Notes
PDF Download

Laboratory Module

Test Requests
Report Uploads
Report Viewing

Payment Module

Payment Tracking
Invoice Generation
Payment History

Notification Module

Automated Notifications
Notification Counter
Notification Dashboard

# 🛠 Technical Skills Demonstrated

This project demonstrates practical experience in:

Python Development
Django Framework
Django REST Framework
REST API Development
JWT Authentication
MySQL Database Design
Role-Based Access Control
CRUD Operations
File Upload Handling
PDF Generation
Healthcare Workflow Automation
Frontend Integration
API Security
Database Relationships
Full Stack Development
Software Architecture Design
Real World Business Logic Implementation

# 📂 Project Structure

```text
SafeCareHospital/
│
├── backend/
│   ├── authentication/
│   ├── media/
│   ├── templates/
│   ├── manage.py
│
├── frontend/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── patient-dashboard.html
│   ├── doctor-dashboard.html
│   ├── payment.html
│   ├── CSS Files
│   ├── JS Files
│
└── README.md
```

# ⚙ Installation

## Clone Repository

```bash
git clone <repository-url>
```

```bash
cd SafeCareHospital
```

# Create Virtual Environment

```bash
python -m venv venv
```

# Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

# Install Dependencies

```bash
pip install -r requirements.txt
```

# Configure Database

Update settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'safecare',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

# Apply Migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

# Create Superuser

```bash
python manage.py createsuperuser
```

# Run Server

```bash
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8001
```

Frontend:

Run using VS Code Live Server

```text
http://127.0.0.1:5500
```

# API Endpoints

Examples:

```text
/auth/register/
/auth/login/
/auth/logout/

/auth/appointments/book/
/auth/appointments/my/

/auth/patient/profile/
/auth/patient/reports/

/auth/doctor/dashboard/

/auth/payments/history/

/auth/patient/notifications/
```

# Future Enhancements

* Real-Time Chat System
* WebSocket Integration
* Video Consultation
* SMS Notifications
* Doctor Ratings & Reviews
* AI Symptom Checker
* Medical Insurance Integration
* Appointment Reminder System

# Learning Outcomes

This project demonstrates practical experience in:

* Django Development
* REST API Development
* Authentication & Authorization
* Database Design
* CRUD Operations
* Role-Based Access Control
* File Upload Management
* PDF Generation
* Healthcare Workflow Automation
* Full Stack Development
* Real World Software Architecture

# 📈 Keywords

Python Developer

Django Developer

Backend Developer

Full Stack Developer

REST API Developer

Healthcare Software

Hospital Management System

JWT Authentication

Role Based Access Control

MySQL

Django REST Framework

API Integration

Software Engineer

Web Application Development

Database Design

Business Workflow Automation

Enterprise Application Development

Scalable System Design

# 🏁 Conclusion

Safe Care Hospital Management System is a comprehensive healthcare management platform that digitizes the entire patient-doctor interaction lifecycle. The project showcases practical implementation of secure authentication, appointment automation, healthcare record management, payment processing, report handling, notification systems, and scalable REST API architecture.

It demonstrates the ability to design and develop production-style business applications using modern full-stack development practices and real-world software engineering principles.

# Author

**Muhamed Shafaan**

Python Django Developer | Full Stack Developer

Focused on building scalable web applications, REST APIs, healthcare platforms, business automation systems, and enterprise software solutions.



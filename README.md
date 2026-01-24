# 🏥 Qurexa – Healthcare 




<img width="1916" height="961" alt="image" src="https://github.com/user-attachments/assets/0bfceda7-7fd3-4cde-a67c-96c32562e03b" />


## 📌 Project Overview

**Qurexa** is a full-stack **Healthcare Management System** built using **Python and Django**, designed to digitize and streamline patient–doctor workflows.

- Manages appointments, clinical records, and visit history
- Supports role-based access for patients and doctors
- Integrates AI-assisted clinical summaries
- Deployed in a production environment using **PythonAnywhere**

---

## 🌐 Live Application

- 🔗 https://rohit1239tech.pythonanywhere.com

## 💻 GitHub Repository

- 🔗 https://github.com/rohit1239-tech/Qurexa-Healthcare

---

## 🎯 Problem Statement

Manual healthcare workflows often lead to:

- Inefficient appointment handling
- Fragmented patient records
- Poor clinical history tracking

**Qurexa solves this by:**

- Centralizing healthcare data
- Providing secure, role-based access
- Maintaining structured and searchable visit records

---

## 🚀 Key Features

### 🔐 Authentication & Authorization

- Role-based authentication system:
  - Patient
  - Doctor
  - Admin
- Secure login using Django Authentication
- OTP-based patient signup verification
- Password hashing and session management
- CSRF protection enabled

---

### 🧑‍⚕️ Doctor Module

- View assigned patient appointments
- Mark appointments as **Completed**
- Write and update clinical notes
- View complete patient visit history
- Generate AI-assisted clinical summaries
- Controlled access to patient data

---

### 🧑‍🦱 Patient Module

- Book appointments with doctors
- View appointment status:
  - Pending
  - Completed
- Access visit history and doctor reports
- Read AI-generated summaries for better understanding
- Read-only access to clinical records

---

### 📋 Clinical Records Management

- Structured visit records linked to appointments
- Clear separation of:
  - Current visit
  - Previous visits
  - Manual doctor reports
  - AI-assisted clinical summaries
- Secure access based on user role

---

### ⚙️ System Capabilities

- Modular Django app-based architecture
- Django ORM for database operations
- Production-ready configuration
- Clean and responsive UI using HTML & CSS

---

## 🛠️ Tech Stack

### Backend
- Python
- Django
- Django ORM

### Frontend
- HTML5
- CSS3

### Database
- SQLite

### AI Integration
- Custom AI service for clinical summary generation

### Deployment & DevOps
- PythonAnywhere
- WSGI configuration
- Production Django settings (`DEBUG = False`)

### Version Control
- Git
- GitHub (SSH-based workflow)

---


## 🗂️ Project Structure

```text
Qurexa-Healthcare/
│
├── Qurexa/                # Project settings, URLs, WSGI/ASGI
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── users/                 # Authentication & roles
├── patients/              # Patient module
├── doctors/               # Doctor module
├── appointments/          # Appointment management
├── records/               # Clinical visit records
├── ai_engine/             # AI summary services
│
├── templates/             # HTML templates
├── static/                # Static assets
│
├── manage.py              # Django entry point
├── requirements.txt       # Dependencies
└── README.md              # Documentation

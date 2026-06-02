# Real Authentication in Django & React 🚀

A complete, production-ready full-stack authentication system built with **Django REST Framework (Backend)** and **React (Frontend)**. This project serves as a robust starting point for SaaS platforms, featuring JWT-based authentication, secure routing, and a complete password recovery flow using email OTPs.

## ✨ Features

* **JWT Authentication:** Secure login and session management using Access and Refresh tokens.
* **User Registration:** Clean account creation flow.
* **Password Recovery Flow:** * Forgot Password (OTP sent to registered email)
  * Verify OTP
  * Secure Password Reset
* **Protected Routes:** Frontend route guards to restrict access to authenticated users only.
* **Global Auth State:** React Context API (`AuthContext`) for seamless user state management across the application.
* **Modern UI/UX:** Fully responsive design built with **Tailwind CSS**, featuring smooth page transitions and component animations via **Framer Motion**.
* **Smart API Handling:** Configured Axios interceptors for automatic token management and error handling.

---

## 🛠️ Tech Stack

**Frontend:**
* React.js (Vite / Create React App)
* React Router DOM (Navigation)
* Tailwind CSS (Styling)
* Framer Motion (Animations)
* Axios (HTTP Client)

**Backend:**
* Python / Django
* Django REST Framework (DRF)
* SimpleJWT (Token management)
* Django-CORS-Headers
---
## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### Prerequisites

* Django and npm installed
* Python 3.8+ installed
* Git

### 1. Backend Setup (Django)

1. **Navigate to your backend directory:**
   ```bash
   cd backend

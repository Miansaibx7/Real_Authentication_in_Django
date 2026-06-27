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
* **🐳 Docker Support:** Ready-to-use Docker configuration for easy deployment and development.

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
* Django-Ratelimit (Rate limiting)

**DevOps:**
* Docker & Docker Compose
* uv (Python package manager)
* SQLite (Development) / PostgreSQL (Production)
  
---
## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### Prerequisites

* Python 3.13+ installed
* Node.js and npm installed
* Git installed
* Docker & Docker Compose (optional, for containerized setup)

### 🐳 Running with Docker (Recommended)
The easiest way to run the project is using Docker. We have a pre-built image available on Docker Hub.

** Quick Start with Docker
*Clone the repository
bash
'git clone https://github.com/Miansaibx7/Real_Authentication_in_Django.git'
'cd Real_Authentication_in_Django'

** Create a .env file

bash
cp .env.example .env
Update the .env file with your own values (SECRET_KEY, email credentials, etc.).

### Run with Docker Compose

bash
docker compose up
The application will be available at: http://localhost:8000

## Using the Pre-built Docker Image
If you want to use the pre-built image directly without cloning the repository:

bash
# Pull the image
'docker pull miansaibx8/real_authentication_in_django:latest'

# Create a docker-compose.yml file (or use the one from the repo)
docker-compose.yml example:
yaml
services:
  web:
    image: miansaibx8/real_authentication_in_django:latest
    container_name: saas_web
    ports:
      - "8000:8000"
    volumes:
      - ./config/db.sqlite3:/app/config/db.sqlite3
    env_file:
      - .env
    environment:
      - DEBUG=${DEBUG:-True}
      - DJANGO_SETTINGS_MODULE=config.settings
    command: ["python", "config/manage.py", "runserver", "0.0.0.0:8000"]
    
** Docker Commands **
bash
# Build the image locally
docker compose build

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Stop the container
docker compose down

# Run migrations
docker compose exec web python config/manage.py migrate

# Create a superuser
docker compose exec web python config/manage.py createsuperuser

# Access the container shell
docker compose exec web bash
Building Your Own Docker Image
Build the image

bash
docker build -t yourusername/real_authentication_in_django:latest .
Tag and push to Docker Hub

bash
docker tag yourusername/real_authentication_in_django:latest yourusername/real_authentication_in_django:latest
docker push yourusername/real_authentication_in_django:latest
💻 Traditional Setup (Without Docker)

### Backend Setup (Django)
Navigate to the backend directory

bash
cd backend
Create a virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies using uv

bash
pip install uv
uv sync
Set up environment variables
Create a .env file in the config/ directory with:

env
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
Run migrations

bash
python config/manage.py migrate
Create a superuser

bash
python config/manage.py createsuperuser
Start the Django development server

bash
python config/manage.py runserver
Access the backend API

API Endpoint: http://127.0.0.1:8000/api/auth/

Admin Panel: http://127.0.0.1:8000/admin/

📁 Project Structure
text
SaaS/
├── config/
│   ├── authenticator/      # Authentication app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── dashboard/          # Dashboard app
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── config/             # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── db.sqlite3          # SQLite database
│   └── manage.py
├── .env                    # Environment variables
├── Dockerfile              # Docker build configuration
├── docker-compose.yml      # Docker Compose configuration
├── pyproject.toml          # Python dependencies (uv)
└── README.md

## 🐛 Common Issues & Solutions
Docker: ModuleNotFoundError: No module named 'dotenv'
Solution: The Dockerfile now includes RUN uv add python-dotenv to ensure it's installed.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

** 📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

** 📧 Contact
Mian Muhammad Waqas
GitHub: @Miansaibx7
Email: mianmwaqas77@gmail.com

##⭐ Show Your Support
If you found this project helpful, please give it a ⭐ on GitHub!
Happy Coding! 🚀

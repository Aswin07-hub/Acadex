
import requests

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Backend URL
BASE_URL = "http://127.0.0.1:8001/"


# ==========================================
# LOGIN PAGE
# ==========================================

def login_page(request):

    message = ""
    success = False

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        role = request.POST.get("role", "").strip()

        session = requests.Session()

        try:
            csrf_response = session.get(
                BASE_URL + "api/csrf/",
                timeout=10
            )

            csrf_token = session.cookies.get("csrftoken")

            if not csrf_response.ok or not csrf_token:
                message = "Unable to connect to backend CSRF service."

            else:
                response = session.post(
                    BASE_URL + "api/login/",
                    json={
                        "username": username,
                        "password": password,
                        "role": role
                    },
                    headers={
                        "X-CSRFToken": csrf_token,
                        "Referer": BASE_URL
                    },
                    timeout=10
                )

                result = response.json()

                message = result.get("message", "Login failed")
                success = result.get("success", False)

        except requests.RequestException:
            message = "Backend server is not running. Please start it."

        except ValueError:
            message = "Invalid response received from backend."

    return render(request, "login.html", {
        "message": message,
        "success": success
    })


# ==========================================
# REGISTER PAGE
# ==========================================

def register_page(request):

    message = ""
    success = False

    if request.method == "POST":

        data = {
            "first_name": request.POST.get("first_name", "").strip(),
            "last_name": request.POST.get("last_name", "").strip(),
            "username": request.POST.get("username", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "phone": request.POST.get("phone", "").strip(),
            "date_of_birth": request.POST.get("date_of_birth", "").strip(),
            "address": request.POST.get("address", "").strip(),
            "register_number": request.POST.get("register_number", "").strip(),
            "department": request.POST.get("department", "").strip(),
            "course": request.POST.get("course", "").strip(),
            "year": request.POST.get("year", "").strip(),
            "section": request.POST.get("section", "").strip(),
            "password": request.POST.get("password", ""),
            "confirm_password": request.POST.get("confirm_password", "")
        }

        session = requests.Session()

        try:
            csrf_response = session.get(
                BASE_URL + "api/csrf/",
                timeout=10
            )

            csrf_token = session.cookies.get("csrftoken")

            if not csrf_response.ok or not csrf_token:
                message = "Unable to get CSRF token from backend."

            else:
                response = session.post(
                    BASE_URL + "api/register/",
                    json=data,
                    headers={
                        "X-CSRFToken": csrf_token,
                        "Referer": BASE_URL
                    },
                    timeout=10
                )

                result = response.json()

                message = result.get("message", "Registration failed")
                success = result.get("success", False)

        except requests.RequestException:
            message = "Backend server is not running. Please start it."

        except ValueError:
            message = "Invalid response received from backend."

    return render(request, "register.html", {
        "message": message,
        "success": success
    })


# ==========================================
# STUDENT DASHBOARD
# ==========================================

# @login_required
def student_dashboard(request):

    context = {
        "total_documents": 0,
        "approved_documents": 0,
        "pending_documents": 0,
        "rejected_documents": 0,
        "documents": [],
        "events": [],
        "notifications": [],
    }

    return render(request, "student_dashboard.html", context)


# ==========================================
# DOCUMENT UPLOAD
# ==========================================

def upload_document(request):

    if request.method == "POST":
        return redirect("student_dashboard")

    return redirect("student_dashboard")

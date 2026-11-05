import requests

from django.shortcuts import render, redirect
from django.contrib.auth import logout


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
            # Get backend CSRF token
            csrf_response = session.get(
                BASE_URL + "api/csrf/",
                timeout=10
            )

            csrf_token = session.cookies.get("csrftoken")

            if not csrf_response.ok or not csrf_token:
                message = "Unable to connect to backend CSRF service."

            else:
                # Backend login
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

                if success:

                    request.session["student_username"] = username
                    request.session["user_role"] = role

                    request.session["backend_sessionid"] = (
                        session.cookies.get("sessionid")
                    )

                    request.session["backend_csrftoken"] = (
                        session.cookies.get("csrftoken")
                    )

                    request.session.save()

                    print("BACKEND SESSION RECEIVED:",
                          bool(request.session.get("backend_sessionid")))

                    print("BACKEND CSRF RECEIVED:",
                          bool(request.session.get("backend_csrftoken")))

                    print("FRONTEND SESSION KEY:",
                          request.session.session_key)

                    return redirect("student_dashboard")

        except requests.RequestException as error:
            print("LOGIN ERROR:", error)
            message = "Backend server is not running."

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
            message = "Backend server is not running."

        except ValueError:
            message = "Invalid response received from backend."

    return render(request, "register.html", {
        "message": message,
        "success": success
    })


# ==========================================
# STUDENT DASHBOARD
# ==========================================
def student_dashboard(request):

    username = request.session.get("student_username")

    if not username:
        return redirect("login_page")

    profile = {}

    try:
        response = requests.get(BASE_URL, timeout=10)

        if response.ok:
            result = response.json()

            if result.get("success"):
                students = result.get("students", [])

                profile = next(
                    (
                        student for student in students
                        if student.get("username") == username
                    ),
                    {}
                )

    except requests.RequestException:
        profile = {}

    context = {
        "username": username,
        "profile": profile,
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

    if not request.session.get("student_username"):
        return redirect("login")

    if request.method == "POST":
        # Actual backend document upload will be connected here.
        return redirect("student_dashboard")

    return redirect("student_dashboard")


# ==========================================
# LOGOUT
# ==========================================

def logout_page(request):

    request.session.flush()

    return redirect("login_page")
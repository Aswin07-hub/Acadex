
import requests

from django.shortcuts import render, redirect


BASE_URL = "http://127.0.0.1:8001/"


def get_backend_cookies(request):
    return {
        "sessionid": request.session.get("backend_sessionid"),
        "csrftoken": request.session.get("backend_csrf_token"),
    }


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

                if success:

                    request.session["student_username"] = username
                    request.session["user_role"] = role

                    request.session["backend_sessionid"] = (
                        session.cookies.get("sessionid")
                    )

                    request.session["backend_csrf_token"] = (
                        session.cookies.get("csrftoken")
                    )

                    if role == "HOD":
                        return redirect("hod_requests_page")

                    if role == "STUDENT":
                        return redirect("student_dashboard")

        except requests.RequestException:
            message = "Backend server is not running."

        except ValueError:
            message = "Invalid response received from backend."

    return render(
        request,
        "login.html",
        {
            "message": message,
            "success": success
        }
    )


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

                message = result.get(
                    "message",
                    "Registration failed"
                )

                success = result.get("success", False)

        except requests.RequestException:
            message = "Backend server is not running."

        except ValueError:
            message = "Invalid response received from backend."

    return render(
        request,
        "register.html",
        {
            "message": message,
            "success": success
        }
    )


# ==========================================
# STUDENT DASHBOARD
# ==========================================

def student_dashboard(request):

    username = request.session.get("student_username")

    if not username:
        return redirect("login_page")

    if request.session.get("user_role") != "STUDENT":
        return redirect("login_page")

    context = {
        "username": username,
        "total_documents": 0,
        "approved_documents": 0,
        "pending_documents": 0,
        "rejected_documents": 0,
        "documents": [],
        "events": [],
        "notifications": [],
        "hod_requests": [],
        "dashboard_error": "",
        "upload_success_message": request.session.pop(
            "upload_success_message",
            ""
        ),
    }

    cookies = get_backend_cookies(request)

    if not cookies["sessionid"]:
        context["dashboard_error"] = (
            "Your backend session has expired. Please login again."
        )

        return render(
            request,
            "student_dashboard.html",
            context
        )

    try:
        response = requests.get(
            BASE_URL + "api/submission-requests/",
            cookies=cookies,
            timeout=20
        )

        result = response.json()

        if response.ok and result.get("success"):
            context["hod_requests"] = result.get("requests", [])

        else:
            context["dashboard_error"] = result.get(
                "message",
                "Unable to load HOD submission requests."
            )

    except requests.RequestException:
        context["dashboard_error"] = (
            "Unable to connect to backend server."
        )

    except ValueError:
        context["dashboard_error"] = (
            "Invalid response received from backend."
        )

    return render(
        request,
        "student_dashboard.html",
        context
    )


# ==========================================
# LOGOUT
# ==========================================

def logout_page(request):

    request.session.flush()

    return redirect("login_page")

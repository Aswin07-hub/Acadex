
import requests

from django.shortcuts import render


# Backend URL
BASE_URL = "http://127.0.0.1:8001/"


# ==========================================
# STUDENT PROFILE
# ==========================================

def student_profile(request):

    message = ""
    success = False

    profile = {
        "first_name": "",
        "last_name": "",
        "username": "",
        "email": "",
        "register_number": "",
        "department": "",
        "course": "",
        "year": "",
        "section": "",
        "phone": "",
        "date_of_birth": "",
        "address": "",
        "profile_photo": ""
    }

    if request.method == "POST":

        data = {
            "first_name": request.POST.get("first_name", "").strip(),
            "last_name": request.POST.get("last_name", "").strip(),
            "username": request.POST.get("username", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "register_number": request.POST.get("register_number", "").strip(),
            "department": request.POST.get("department", "").strip(),
            "course": request.POST.get("course", "").strip(),
            "year": request.POST.get("year", "").strip(),
            "section": request.POST.get("section", "").strip(),
            "phone": request.POST.get("phone", "").strip(),
            "date_of_birth": request.POST.get("date_of_birth", "").strip(),
            "address": request.POST.get("address", "").strip()
        }

        profile.update(data)

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
                    BASE_URL + "api/student-profile/",
                    json=data,
                    headers={
                        "X-CSRFToken": csrf_token,
                        "Referer": BASE_URL
                    },
                    timeout=10
                )

                result = response.json()

                message = result.get(
                    "message", "Unable to update student profile."
                )

                success = result.get("success", False)

                if success:
                    profile.update(result.get("profile", {}))

        except requests.RequestException:
            message = "Backend server is not running. Please start it."

        except ValueError:
            message = "Invalid response received from backend."

    return render(request, "student_profile.html", {
        "profile": profile,
        "message": message,
        "success": success
    })

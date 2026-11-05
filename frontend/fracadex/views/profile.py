
import requests
from django.shortcuts import render, redirect

BASE_URL = "http://127.0.0.1:8001/"


def student_profile(request):

    username = request.session.get("student_username")

    print("LOGGED-IN USERNAME:", username)

    if not username:
        return redirect("login_page")

    profile = {}
    message = ""
    success = False

    backend_session = requests.Session()

    # Backend authentication cookie
    backend_session.cookies.set(
        "sessionid",
        request.session.get("backend_sessionid") or "",
        domain="127.0.0.1",
        path="/"
    )

    # Backend CSRF cookie
    csrf_token = request.session.get("backend_csrftoken") or ""

    backend_session.cookies.set(
        "csrftoken",
        csrf_token,
        domain="127.0.0.1",
        path="/"
    )

    try:

        # FETCH PROFILE
        response = backend_session.get(
            BASE_URL + "api/student-profile/",
            timeout=10
        )

        print("FETCH STATUS:", response.status_code)

        result = response.json()

        if response.ok and result.get("success"):
            profile = result.get("profile", {})
            print("MATCHED PROFILE:", profile)
        else:
            message = result.get(
                "message",
                "Unable to fetch student profile."
            )

        # UPDATE PROFILE
        if request.method == "POST":

            data = {
                "first_name": request.POST.get("first_name", "").strip(),
                "last_name": request.POST.get("last_name", "").strip(),
                "email": request.POST.get("email", "").strip(),
                "phone": request.POST.get("phone", "").strip(),
                "date_of_birth": request.POST.get("date_of_birth", "").strip(),
                "address": request.POST.get("address", "").strip()
            }

            headers = {
                "X-CSRFToken": csrf_token,
                "Referer": BASE_URL + "api/student-profile/"
            }

            update_response = backend_session.post(
                BASE_URL + "api/student-profile/",
                json=data,
                headers=headers,
                timeout=10
            )

            print("UPDATE STATUS:", update_response.status_code)
            print("UPDATE RESPONSE:", update_response.text)

            update_result = update_response.json()

            if update_response.ok and update_result.get("success"):

                success = True
                message = "Profile updated successfully."
                profile = update_result.get("profile", {})

            else:
                message = update_result.get(
                    "message",
                    "Unable to update profile."
                )

    except requests.RequestException as error:

        print("REQUEST ERROR:", error)
        message = "Unable to connect to backend server."

    except ValueError:

        message = "Invalid response received from backend."

    return render(request, "student_profile.html", {
        "profile": profile,
        "username": username,
        "message": message,
        "success": success
    })

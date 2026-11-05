
import requests

from django.shortcuts import render, redirect


BASE_URL = "http://127.0.0.1:8001/"


# ==========================================
# HOD SUBMISSION REQUESTS PAGE
# ==========================================

def hod_requests_page(request):

    # Check whether the user is logged in
    username = request.session.get("student_username")

    if not username:
        return redirect("login_page")

    # Check HOD role
    user_role = str(
        request.session.get("user_role", "")
    ).strip().upper()
    print("DEBUG USERNAME:", request.session.get("student_username"))
    print("DEBUG USER ROLE:", repr(request.session.get("user_role")))
    print("DEBUG NORMALIZED ROLE:", repr(user_role))

    if user_role != "HOD":
        return redirect("student_dashboard")

    # Get backend authentication cookies
    backend_sessionid = request.session.get("backend_sessionid")
    backend_csrf_token = request.session.get("backend_csrf_token")

    if not backend_sessionid or not backend_csrf_token:
        return redirect("login_page")

    cookies = {
        "sessionid": backend_sessionid,
        "csrftoken": backend_csrf_token
    }

    headers = {
        "X-CSRFToken": backend_csrf_token,
        "Referer": BASE_URL
    }

    message = ""
    requests_list = []

    # ==========================================
    # CREATE SUBMISSION REQUEST
    # ==========================================

    if request.method == "POST":

        data = {
            "title": request.POST.get("title", "").strip(),
            "document_type": request.POST.get("document_type", "").strip(),
            "description": request.POST.get("description", "").strip(),
            "deadline": request.POST.get("deadline", "").strip()
        }

        try:

            response = requests.post(
                BASE_URL + "api/submission-requests/",
                json=data,
                cookies=cookies,
                headers=headers,
                timeout=30
            )

            result = response.json()

            if result.get("success"):
                return redirect("hod_requests_page")

            message = result.get(
                "message",
                "Unable to create submission request."
            )

        except requests.RequestException:

            message = "Unable to connect to backend server."

        except ValueError:

            message = "Invalid response received from backend."

    # ==========================================
    # FETCH EXISTING SUBMISSION REQUESTS
    # ==========================================

    try:

        response = requests.get(
            BASE_URL + "api/submission-requests/",
            cookies=cookies,
            timeout=30
        )

        result = response.json()

        if result.get("success"):

            requests_list = result.get("requests", [])

        else:

            message = result.get(
                "message",
                "Unable to load submission requests."
            )

    except requests.RequestException:

        message = "Unable to connect to backend server."

    except ValueError:

        message = "Invalid response received from backend."

    # ==========================================
    # PAGE CONTEXT
    # ==========================================

    document_types = [
        ("ASSIGNMENT", "Assignment"),
        ("GROUP_PROJECT", "Group Project Report"),
        ("MINI_PROJECT", "Mini Project Report"),
        ("FINAL_PROJECT", "Final Year Project"),
        ("SEMINAR", "Seminar Report"),
        ("INTERNSHIP", "Internship Report"),
        ("INDUSTRIAL_VISIT", "Industrial Visit Report"),
        ("RESEARCH", "Research Paper"),
        ("OTHER", "Other Academic Work"),
    ]

    context = {
        "username": username,
        "message": message,
        "requests_list": requests_list,
        "document_types": document_types,
    }

    return render(
        request,
        "hod_requests.html",
        context
    )

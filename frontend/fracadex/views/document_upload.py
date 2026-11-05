
import requests

from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import get_template


# Backend API URL
BASE_URL = "http://127.0.0.1:8001/"


# Document types matching the backend Document model
DOCUMENT_TYPES = [
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


def get_backend_cookies(request):
    return {
        "sessionid": request.session.get("backend_sessionid"),
        "csrftoken": request.session.get("backend_csrf_token"),
    }


def upload_document(request):

    print("\n========== ACADEX UPLOAD VIEW ==========")
    print("NEW DOCUMENT UPLOAD VIEW IS RUNNING")

    # Check student login
    username = request.session.get("student_username")
    role = request.session.get("user_role")

    if not username or role != "STUDENT":
        messages.error(request, "Please login as a student first.")
        return redirect("login_page")

    # Get optional HOD submission request ID
    submission_request_id = (
        request.GET.get("request_id")
        or request.POST.get("submission_request_id")
    )

    selected_request = None
    error_message = None

    cookies = get_backend_cookies(request)

    # Load selected HOD request, if applicable
    if submission_request_id:

        try:
            response = requests.get(
                BASE_URL + "api/submission-requests/",
                cookies=cookies,
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()

                if data.get("success"):

                    for item in data.get("requests", []):

                        if str(item.get("id")) == str(submission_request_id):
                            selected_request = item
                            break

                if not selected_request:
                    error_message = (
                        "The selected HOD submission request was not found."
                    )

            else:
                error_message = (
                    "Unable to load the selected submission request."
                )

        except requests.RequestException:
            error_message = (
                "Unable to connect to the backend server."
            )

    # Process document upload
    if request.method == "POST":

        document_type = request.POST.get("document_type")
        title = request.POST.get("title", "").strip()
        uploaded_file = request.FILES.get("file")

        if not document_type or not title or not uploaded_file:

            error_message = (
                "Please fill in all fields and select a file."
            )

        elif document_type not in [
            item[0] for item in DOCUMENT_TYPES
        ]:

            error_message = "Please select a valid document type."

        elif (
            not cookies.get("sessionid")
            or not cookies.get("csrftoken")
        ):

            error_message = (
                "Your backend login session has expired. "
                "Please login again."
            )

        else:

            upload_data = {
                "document_type": document_type,
                "title": title,
            }

            # Link the document to an HOD request when provided
            if submission_request_id:
                upload_data["submission_request_id"] = (
                    submission_request_id
                )

            headers = {
                "X-CSRFToken": cookies["csrftoken"],
                "Referer": BASE_URL,
            }

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    uploaded_file.content_type
                )
            }

            try:

                response = requests.post(
                    BASE_URL + "api/documents/upload/",
                    data=upload_data,
                    files=files,
                    cookies=cookies,
                    headers=headers,
                    timeout=30
                )

                try:
                    result = response.json()
                except ValueError:
                    result = {}

                if (
                    response.status_code in [200, 201]
                    and result.get("success")
                ):

                    request.session["upload_success_message"] = (
                        "Document submitted successfully! "
                        "Your HOD will review it."
                    )

                    return redirect("student_dashboard")

                else:

                    error_message = result.get(
                        "message",
                        "Document upload failed. Please try again."
                    )

            except requests.RequestException:

                error_message = (
                    "Unable to connect to the backend server. "
                    "Please check whether the backend is running."
                )

    # Template context
    context = {
        "document_types": DOCUMENT_TYPES,
        "selected_request": selected_request,
        "submission_request_id": submission_request_id,
        "message": error_message,
    }

    # Check which template Django is loading
    template = get_template("document_upload.html")

    print("TEMPLATE LOADED FROM:", template.origin.name)
    print("========================================\n")

    # IMPORTANT: Pass the template NAME, not the Template object
    return render(
        request,
        "document_upload.html",
        context
    )

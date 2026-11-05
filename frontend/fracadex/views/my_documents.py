
import requests

from django.shortcuts import render, redirect


BASE_URL = "http://127.0.0.1:8001/"


def get_backend_cookies(request):
    """
    Get the backend Django session and CSRF cookies
    saved during student login.
    """

    session_id = request.session.get("backend_sessionid")
    csrf_token = request.session.get("backend_csrf_token")

    if not session_id:
        return None

    cookies = {
        "sessionid": session_id
    }

    if csrf_token:
        cookies["csrftoken"] = csrf_token

    return cookies


def extract_list(data, *possible_keys):
    """
    Safely extract a list from a backend JSON response.
    """

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in possible_keys:
            value = data.get(key)

            if isinstance(value, list):
                return value

    return []


def my_documents_page(request):

    # Check frontend login
    username = request.session.get("student_username")
    role = request.session.get("user_role")

    if not username or role != "STUDENT":
        return redirect("login_page")

    cookies = get_backend_cookies(request)

    if not cookies:
        return redirect("login_page")

    documents = []
    hod_requests = []
    page_error = None

    try:

        # Fetch uploaded student documents
        document_response = requests.get(
            BASE_URL + "api/documents/",
            cookies=cookies,
            timeout=15
        )

        document_response.raise_for_status()

        document_data = document_response.json()

        if document_data.get("success"):
            documents = extract_list(
                document_data,
                "documents",
                "data",
                "results"
            )
        else:
            page_error = document_data.get(
                "message",
                "Unable to load your documents."
            )


        # Fetch HOD-assigned submission requests
        request_response = requests.get(
            BASE_URL + "api/submission-requests/",
            cookies=cookies,
            timeout=15
        )

        request_response.raise_for_status()

        request_data = request_response.json()

        if request_data.get("success"):
            hod_requests = extract_list(
                request_data,
                "requests",
                "submission_requests",
                "data",
                "results"
            )
        elif not page_error:
            page_error = request_data.get(
                "message",
                "Unable to load HOD submission requests."
            )

    except requests.RequestException:
        page_error = (
            "Unable to connect to the ACADEX backend. "
            "Please check whether the backend server is running."
        )

    except ValueError:
        page_error = "The backend returned an invalid response."

    context = {
        "username": username,
        "documents": documents,
        "hod_requests": hod_requests,
        "page_error": page_error,
    }

    return render(
        request,
        "my_documents.html",
        context
    )

import requests

from django.shortcuts import render, redirect


BASE_URL = "http://127.0.0.1:8001/"


def hod_documents_page(request):

    username = request.session.get("student_username")
    role = request.session.get("user_role")

    # Check HOD login
    if not username:
        return redirect("login_page")

    if role != "HOD":
        return redirect("student_dashboard")

    # Backend authentication cookies
    cookies = {
        "sessionid": request.session.get("backend_sessionid"),
        "csrftoken": request.session.get("backend_csrf_token"),
    }

    csrf_token = request.session.get("backend_csrf_token")

    documents = []
    message = ""
    department = ""

    # Handle HOD verification form
    if request.method == "POST":

        document_id = request.POST.get("document_id")
        status = request.POST.get("status")
        comments = request.POST.get("comments", "").strip()

        if status not in ["APPROVED", "CORRECTION", "REJECTED"]:
            message = "Invalid review action."

        elif status in ["CORRECTION", "REJECTED"] and not comments:
            message = "Please enter comments for correction or rejection."

        else:
            try:
                response = requests.post(
                    BASE_URL + "api/hod/documents/",
                    data={
                        "document_id": document_id,
                        "status": status,
                        "comments": comments,
                    },
                    cookies=cookies,
                    headers={
                        "X-CSRFToken": csrf_token,
                        "Referer": BASE_URL,
                    },
                    timeout=30
                )

                result = response.json()

                if response.ok and result.get("success"):
                    message = result.get(
                        "message",
                        "Document review submitted successfully."
                    )
                else:
                    message = result.get(
                        "message",
                        "Unable to submit document review."
                    )

            except requests.RequestException:
                message = "Unable to connect to backend server."

            except ValueError:
                message = "Invalid response from backend."

    # Load documents
    try:
        response = requests.get(
            BASE_URL + "api/hod/documents/",
            cookies=cookies,
            timeout=30
        )

        result = response.json()

        if response.ok and result.get("success"):
            documents = result.get("documents", [])
            department = result.get("department", "")

        else:
            if not message:
                message = result.get(
                    "message",
                    "Unable to load student documents."
                )

    except requests.RequestException:
        if not message:
            message = "Unable to connect to backend server."

    except ValueError:
        if not message:
            message = "Invalid response from backend."

    context = {
        "username": username,
        "department": department,
        "documents": documents,
        "message": message,
        "total_documents": len(documents),
    }

    return render(
        request,
        "hod_documents.html",
        context
    )
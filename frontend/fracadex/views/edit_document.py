
import requests

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

BASE_URL = "http://127.0.0.1:8001/"


def get_backend_cookies(request):
    session_id = request.session.get("backend_sessionid")
    csrf_token = request.session.get("backend_csrf_token")

    if not session_id:
        return None

    cookies = {"sessionid": session_id}

    if csrf_token:
        cookies["csrftoken"] = csrf_token

    return cookies


@require_http_methods(["GET", "POST"])
def edit_document_page(request, document_id):

    username = request.session.get("student_username")
    role = request.session.get("user_role")

    if not username or role != "STUDENT":
        return redirect("login_page")

    cookies = get_backend_cookies(request)

    if not cookies:
        return redirect("login_page")

    document = None
    page_error = None

    # Fetch the student's documents
    try:
        response = requests.get(
            BASE_URL + "api/documents/",
            cookies=cookies,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            documents = data.get("documents", [])

            document = next(
                (
                    item for item in documents
                    if str(item.get("id")) == str(document_id)
                ),
                None
            )

        if not document:
            page_error = "Document not found."

    except requests.RequestException:
        page_error = "Unable to connect to the backend."

    except ValueError:
        page_error = "Invalid response received from the backend."

    if page_error:
        return render(
            request,
            "edit_document.html",
            {
                "username": username,
                "page_error": page_error,
                "document": None
            }
        )

    # Update document
    if request.method == "POST":

        new_title = request.POST.get("title", "").strip()
        replacement_file = request.FILES.get("file")

        if not new_title and not replacement_file:
            page_error = "Enter a new title or choose a replacement file."

        else:
            csrf_token = request.session.get("backend_csrf_token")

            headers = {}

            if csrf_token:
                headers["X-CSRFToken"] = csrf_token

            form_data = {
                "document_id": str(document_id),
                "title": new_title
            }

            files = None

            if replacement_file:
                files = {
                    "file": (
                        replacement_file.name,
                        replacement_file.file,
                        replacement_file.content_type
                    )
                }

            try:
                update_response = requests.post(
                    BASE_URL + "api/documents/edit/",
                    data=form_data,
                    files=files,
                    cookies=cookies,
                    headers=headers,
                    timeout=30
                )

                result = update_response.json()

                if update_response.ok and result.get("success"):
                    return redirect("my_documents_page")

                page_error = result.get(
                    "message",
                    "Unable to update the document."
                )

            except requests.RequestException:
                page_error = "Unable to connect to the backend."

            except ValueError:
                page_error = "Invalid response received from the backend."

    return render(
        request,
        "edit_document.html",
        {
            "username": username,
            "document": document,
            "page_error": page_error
        }
    )


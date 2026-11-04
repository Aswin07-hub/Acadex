
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST


BACKEND_URL = "http://127.0.0.1:8001/api/notifications/"


def notification_page(request):

    username = request.session.get("student_username")

    if not username:
        from django.shortcuts import redirect
        return redirect("login_page")

    context = {
        "username": username,
        "notifications": [],
        "total_count": 0,
        "unread_count": 0,
        "important_count": 0,
        "api_error": ""
    }

    try:
        response = requests.get(
            BACKEND_URL,
            params={"username": username},
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        context.update({
            "notifications": result.get("notifications", []),
            "total_count": result.get("total_count", 0),
            "unread_count": result.get("unread_count", 0),
            "important_count": result.get("important_count", 0)
        })

    except requests.RequestException as error:
        print("Notification API Error:", error)
        context["api_error"] = "Unable to connect to notification server."

    except ValueError as error:
        print("JSON Error:", error)
        context["api_error"] = "Invalid notification server response."

    return render(request, "notifications.html", context)


@require_POST
def mark_notification_read(request, notification_id):

    username = request.session.get("student_username")

    if not username:
        return JsonResponse({"success": False}, status=401)

    return send_backend_request(
        f"read/{notification_id}/", username
    )


@require_POST
def mark_all_notifications_read(request):

    username = request.session.get("student_username")

    if not username:
        return JsonResponse({"success": False}, status=401)

    return send_backend_request("read-all/", username)


@require_POST
def delete_notification(request, notification_id):

    username = request.session.get("student_username")

    if not username:
        return JsonResponse({"success": False}, status=401)

    return send_backend_request(
        f"delete/{notification_id}/", username
    )


def send_backend_request(endpoint, username):

    try:
        response = requests.post(
            BACKEND_URL + endpoint,
            data={"username": username},
            timeout=10
        )

        try:
            result = response.json()
        except ValueError:
            result = {"success": response.ok}

        return JsonResponse(result, status=response.status_code)

    except requests.RequestException as error:
        print("Backend Request Error:", error)

        return JsonResponse(
            {"success": False, "message": "Backend connection failed"},
            status=503
        )

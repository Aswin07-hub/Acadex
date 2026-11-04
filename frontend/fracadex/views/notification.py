
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST

BACKEND_URL = "http://127.0.0.1:8001/api/notifications/"


def notification_page(request):
    username = request.session.get("student_username")

    if not username:
        return redirect("login")

    try:
        response = requests.get(BACKEND_URL, params={"username": username}, timeout=10)
        response.raise_for_status()
        result = response.json()

        context = {
            "notifications": result.get("notifications", []),
            "unread_count": result.get("unread_count", 0),
            "total_count": result.get("total_count", 0),
            "important_count": result.get("important_count", 0),
            "api_error": ""
        }

    except (requests.RequestException, ValueError):
        context = {
            "notifications": [],
            "unread_count": 0,
            "total_count": 0,
            "important_count": 0,
            "api_error": "Unable to connect to notification server."
        }

    return render(request, "notifications.html", context)


@require_POST
def mark_notification_read(request, notification_id):
    username = request.session.get("student_username")

    if not username:
        return JsonResponse({"success": False, "message": "Login required"}, status=401)

    try:
        response = requests.post(
            f"{BACKEND_URL}read/{notification_id}/",
            data={"username": username},
            timeout=10
        )
        return JsonResponse(response.json(), status=response.status_code)

    except (requests.RequestException, ValueError):
        return JsonResponse({"success": False, "message": "Backend unavailable"}, status=503)


@require_POST
def mark_all_notifications_read(request):
    username = request.session.get("student_username")

    if not username:
        return JsonResponse({"success": False, "message": "Login required"}, status=401)

    try:
        response = requests.post(
            f"{BACKEND_URL}read-all/",
            data={"username": username},
            timeout=10
        )
        return JsonResponse(response.json(), status=response.status_code)

    except (requests.RequestException, ValueError):
        return JsonResponse({"success": False, "message": "Backend unavailable"}, status=503)


@require_POST
def delete_notification(request, notification_id):
    username = request.session.get("student_username")

    if not username:
        return JsonResponse({"success": False, "message": "Login required"}, status=401)

    try:
        response = requests.post(
            f"{BACKEND_URL}delete/{notification_id}/",
            data={"username": username},
            timeout=10
        )
        return JsonResponse(response.json(), status=response.status_code)

    except (requests.RequestException, ValueError):
        return JsonResponse({"success": False, "message": "Backend unavailable"}, status=503)

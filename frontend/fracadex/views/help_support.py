
import requests

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt

BASE_URL = "http://127.0.0.1:8001/"


def help_support_page(request):
    username = request.session.get("student_username")

    if not username:
        return redirect("login_page")

    return render(request, "help_support.html", {
        "username": username
    })


@csrf_exempt
@require_POST
def send_support_message(request):
    username = request.session.get("student_username")

    if not username:
        return JsonResponse({
            "success": False,
            "message": "Please log in again."
        }, status=401)

    question = request.POST.get("message", "").strip()
    conversation_id = request.POST.get("conversation_id", "")

    if not question:
        return JsonResponse({
            "success": False,
            "message": "Please enter your question."
        }, status=400)

    payload = {
        "username": username,
        "message": question
    }

    if conversation_id:
        payload["conversation_id"] = conversation_id

    try:
        response = requests.post(
            BASE_URL + "api/support/chat/",
            json=payload,
            timeout=90
        )

        return JsonResponse(
            response.json(),
            status=response.status_code
        )

    except requests.Timeout as e:
        print("ACADEX REQUEST TIMEOUT:", repr(e))

        return JsonResponse({
            "success": False,
            "message": "AI is taking too long. Please try again."
        }, status=504)

    except requests.RequestException as e:
        print("ACADEX CONNECTION ERROR:", repr(e))

        return JsonResponse({
            "success": False,
            "message": "Unable to connect to ACADEX server."
        }, status=503)


@require_GET
def support_history(request):
    username = request.session.get("student_username")

    if not username:
        return JsonResponse({
            "success": False,
            "message": "Please log in again."
        }, status=401)

    try:
        response = requests.get(
            BASE_URL + "api/support/history/",
            params={"username": username},
            timeout=10
        )

        return JsonResponse(
            response.json(),
            status=response.status_code
        )

    except requests.RequestException as e:
        print("ACADEX HISTORY ERROR:", repr(e))

        return JsonResponse({
            "success": False,
            "message": "Unable to connect to ACADEX server."
        }, status=503)

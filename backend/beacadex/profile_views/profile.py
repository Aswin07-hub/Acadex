
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_date

from beacadex.models import StudentProfile


@ensure_csrf_cookie
@csrf_protect
@require_http_methods(["GET", "POST"])
def student_profile_view(request):

    # Check backend authentication
    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "Please login first"
        }, status=401)

    # Check student role
    if request.user.role != "STUDENT":
        return JsonResponse({
            "success": False,
            "message": "Access denied"
        }, status=403)

    user = request.user

    profile, created = StudentProfile.objects.get_or_create(
        user=user
    )

    # Update profile
    if request.method == "POST":

        try:
            data = json.loads(request.body)

            if not isinstance(data, dict):
                raise ValueError()

        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            return JsonResponse({
                "success": False,
                "message": "Invalid profile data"
            }, status=400)

        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)

        profile.phone = data.get("phone", profile.phone)
        profile.address = data.get("address", profile.address)

        dob = data.get("date_of_birth", "")

        if dob:
            parsed_dob = parse_date(dob)

            if parsed_dob is None:
                return JsonResponse({
                    "success": False,
                    "message": "Invalid date of birth"
                }, status=400)

            profile.date_of_birth = parsed_dob

        user.save()
        profile.save()

    # Return profile
    return JsonResponse({
        "success": True,
        "message": (
            "Profile updated successfully"
            if request.method == "POST"
            else "Student profile fetched successfully"
        ),
        "profile": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "register_number": profile.register_number,
            "department": profile.department,
            "course": profile.course,
            "year": profile.year,
            "section": profile.section,
            "phone": profile.phone,
            "date_of_birth": (
                profile.date_of_birth.isoformat()
                if profile.date_of_birth else ""
            ),
            "address": profile.address
        }
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from beacadex.models import StudentProfile


@csrf_protect
@require_http_methods(["GET", "POST"])
def student_profile_view(request):

    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "Please login first"
        }, status=401)

    if request.user.role != "STUDENT":
        return JsonResponse({
            "success": False,
            "message": "Access denied"
        }, status=403)

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    user = request.user

    if request.method == "POST":

        import json

        data = json.loads(request.body)

        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)

        user.save()

        profile.register_number = data.get(
            "register_number", profile.register_number
        )
        profile.department = data.get(
            "department", profile.department
        )
        profile.course = data.get("course", profile.course)
        profile.year = data.get("year", profile.year)
        profile.section = data.get("section", profile.section)
        profile.phone = data.get("phone", profile.phone)
        profile.date_of_birth = data.get(
            "date_of_birth"
        ) or None
        profile.address = data.get("address", profile.address)

        profile.save()

    return JsonResponse({
        "success": True,
        "message": "Student profile fetched successfully",
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
            "address": profile.address,
        }
    })

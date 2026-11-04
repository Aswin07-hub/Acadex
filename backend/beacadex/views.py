
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import (
    ensure_csrf_cookie,
    csrf_protect,
    csrf_exempt
)
from django.db import transaction
from django.utils.dateparse import parse_date
from .models import StudentProfile, Notification

User = get_user_model()


# ==========================================
# GET: Generate CSRF Token
# ==========================================

@ensure_csrf_cookie
@require_GET
def get_csrf_token(request):
    return JsonResponse({
        "success": True,
        "message": "CSRF token generated"
    })


# ==========================================
# GET: Display Students as JSON
# POST: Register New Student
# ==========================================

@csrf_protect
@require_http_methods(["GET", "POST"])
def register_view(request):

    # GET METHOD
    if request.method == "GET":

        profiles = StudentProfile.objects.select_related("user").all()

        students = []

        for profile in profiles:
            students.append({
                "id": profile.user.id,
                "first_name": profile.user.first_name,
                "last_name": profile.user.last_name,
                "username": profile.user.username,
                "email": profile.user.email,
                "phone": profile.phone,
                "date_of_birth": (
                    profile.date_of_birth.isoformat()
                    if profile.date_of_birth else None
                ),
                "address": profile.address,
                "register_number": profile.register_number,
                "department": profile.department,
                "course": profile.course,
                "year": profile.year,
                "section": profile.section,
                "role": profile.user.role,
                "created_at": profile.created_at.isoformat()
            })

        return JsonResponse({
            "success": True,
            "total_students": len(students),
            "students": students
        })


    # POST METHOD
    if request.method == "POST":

        try:
            data = json.loads(request.body)

            if not isinstance(data, dict):
                raise ValueError()

        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            return JsonResponse({
                "success": False,
                "message": "Invalid JSON data"
            }, status=400)


        # Read form data

        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()

        date_of_birth = data.get("date_of_birth", "").strip()
        address = data.get("address", "").strip()

        register_number = data.get("register_number", "").strip()
        department = data.get("department", "").strip()
        course = data.get("course", "").strip()
        section = data.get("section", "").strip()

        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")

        year = data.get("year", "")


        # Validate required fields

        required_fields = [
            first_name,
            last_name,
            username,
            email,
            phone,
            register_number,
            department,
            section,
            password,
            confirm_password,
            str(year)
        ]

        if not all(required_fields):
            return JsonResponse({
                "success": False,
                "message": "Please fill all required fields"
            }, status=400)


        # Validate password

        if password != confirm_password:
            return JsonResponse({
                "success": False,
                "message": "Passwords do not match"
            }, status=400)

        if len(password) < 8:
            return JsonResponse({
                "success": False,
                "message": "Password must contain at least 8 characters"
            }, status=400)


        # Validate academic year

        try:
            year = int(year)

            if year not in [1, 2, 3, 4]:
                raise ValueError()

        except (ValueError, TypeError):
            return JsonResponse({
                "success": False,
                "message": "Select a valid academic year"
            }, status=400)


        # Validate date of birth

        dob = None

        if date_of_birth:
            dob = parse_date(date_of_birth)

            if dob is None:
                return JsonResponse({
                    "success": False,
                    "message": "Invalid date of birth"
                }, status=400)


        # Check duplicate username

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "success": False,
                "message": "Username already exists"
            }, status=409)


        # Check duplicate register number

        if StudentProfile.objects.filter(
            register_number=register_number
        ).exists():
            return JsonResponse({
                "success": False,
                "message": "Register number already exists"
            }, status=409)


        # Save User and Student Profile together

        try:
            with transaction.atomic():

                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    role="STUDENT"
                )

                profile = StudentProfile.objects.create(
                    user=user,
                    register_number=register_number,
                    department=department,
                    course=course,
                    year=year,
                    section=section,
                    phone=phone,
                    date_of_birth=dob,
                    address=address
                )

            return JsonResponse({
                "success": True,
                "message": "Student registered successfully",
                "student": {
                    "id": user.id,
                    "username": user.username,
                    "register_number": profile.register_number,
                    "department": profile.department,
                    "role": user.role
                }
            }, status=201)

        except Exception:
            return JsonResponse({
                "success": False,
                "message": "Registration failed. Please check your details."
            }, status=400)


# ==========================================
# POST: Student and HOD Login
# ==========================================

@csrf_protect
@require_POST
def login_view(request):

    try:
        data = json.loads(request.body)

        if not isinstance(data, dict):
            raise ValueError()

    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return JsonResponse({
            "success": False,
            "message": "Invalid request data"
        }, status=400)

    username = data.get("username", "")
    password = data.get("password", "")
    role = data.get("role", "")

    if not all(
        isinstance(value, str)
        for value in [username, password, role]
    ):
        return JsonResponse({
            "success": False,
            "message": "Invalid input"
        }, status=400)

    username = username.strip()
    role = role.strip().upper()

    if not username or not password or not role:
        return JsonResponse({
            "success": False,
            "message": "Please fill all fields"
        }, status=400)

    if role not in ["STUDENT", "HOD"]:
        return JsonResponse({
            "success": False,
            "message": "Invalid role"
        }, status=400)

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is None:
        return JsonResponse({
            "success": False,
            "message": "Invalid username or password"
        }, status=401)

    if user.role != role:
        return JsonResponse({
            "success": False,
            "message": "Incorrect role selected"
        }, status=403)

    login(request, user)

    return JsonResponse({
        "success": True,
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    })


# ==========================================
# POST: Logout
# ==========================================

@csrf_protect
@require_POST
def logout_view(request):

    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "User is not logged in"
        }, status=401)

    logout(request)

    return JsonResponse({
        "success": True,
        "message": "Logout successful"
    })



# ==========================================
# GET: Display Student Notifications
# ==========================================

@csrf_exempt
@require_GET
def notification_list(request):

    username = request.GET.get("username")

    if not username:
        return JsonResponse({
            "success": False,
            "message": "Username is required"
        }, status=400)

    notifications = Notification.objects.filter(
        recipient__username=username,
        recipient__role="STUDENT"
    )

    data = []

    for notification in notifications:
        data.append({
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "category": notification.category,
            "category_display": notification.get_category_display(),
            "priority": notification.priority,
            "is_read": notification.is_read,
            "created_at": notification.created_at.strftime(
                "%d %b %Y, %I:%M %p"
            )
        })

    return JsonResponse({
        "success": True,
        "notifications": data,
        "total_count": notifications.count(),
        "unread_count": notifications.filter(
            is_read=False
        ).count(),
        "important_count": notifications.filter(
            priority__in=["IMPORTANT", "URGENT"]
        ).count()
    })


# ==========================================
# POST: Mark One Notification as Read
# ==========================================

@csrf_exempt
@require_POST
def mark_notification_read(request, notification_id):

    username = request.POST.get("username")

    if not username:
        return JsonResponse({
            "success": False,
            "message": "Username is required"
        }, status=400)

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient__username=username,
        recipient__role="STUDENT"
    )

    notification.is_read = True
    notification.save(update_fields=["is_read"])

    return JsonResponse({
        "success": True,
        "message": "Notification marked as read"
    })


# ==========================================
# POST: Mark All Notifications as Read
# ==========================================

@csrf_exempt
@require_POST
def mark_all_notifications_read(request):

    username = request.POST.get("username")

    if not username:
        return JsonResponse({
            "success": False,
            "message": "Username is required"
        }, status=400)

    Notification.objects.filter(
        recipient__username=username,
        recipient__role="STUDENT",
        is_read=False
    ).update(is_read=True)

    return JsonResponse({
        "success": True,
        "message": "All notifications marked as read"
    })


# ==========================================
# POST: Delete Notification
# ==========================================

@csrf_exempt
@require_POST
def delete_notification(request, notification_id):

    username = request.POST.get("username")

    if not username:
        return JsonResponse({
            "success": False,
            "message": "Username is required"
        }, status=400)

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient__username=username,
        recipient__role="STUDENT"
    )

    notification.delete()

    return JsonResponse({
        "success": True,
        "message": "Notification deleted successfully"
    })
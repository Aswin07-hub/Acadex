
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_date
from django.utils import timezone

from .models import (
    SubmissionRequest,
    Document,
    HODProfile,
    StudentProfile
)


@csrf_protect
@require_http_methods(["GET", "POST"])
def submission_requests_api(request):

    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "Please login first."
        }, status=401)

    # GET: Students and HODs can view requests
    if request.method == "GET":

        if request.user.role == "HOD":
            try:
                profile = HODProfile.objects.get(user=request.user)
            except HODProfile.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "message": "HOD profile not found."
                }, status=404)

            requests_list = SubmissionRequest.objects.filter(
                department=profile.department
            ).order_by("-created_at")

        elif request.user.role == "STUDENT":
            try:
                profile = StudentProfile.objects.get(user=request.user)
            except StudentProfile.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "message": "Student profile not found."
                }, status=404)

            requests_list = SubmissionRequest.objects.filter(
                department=profile.department,
                is_active=True
            ).order_by("-created_at")

        else:
            return JsonResponse({
                "success": False,
                "message": "Access denied."
            }, status=403)

        data = []

        for item in requests_list:

            request_data = {
                "id": item.id,
                "title": item.title,
                "document_type": item.document_type,
                "description": item.description,
                "deadline": item.deadline.isoformat(),
                "is_active": item.is_active
            }

            if request.user.role == "HOD":
                request_data["submission_count"] = (
                    item.submissions.count()
                )

            else:
                submitted_document = Document.objects.filter(
                    submission_request=item,
                    student=profile
                ).order_by("-uploaded_at").first()

                request_data["has_submitted"] = (
                    submitted_document is not None
                )

                request_data["submission_status"] = (
                    submitted_document.status
                    if submitted_document else "NOT_SUBMITTED"
                )

            data.append(request_data)

        return JsonResponse({
            "success": True,
            "requests": data
        })

    # POST: Only HODs can create requests
    if request.user.role != "HOD":
        return JsonResponse({
            "success": False,
            "message": "Only HODs can create requests."
        }, status=403)

    try:
        hod_profile = HODProfile.objects.get(user=request.user)
    except HODProfile.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "HOD profile not found."
        }, status=404)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({
            "success": False,
            "message": "Invalid request data."
        }, status=400)

    document_type = data.get("document_type", "").strip()
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    deadline_text = data.get("deadline", "").strip()

    if not all([document_type, title, description, deadline_text]):
        return JsonResponse({
            "success": False,
            "message": "Please provide all required fields."
        }, status=400)

    if document_type not in dict(Document.DOCUMENT_TYPES):
        return JsonResponse({
            "success": False,
            "message": "Invalid document category."
        }, status=400)

    deadline = parse_date(deadline_text)

    if not deadline:
        return JsonResponse({
            "success": False,
            "message": "Invalid deadline."
        }, status=400)

    if deadline < timezone.localdate():
        return JsonResponse({
            "success": False,
            "message": "Deadline cannot be in the past."
        }, status=400)

    submission_request = SubmissionRequest.objects.create(
        created_by=request.user,
        department=hod_profile.department,
        document_type=document_type,
        title=title,
        description=description,
        deadline=deadline
    )

    return JsonResponse({
        "success": True,
        "message": "Submission request created successfully.",
        "request_id": submission_request.id
    }, status=201)

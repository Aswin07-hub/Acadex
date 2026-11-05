
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

from .models import (
    Document,
    StudentProfile,
    SubmissionRequest
)


# ==========================================
# COMMON STUDENT AUTHENTICATION
# ==========================================

def get_logged_in_student(request):

    if not request.user.is_authenticated:
        return None, JsonResponse({
            "success": False,
            "message": "Please login first."
        }, status=401)

    if request.user.role != "STUDENT":
        return None, JsonResponse({
            "success": False,
            "message": "Only students can access this feature."
        }, status=403)

    try:
        student = StudentProfile.objects.get(user=request.user)
        return student, None

    except StudentProfile.DoesNotExist:
        return None, JsonResponse({
            "success": False,
            "message": "Student profile not found."
        }, status=404)


# ==========================================
# FILE VALIDATION
# ==========================================

def validate_uploaded_file(uploaded_file):

    allowed_extensions = [
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"
    ]

    filename = uploaded_file.name.lower()

    if not any(filename.endswith(ext) for ext in allowed_extensions):
        return False

    return True


# ==========================================
# STUDENT DOCUMENT UPLOAD API
# ==========================================

@csrf_protect
@require_POST
def upload_student_document(request):

    student, error = get_logged_in_student(request)

    if error:
        return error

    document_type = request.POST.get(
        "document_type", ""
    ).strip()

    title = request.POST.get(
        "title", ""
    ).strip()

    uploaded_file = request.FILES.get("file")

    submission_request_id = request.POST.get(
        "submission_request_id", ""
    ).strip()

    if not document_type or not title or not uploaded_file:
        return JsonResponse({
            "success": False,
            "message": "Please provide document type, title and file."
        }, status=400)

    valid_types = dict(Document.DOCUMENT_TYPES)

    if document_type not in valid_types:
        return JsonResponse({
            "success": False,
            "message": "Invalid document type."
        }, status=400)

    if not validate_uploaded_file(uploaded_file):
        return JsonResponse({
            "success": False,
            "message": "Only PDF, JPG, JPEG and PNG files are allowed."
        }, status=400)

    linked_request = None

    if submission_request_id:

        try:
            linked_request = SubmissionRequest.objects.get(
                id=int(submission_request_id),
                department=student.department,
                is_active=True
            )

        except (SubmissionRequest.DoesNotExist, ValueError):
            return JsonResponse({
                "success": False,
                "message": "Invalid or inactive submission request."
            }, status=404)

        if linked_request.deadline < timezone.localdate():
            return JsonResponse({
                "success": False,
                "message": "The submission deadline has passed."
            }, status=400)

        if linked_request.document_type != document_type:
            return JsonResponse({
                "success": False,
                "message": "Document type does not match the request."
            }, status=400)

        existing_document = Document.objects.filter(
            student=student,
            submission_request=linked_request
        ).exists()

        if existing_document:
            return JsonResponse({
                "success": False,
                "message": "You have already submitted this request."
            }, status=400)

    document = Document.objects.create(
        student=student,
        document_type=document_type,
        title=title,
        file=uploaded_file,
        status="PENDING",
        version=1,
        submission_request=linked_request
    )

    return JsonResponse({
        "success": True,
        "message": "Document uploaded successfully.",
        "document": {
            "id": document.id,
            "title": document.title,
            "document_type": document.get_document_type_display(),
            "status": document.status,
            "version": document.version,
            "uploaded_at": document.uploaded_at.strftime(
                "%d %b %Y, %I:%M %p"
            )
        }
    }, status=201)


# ==========================================
# FETCH STUDENT'S DOCUMENTS
# GET /api/documents/
# ==========================================

@require_http_methods(["GET"])
def student_documents_api(request):

    student, error = get_logged_in_student(request)

    if error:
        return error

    documents = Document.objects.filter(
        student=student
    ).order_by("-uploaded_at")

    document_list = []

    for document in documents:

        document_list.append({
            "id": document.id,
            "title": document.title,
            "document_type": document.document_type,
            "document_type_display": document.get_document_type_display(),
            "status": document.status,
            "version": document.version,
            "uploaded_at": document.uploaded_at.strftime(
                "%d %b %Y, %I:%M %p"
            ),
            "file_url": (
                request.build_absolute_uri(document.file.url)
                if document.file else None
            ),
            "submission_request_id": (
                document.submission_request_id
            )
        })

    return JsonResponse({
        "success": True,
        "documents": document_list,
        "total_documents": len(document_list)
    })


# ==========================================
# EDIT / REPLACE STUDENT DOCUMENT
# POST /api/documents/edit/
# ==========================================

@csrf_protect
@require_POST
def edit_student_document(request):

    student, error = get_logged_in_student(request)

    if error:
        return error

    document_id = request.POST.get("document_id", "").strip()
    new_title = request.POST.get("title", "").strip()
    replacement_file = request.FILES.get("file")

    if not document_id:
        return JsonResponse({
            "success": False,
            "message": "Document ID is required."
        }, status=400)

    try:
        document = Document.objects.get(
            id=int(document_id),
            student=student
        )

    except (Document.DoesNotExist, ValueError):
        return JsonResponse({
            "success": False,
            "message": "Document not found."
        }, status=404)

    if document.status == "APPROVED":
        return JsonResponse({
            "success": False,
            "message": "Approved documents cannot be edited."
        }, status=400)

    if not new_title and not replacement_file:
        return JsonResponse({
            "success": False,
            "message": "Enter a new title or choose a replacement file."
        }, status=400)

    if new_title:
        document.title = new_title

    if replacement_file:

        if not validate_uploaded_file(replacement_file):
            return JsonResponse({
                "success": False,
                "message": "Only PDF, JPG, JPEG and PNG files are allowed."
            }, status=400)

        document.file = replacement_file
        document.version += 1
        document.status = "PENDING"

    document.updated_at = timezone.now()
    document.save()

    return JsonResponse({
        "success": True,
        "message": "Document updated successfully.",
        "document": {
            "id": document.id,
            "title": document.title,
            "document_type": document.get_document_type_display(),
            "status": document.status,
            "version": document.version
        }
    })

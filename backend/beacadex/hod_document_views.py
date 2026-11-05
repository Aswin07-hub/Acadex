

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

from .models import HODProfile, Document, DocumentReview


@csrf_protect
@require_http_methods(["GET", "POST"])
def hod_documents_api(request):

    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "Please login first."
        }, status=401)

    # Only HOD can access this API
    if request.user.role != "HOD":
        return JsonResponse({
            "success": False,
            "message": "Only HODs can access documents."
        }, status=403)

    # Get HOD profile
    try:
        hod = HODProfile.objects.get(user=request.user)

    except HODProfile.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "HOD profile not found."
        }, status=404)

    # ------------------------------------------
    # GET: DISPLAY DEPARTMENT DOCUMENTS
    # ------------------------------------------

    if request.method == "GET":

        documents = Document.objects.filter(
            student__department=hod.department
        ).select_related(
            "student",
            "student__user",
            "submission_request"
        ).order_by("-uploaded_at")

        document_list = []

        for document in documents:

            latest_review = document.reviews.order_by(
                "-reviewed_at"
            ).first()

            document_list.append({
                "id": document.id,
                "title": document.title,
                "document_type": document.get_document_type_display(),

                "student_name": (
                    document.student.user.get_full_name()
                    or document.student.user.username
                ),

                "register_number": document.student.register_number,
                "department": document.student.department,

                "status": document.status,
                "status_display": document.get_status_display(),

                "version": document.version,

                "uploaded_at": document.uploaded_at.strftime(
                    "%d %b %Y, %I:%M %p"
                ),

                "file_url": request.build_absolute_uri(
                    document.file.url
                ),

                "submission_request_id": (
                    document.submission_request_id
                ),

                "submission_request_title": (
                    document.submission_request.title
                    if document.submission_request else None
                ),

                "review_comments": (
                    latest_review.comments if latest_review else ""
                ),

                "reviewed_at": (
                    latest_review.reviewed_at.strftime(
                        "%d %b %Y, %I:%M %p"
                    )
                    if latest_review else None
                )
            })

        return JsonResponse({
            "success": True,
            "department": hod.department,
            "total_documents": len(document_list),
            "documents": document_list
        })

    # ------------------------------------------
    # POST: HOD REVIEWS A DOCUMENT
    # ------------------------------------------

    document_id = request.POST.get("document_id")
    new_status = request.POST.get("status", "").strip().upper()
    comments = request.POST.get("comments", "").strip()

    if not document_id or not new_status:
        return JsonResponse({
            "success": False,
            "message": "Document ID and review status are required."
        }, status=400)

    allowed_statuses = [
        "APPROVED",
        "CORRECTION",
        "REJECTED"
    ]

    if new_status not in allowed_statuses:
        return JsonResponse({
            "success": False,
            "message": "Invalid review status."
        }, status=400)

    if new_status in ["CORRECTION", "REJECTED"] and not comments:
        return JsonResponse({
            "success": False,
            "message": "Please provide comments for this decision."
        }, status=400)

    # Find document only within this HOD's department
    try:
        document = Document.objects.get(
            id=document_id,
            student__department=hod.department
        )

    except Document.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Document not found in your department."
        }, status=404)

    # Save review history
    DocumentReview.objects.create(
        document=document,
        reviewer=request.user,
        status=new_status,
        comments=comments
    )

    # Update current document status
    document.status = new_status
    document.save(update_fields=["status", "updated_at"])

    return JsonResponse({
        "success": True,
        "message": "Document review submitted successfully.",
        "document_id": document.id,
        "status": document.status,
        "comments": comments
    })

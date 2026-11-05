
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# ==================================================
# 1. USER MODEL
# Used by both Student and HOD
# ==================================================

class User(AbstractUser):

    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('HOD', 'HOD'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.username} - {self.role}"


# ==================================================
# 2. STUDENT PROFILE MODEL
# Student personal and academic information
# ==================================================

class StudentProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    register_number = models.CharField(
        max_length=20,
        unique=True
    )

    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100, blank=True)
    year = models.PositiveIntegerField()
    section = models.CharField(max_length=10)

    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    profile_photo = models.ImageField(
        upload_to='student_profiles/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.register_number


# ==================================================
# 3. HOD PROFILE MODEL
# HOD personal and department information
# ==================================================

class HODProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hod_profile'
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    department = models.CharField(max_length=100)

    designation = models.CharField(
        max_length=100,
        default='Head of Department'
    )

    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.employee_id} - {self.department}"


# ==================================================
# 4. SUBMISSION REQUEST MODEL
# HOD creates academic submission requests
# ==================================================

class SubmissionRequest(models.Model):

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submission_requests'
    )

    department = models.CharField(max_length=100)

    document_type = models.CharField(max_length=30)

    title = models.CharField(max_length=150)

    description = models.TextField()

    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.department}"


# ==================================================
# 5. DOCUMENT MODEL
# Students upload academic documents
# ==================================================

class Document(models.Model):

    DOCUMENT_TYPES = [
        ('ASSIGNMENT', 'Assignment'),
        ('GROUP_PROJECT', 'Group Project Report'),
        ('MINI_PROJECT', 'Mini Project Report'),
        ('FINAL_PROJECT', 'Final Year Project'),
        ('SEMINAR', 'Seminar Report'),
        ('INTERNSHIP', 'Internship Report'),
        ('INDUSTRIAL_VISIT', 'Industrial Visit Report'),
        ('RESEARCH', 'Research Paper'),
        ('OTHER', 'Other Academic Work'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('CORRECTION', 'Correction Required'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    submission_request = models.ForeignKey(
        SubmissionRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='submissions'
    )

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES
    )

    title = models.CharField(max_length=150)

    file = models.FileField(
        upload_to='student_documents/'
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    version = models.PositiveIntegerField(default=1)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.student.register_number}"


# ==================================================
# 6. DOCUMENT REVIEW MODEL
# HOD reviews student documents
# ==================================================

class DocumentReview(models.Model):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='document_reviews'
    )

    status = models.CharField(
        max_length=15,
        choices=Document.STATUS_CHOICES
    )

    comments = models.TextField(blank=True)

    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document.title} - {self.status}"


# ==================================================
# 7. ANNOUNCEMENT MODEL
# HOD publishes campus announcements
# ==================================================

class Announcement(models.Model):

    AUDIENCE_CHOICES = [
        ('ALL', 'All Students'),
        ('DEPARTMENT', 'Department'),
        ('YEAR', 'Specific Year'),
        ('SECTION', 'Specific Section'),
    ]

    PRIORITY_CHOICES = [
        ('NORMAL', 'Normal'),
        ('IMPORTANT', 'Important'),
        ('URGENT', 'Urgent'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='announcements'
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    audience = models.CharField(
        max_length=15,
        choices=AUDIENCE_CHOICES,
        default='ALL'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='NORMAL'
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    section = models.CharField(
        max_length=10,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


# ==================================================
# 8. NOTIFICATION MODEL
# Notifications for Students and HOD
# ==================================================

class Notification(models.Model):

    CATEGORY_CHOICES = [
        ('ACADEMIC', 'Academic'),
        ('DOCUMENT', 'Documents'),
        ('ANNOUNCEMENT', 'Announcements'),
        ('EVENT', 'Events'),
        ('SYSTEM', 'System Updates'),
    ]

    PRIORITY_CHOICES = [
        ('NORMAL', 'Normal'),
        ('IMPORTANT', 'Important'),
        ('URGENT', 'Urgent'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='ANNOUNCEMENT'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='NORMAL'
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"


# ==================================================
# 9. AUDIT LOG MODEL
# Tracks important activities
# ==================================================

class AuditLog(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action




# ==========================================
# 9. SUPPORT CONVERSATION MODEL
# ==========================================

class SupportConversation(models.Model):

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="support_conversations"
    )

    subject = models.CharField(
        max_length=200,
        default="AI Help & Support"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.register_number} - {self.subject}"


# ==========================================
# 10. SUPPORT MESSAGE MODEL
# ==========================================

class SupportMessage(models.Model):

    SENDER_CHOICES = [
        ("STUDENT", "Student"),
        ("AI", "AI Assistant"),
    ]

    STATUS_CHOICES = [
        ("ANSWERED", "Answered"),
        ("UNRESOLVED", "Unresolved"),
    ]

    conversation = models.ForeignKey(
        SupportConversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.CharField(
        max_length=10,
        choices=SENDER_CHOICES
    )

    message = models.TextField()

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="ANSWERED"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.created_at}"

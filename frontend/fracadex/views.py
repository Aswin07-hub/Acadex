from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def login_page(request):
    return render(request, 'login.html')
# Create your views here.


@login_required
def student_dashboard(request):
    context = {
        'total_documents': 0,
        'approved_documents': 0,
        'pending_documents': 0,
        'rejected_documents': 0,
        'documents': [],
        'events': [],
        'notifications': [],
    }

    return render(request, 'student_dashboard.html', context)
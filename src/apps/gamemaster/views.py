from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()

@login_required
@permission_required('auth.view_user', raise_exception=True)  
def gamemaster_dashboard(request):
    users = User.objects.all()  
    return render(request, 'gamemaster_dashboard.html', {'users': users})

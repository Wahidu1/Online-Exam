from .models import Examinee, Notification

def global_context(request):
    context = {
        'notifications': [],
        'unread_notifications': 0,
        'examinee': None
    }
    
    if request.session.get('is_logged_in'):
        email = request.session.get('user_email')
        examinee = Examinee.objects.filter(email=email).first()
        
        if examinee:
            notifications = Notification.objects.filter(examinee=examinee, is_read=False)
            unread_count = notifications.count()
            
            context['notifications'] = notifications
            context['unread_notifications'] = unread_count
            context['examinee'] = examinee
    
    return context

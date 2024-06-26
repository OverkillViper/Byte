from .models import Notification, Account

def notification_context(request):
    
    if not request.user.is_anonymous:
        account = Account.objects.get(email=request.user.email)
        
        notifications = Notification.objects.filter(account=account).order_by('-created_at')[:3]
        unseen = any(notification.seen == False for notification in notifications)
        
        notifications = notifications[:3]
        
        return {
            'notifications' : notifications,
            'unseen'        : unseen
        }
    else:
        return {
            'notifications' : None,
            'unseen'        : False
        }

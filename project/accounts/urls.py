from django.urls import path
from . import views

urlpatterns = [
    # Notification
    path('notifications', views.notifications, name='notifications'),
    path('notification-link/<str:notification_id>/', views.notificationLink, name='notificationLink'),
    path('delete-notification/<str:notification_id>', views.deleteNotification, name='deleteNotification'),
    path('delete-all-notifications', views.deleteAllNotification, name='deleteAllNotification'),
    
    # Account
    path('account', views.account, name='account'),
    
    # Messages
    path('conversations', views.conversations, name='conversations'),
    path('conversation/<str:conversation_id>', views.conversationDetail, name='conversationDetail'),
    path('start-conversation/<str:email>', views.startConversation, name='startConversation'),
    path('delete-conversation/<str:conversation_id>', views.deleteConversation, name='deleteConversation'),
]
from django.shortcuts               import render, redirect, get_object_or_404
from .models                        import *
from authenticate.views             import validate_field
from django.contrib                 import messages
from django.http                    import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def addAddress(request):
    
    if request.method == 'POST' and request.user.is_authenticated:
    
        title    = request.POST.get('title')
        street   = request.POST.get('street')
        city     = request.POST.get('city')
        district = request.POST.get('district')
        country  = request.POST.get('country')
        
        errors = []
        
        validate_field(title,    "", 'Address title must not be empty', errors)
        validate_field(street,   "", 'Street name must not be empty',   errors)
        validate_field(city,     "", 'City must not be empty',          errors)
        validate_field(district, "", 'District must not be empty',      errors)
        validate_field(country,  "", 'Country must not be empty',       errors)
        
        if errors:
            for error in errors:
                messages.error(request, error)
                
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            account  = Account.objects.get(email=request.user.email)
            
            address  = Address(account=account, title=title, street=street, city=city, district=district, country=country)
            address.save()
            
            messages.success(request, 'Address added successfully')
            
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid request')
        
def deleteAddress(request, address_id):
    
    account = Account.objects.get(email=request.user.email)
    address = Address.objects.get(id=address_id)
    
    if address.account == account:
        address.delete()
        
    return redirect(request.META.get('HTTP_REFERER'))

def notificationLink(request, notification_id):
    
    ref = request.GET.get('ref')
    
    notification = Notification.objects.get(id=notification_id)
    
    notification.seen = True
    notification.save()
    
    return redirect(str(ref))

def deleteNotification(request, notification_id):
    
    account = Account.objects.get(email=request.user.email)
    
    notification = Notification.objects.get(id=notification_id)
    
    if notification.account == account:
        notification.delete()
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('unauthorized')
    
def deleteAllNotification(request):
    
    account = Account.objects.get(email=request.user.email)
    
    notifications = Notification.objects.filter(account=account)
    
    for notification in notifications:
        notification.delete()
        
    return redirect(request.META.get('HTTP_REFERER'))
    
def notifications(request):
    account = Account.objects.get(email=request.user.email)
    
    notifications = Notification.objects.filter(account=account).order_by('-created_at')
    
    context = {
        'notifications' : notifications,
        'page_title'    : 'Notifications'
    }
    if request.user.role == 'seller':
        return render(request, 'seller/notifications.html', context)
    elif request.user.role == 'customer':
        return render(request, 'customer/notifications.html', context)
    else:
        return redirect('unauthorized')
    
def account(request):
    
    account = Account.objects.get(email=request.user.email)
    
    context = {
        'page_title' : 'Account',
        'referrer'   : '/' + ('moderator' if account.role == 'admin' else account.role) + '/dashboard',
        'account'    : account
    }
    
    match account.role:
        case 'customer':
            return render(request, 'customer/account_self.html', context)
        case 'seller':
            return render(request, 'seller/account_self.html', context)
        case 'admin':
            return render(request, 'moderator/account_self.html', context)
        case _:
            return HttpResponse('Invalid role')
        
def conversations(request):
    
    account = Account.objects.get(email=request.user.email)
    
    conversations = Conversation.objects.filter(participants=account)
         
    last_messages = {}
    
    # for conversation in conversations:
    #     last_message = conversation.messages.order_by('-created_at').first()
    #     last_messages[conversation.id] = last_message
    
    context = {
        'conversations' : conversations,
        # 'last_messages' : last_messages,
        'page_title'    : 'Conversations',
        'referrer'      : '/auth/login'
    }
    
    match account.role:
        case 'customer':
            return render(request, 'customer/conversations.html', context)
        case 'seller':
            return render(request, 'seller/conversations.html', context)
        case _:
            return HttpResponse('Invalid role')
        
@login_required(login_url='/auth/login')        
def startConversation(request, email):
    recipient = get_object_or_404(Account, email=email)
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=recipient).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, recipient)
    
    return redirect('conversationDetail', conversation_id=conversation.id)

@login_required(login_url='/auth/login') 
def deleteConversation(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)
    
    conversation.delete()
    
    return redirect('/account/conversations')

@login_required(login_url='/auth/login') 
def conversationDetail(request, conversation_id):
    
    account = Account.objects.get(email=request.user.email)
    
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    if request.user not in conversation.participants.all():
        return redirect('conversations')
    
    messages = conversation.messages.order_by('created_at')

    if request.method == 'POST':
        message_text = request.POST.get('message')
        
        message = Message(content=message_text, conversation=conversation, sender=account)
        message.save()
        
        return redirect('conversationDetail', conversation_id=conversation.id)
    else:
        context = {
            'conversation'  : conversation,
            'msgs'          : messages,
            'page_title'    : 'Conversation Details',
            'referrer'      : '/account/conversations'
        }

        match account.role:
            case 'customer':
                return render(request, 'customer/conversation_detail.html', context)
            case 'seller':
                return render(request, 'seller/conversation_detail.html', context)
            case _:
                return HttpResponse('Invalid role')

from django.shortcuts               import render, redirect
from django.http                    import HttpResponse
from django.contrib                 import messages
from .forms                         import *
from accounts.models                import Account, AccountActivationToken, Notification
from django.contrib.auth            import authenticate, logout
from django.contrib.auth            import login as auth_login
from django.contrib.auth            import get_user_model
from .decorators                    import unauthenticated_account, allowed_account
from accounts.tokens                import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http              import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding          import force_bytes, force_str
from django.core.mail               import EmailMessage, EmailMultiAlternatives
from django.template.loader         import render_to_string

import re

# Login
@unauthenticated_account
def login(request):
    context = {}
    
    if request.method == 'POST':
        form = loginForm(request.POST)
        
        email       = request.POST.get('email')
        password    = request.POST.get('password')
        nextURL     = request.POST.get('next')
        account     = authenticate(username=email, password=password)
              
        errors = []
        
        validate_field(email,    "", "Please enter your email",   errors)
        validate_field(password, "", "Please enter the password", errors)
       
        # Check if authentication is successful
        if email != "" and password != "" and account is None:
            errors.append("Invalid email or password")
        
        # Login only if no error exists
        if not errors:
            auth_login(request, account)
            
            if nextURL is None or nextURL == "":
                if request.user.role == 'customer':
                    return redirect('/customer/dashboard')
                elif request.user.role == 'seller': 
                    return redirect('/seller/dashboard')
                elif request.user.role == 'admin':
                    return redirect('/moderator/dashboard')
                else:
                    return HttpResponse('Invalid account role')
            else:
                return redirect(nextURL)
        else:
            for error in errors:
                messages.error(request, error)
    else:
        form = loginForm()
    
    context = {
        'form' : form
    }
    
    return render(request, 'authenticate/login.html', context)

# Register
@unauthenticated_account
def register(request, role):
    context = {}
    
    if request.method == 'POST':
        form        = registerForm(request.POST)
        
        first_name  = request.POST.get('first_name')
        last_name   = request.POST.get('last_name')
        email       = request.POST.get('email')
        phone       = request.POST.get('phone')
        password1   = request.POST.get('password1')
        password2   = request.POST.get('password2')
        
        errors = []
        
        # Check if field is empty
        validate_field(first_name,  "", "First name cannot be empty",   errors)
        validate_field(last_name,   "", "Last name cannot be empty",    errors)
        validate_field(email,       "", "Email cannot be empty",        errors)
        validate_field(phone,       "", "Phone number cannot be empty", errors)
        validate_field(password1,   "", "Please provide a password",    errors)
        validate_field(password2,   "", "Please confirm the password",  errors)
        
        if first_name != "" and has_numbers(first_name):
            errors.append("First name cannot contain numbers")
            
        if last_name != "" and  has_numbers(last_name):
            errors.append("Last name cannot contain numbers")
        
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        
        if email != "" and not EMAIL_REGEX.match(email):
            errors.append("Please enter a valid email")
        
        if phone != "" and len(phone) < 11:
            errors.append("Phone number must be 11+ charecters long")
        
        if len(password1) < 6:
            errors.append("Password must be 6+ charecters long")
            
        if role not in ['customer', 'seller']:
            errors.append("Invalid role. Must be customer or admin")
            
        if password1 != "" and password2 != "" and password1 != password2:
            errors.append("Passwords do not match")
            
        if not errors:
            # Create account if no errors exists
            user = Account.objects.create_user(
                email      = email,
                password   = password1,
                first_name = first_name,
                last_name  = last_name,
                phone      = phone,
                role       = role
            )
            
            account = authenticate(username=email, password=password1)
            auth_login(request, account)
            
            notification = Notification.objects.create(
                account=account,
                title="Welcome to Byte",
                content="Lets begin your tech journey",
                ref='/auth/login'
            )
            
            sendActivatationEmail(request, account, email)
            
            return redirect('/auth/activate-email-sent')
        else:
            # Return errors if exists
            for error in errors:
                messages.error(request, error)

    else:
        form = registerForm()
        
    context = {
        'form' : form,
        'role' : role
    }
        
    return render(request, 'authenticate/register.html', context)

# Logout
def logoutAccount(request):
    logout(request)
    return redirect('/auth/login')

def sendActivatationEmail(request, user, to_email):
    subject = "Activate your account | BYTE"
    
    uid     = urlsafe_base64_encode(force_bytes(user.email))
    token   = account_activation_token.make_token(user)
    
    activatetionToken = AccountActivationToken(uid=uid, token=token)
    activatetionToken.save()
    
    text_content = 'Please visit this link to activate your account. http://localhost:8000/auth/activate/' + uid + '/' + token
    html_content = '<div style="background-color: #131517; padding: 20px"><table style="margin:auto"><tr><td style="padding:20px; text-align:center; font-family: \'Arial\'; font-size: 20px; color: white; font-weight: bold">BYTE</td></tr><tr><td style="text-align:center; font-family: \'Arial\'; font-size: 14px; color: white;">Please click the below link to activate your account</td></tr><tr><td style="text-align:center; padding: 20px;"><a href="http://localhost:8000/auth/activate/' + urlsafe_base64_encode(force_bytes(user.email)) + '/' + account_activation_token.make_token(user) + '" style="background: #8bc2f9; text-decoration: none;color:black;font-family: \'Arial\'; font-size: 14px; font-weight: bold; border-radius: 5px; padding: 10px;">Activate Account</a></td></tr></table></div>'
    
    email = EmailMultiAlternatives(subject, text_content, to=[to_email])
    email.attach_alternative(html_content, "text/html")

    if not email.send():
        return HttpResponse("Error sending activation email. Please check the provided email address exists.")

def activateAccount(request, uidb64, token):
    
    account = get_user_model()
    
    try:
        uid             = force_str(urlsafe_base64_decode(uidb64))
        activationToken = AccountActivationToken.objects.get(uid=uidb64)
        account         = Account.objects.get(email=uid)
        
        print(account)
    except:
        account = None
    
    if account is not None and account_activation_token.check_token(account, token):

        print(activationToken.created_at)

        if not activationToken.is_expired():
            account.email_verified = True
            account.save()
            
            activationToken.delete()
            
            messages.success(request, "Account activated successfully")

            return redirect('login')
        else:
            return HttpResponse("token expired")
        
    else:
        return redirect('activateLinkInvalid')

def activateEmailSent(request):
       
    context = {
        'last_name' : request.user.last_name,
        'email'     : request.user.email
    }
    
    if request.user.email_verified:
        if request.user.role == 'customer':
            return redirect('/customer/dashboard')
        elif request.user.role == 'seller': 
            return redirect('/seller/dashboard')
        else:
            return HttpResponse('Invalid account role')
    else:
        return render(request, 'authenticate/activate_email_sent.html', context)

def activateLinkInvalid(request):
    return render(request, 'authenticate/activate_link_invalid.html')

def redirectToDashboard(request):
    
    print('Inside redirect to dashboard')
    
    if request.user.role == 'customer' or request.user.role == 'admin':
        print('redirecting to customer dashboard')
        return redirect('/customer/dashboard')
    elif request.user.role == 'seller' or request.user.role == 'admin': 
        return redirect('/seller/dashboard')
    else:
        return HttpResponse('Invalid account role')

def unauthorized(request):
    return render(request, 'authenticate/unauthorized.html')

def validate_field(field, condition, error_message, errors):
    if field == condition:
        errors.append(error_message)
        
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
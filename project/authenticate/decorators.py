from django.http        import HttpResponse
from django.shortcuts   import redirect

def unauthenticated_account(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 'customer':
                return redirect('/customer/dashboard')
            elif request.user.role == 'seller': 
                return redirect('/seller/dashboard')
            elif request.user.role == 'admin': 
                return redirect('/moderator/dashboard')
            else:
                return HttpResponse('Invalid account role')
        else:
            return view_function(request, *args, **kwargs)
    
    return wrapper_function

def allowed_account(allowed_roles=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):

            role = request.user.role
            email_verified = request.user.email_verified
            
            if not email_verified:
                return redirect('/auth/activate-email-sent')
            
            if role not in allowed_roles:
                return redirect('/auth/unauthorized')
            
            return view_function(request, *args, **kwargs)
        
        return wrapper_function
    return decorator
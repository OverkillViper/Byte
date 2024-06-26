from django          import forms
from accounts.models import Account

class registerForm(forms.ModelForm):
    class Meta:
        model = Account
        
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
        ]
        
        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-input', 'id' : 'first_name'}),
            'last_name'  : forms.TextInput(attrs={'class' : 'form-input', 'id' : 'last_name'}),
            'email'      : forms.TextInput(attrs={'class' : 'form-input', 'id' : 'email'}),
            'phone'      : forms.TextInput(attrs={'class' : 'form-input', 'id' : 'phone'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['email'].initial = self.instance.email
            self.fields['phone'].initial = self.instance.phone
            
class loginForm(forms.ModelForm):
    class Meta:
        model = Account
        
        fields = [
            "email",
            "password"
        ]
        
        widgets = {
            'email'     : forms.TextInput(attrs={'class' : 'form-input', 'id' : 'email'}),
            'password'  : forms.TextInput(attrs={'class' : 'form-input', 'id' : 'password'}),
        }
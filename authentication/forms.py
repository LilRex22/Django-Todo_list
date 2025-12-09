from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from todoApp.models import Todo


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        for field in self.fields:
            self.fields[field].help_text = None
            # Suppress the 'This field is required.' error message
            # self.fields[field].error_messages['required'] = ''
            
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['content',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})    
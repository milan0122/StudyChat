from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room,User
#from django.contrib.auth.models import User
#for registration
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']

#Form for rooms
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields='__all__'    #creating form with all field
        exclude=['host','participants'] # not include this one

#for profile 
class UserForm(ModelForm):
    class Meta:
        model = User # builtin model 
        fields = ['avatar','name','username','email','bio'] #include only these
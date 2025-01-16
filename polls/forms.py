from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields='__all__'    #creating form with all field
        exclude=['host','participants'] # not include this one

class UserForm(ModelForm):
    class Meta:
        model = User # builtin model 
        fields = ['username','email'] #include only these
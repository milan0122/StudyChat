from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields='__all__'    #creating form with all field
        exclude=['host','participants']
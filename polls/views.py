from django.shortcuts import render
from django.http import HttpResponse


rooms=[
    {'id':'1','name':'milan'},
     {'id':'2','name':'samir'},
      {'id':'3','name':'sabita'},
       {'id':'4','name':'aarosi'},
]

def home(request):
    context = {'room':rooms}
    return render(request,'home.html',context)
def room(request):
   return render(request,"room.html")
# Create your views here.

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

# rooms=[
#     {'id':'1','name':'Learn django with Me'},
#     {'id':'2','name':'Data Warehousing and Data Mining'},
#     {'id':'3','name':'Advanced Java Programming'},
#     {'id':'4','name':'Self scalling'},
# ]

def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request,'polls/home.html',context)

def room(request,id):  
    rm = None
    # for r in rooms:
    #     if r['id'] == id:
    #        rm = r
    # if rm is None:
    #     return HttpResponse("Room not found",status=404)
    room = Room.objects.get(id =id)
    context = {'room':room}  
    return render(request,"polls/room.html",context)

def create_room(request):
    form = RoomForm()
    if request.method =='POST':
       #add data to form
       form = RoomForm(request.POST)
       #check valid
       if form.is_valid():
           #save if valid
           form.save()
           #redirect to home
           return redirect('home')
    context ={'form':form}
    return render(request,"polls/room_form.html",context)

def updateRoom(request,id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    context = {'form':form}
    return render(request,'polls/room_form.html',context)
    

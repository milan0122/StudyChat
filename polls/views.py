from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic,Message
from .forms import RoomForm, UserForm



# rooms=[
#     {'id':'1','name':'Learn django with Me'},
#     {'id':'2','name':'Data Warehousing and Data Mining'},
#     {'id':'3','name':'Advanced Java Programming'},
#     {'id':'4','name':'Self scalling'},
# ]
def loginPage(request):
    page ='login'
    #if already user authenticated then login_url will not works
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username =request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"username or password invalids")
        except:
            messages.error(request,"user doesn't exits")
        
    context = {'page':page}
    return render(request,'polls/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')
def registerUser(request):
    page ='register'
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occured during registration")
    # context = {'page':page}
    return render(request,'polls/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    #when parameter available it searches using q(param)
    #here using default model "Q" we can do dynamic searching ie. multiple searching
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )
    topics = Topic.objects.all()
    room_counts = rooms.count()
    # room_message = Message.objects.all().order_by('-created')
    #instead of ordering here, i apply it on the model
    room_message = Message.objects.filter(Q(
        room__topic__name__icontains=q
    ))

    context = {'rooms':rooms,'topics':topics,'room_counts':room_counts,'room_message':room_message}
    return render(request,'polls/home.html',context)

def room(request,id):  
    rm = None
    # for r in rooms:
    #     if r['id'] == id:
    #        rm = r
    # if rm is None:
    #     return HttpResponse("Room not found",status=404)
    room = Room.objects.get(id =id)
    # room_messages = room.message_set.all().order_by('-created')
    room_messages = room.message_set.all()
    #for many to one relationship , use object_set.all
    #for many to many relationship, simply use object.all
    #if need all the attribute of entity simple use object.all
    #if not replace object by actual attribute of entity to access specific attribute
    participants = room.participants.all()
    if request.method=='POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',id=room.id,)
    
    context = {'room':room,'room_messages':room_messages,'participants':participants}  
    return render(request,"polls/room.html",context)

def userProfile(request,id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'topics':topics,
               'room_message':room_message}
    return render(request,'polls/profile.html',context)
    
@login_required(login_url='login') # decorators provide functionality when user wann to create room there need to be login 
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method =='POST':
       #add data to form
       topic_name = request.POST.get('topic')
       #topic,create ensure that it show the topic if user want to talk in same topic
       #but it make also possible when user want to talk on new topic, it create the room with new topic and add it into list,
       #when user want to talk same topic , then it shows
       topic,created = Topic.objects.get_or_create(name=topic_name)
       Room.objects.create(
           host = request.user,
           topic= topic,
           name= request.POST.get('name'),
           description= request.POST.get('description')
       )
       return redirect('home')
    #    form = RoomForm(request.POST)
    #    #check valid
    #    if form.is_valid():
    #        #save if valid
    #        room=form.save(commit=False)
    #        room.host=request.user #it save the host automatically
    #        room.save()
    #        #redirect to home
           
    context ={'form':form,'topics':topics}
    return render(request,"polls/room_form.html",context)

@login_required(login_url='login') # decorators provide functionality when user wann to create room there need to be login 
def updateRoom(request,id):
    room = Room.objects.get(id=id)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)
    #this restricted the user to update other message
    if request.user !=room.host:
        return HttpResponse("You are not allowed to here!!")
    if request.method=='POST':
         topic_name = request.POST.get('topic')
         topic,created = Topic.objects.get_or_create(name=topic_name)
         room.name = request.POST.get('name')
         room.topic = topic
         room.description= request.POST.get('description')
         room.save()
        # form = RoomForm(request.POST,instance=room)
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
        # else:
        #     return HttpResponse("form not valid")
         return redirect('home')
    context = {'form':form,'topics':topics,'room':room}
    return render(request,'polls/room_form.html',context)

#delete operation
@login_required(login_url='login') # decorators provide functionality when user wann to create room there need to be login 
def deleteRoom(request,id):
    room = Room.objects.get(id=id)
    if request.user !=room.host:
        return HttpResponse("You are not allowed to here!!")
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'polls/delete_room.html',{'obj':room})

@login_required(login_url='login') # decorators provide functionality when user wann to create room there need to be login 
def deleteMessage(request,id):
    msg = Message.objects.get(id=id)
    if request.user !=msg.user:
        return HttpResponse("You are not allowed to here!!")
    if request.method=='POST':
        msg.delete()
        return redirect('home')
    return render(request,'polls/delete_room.html',{'obj':msg})
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    forms = UserForm(instance=user)
    if request.method == "POST":
        forms = UserForm(request.POST,instance=user)
        if forms.is_valid():
            forms.save()
            return redirect('home')
    context={'forms':forms}
    return render(request,'polls/update-user.html',context)


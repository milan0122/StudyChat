from rest_framework.decorators import api_view
from rest_framework.response import Response
from polls.models import Room
from .serializers import RoomSerializer
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms', # api to see rooms
        'GET /api/rooms/:id'
    ]
    return Response(routes)

#sent reponse for all
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    # many = True means, serialize the all objects
    serializer = RoomSerializer(rooms,many=True)
    return Response(serializer.data)

#sent reponse for specific id
@api_view(['GET'])
def getRoom(request,id):
    room = Room.objects.get(id=id)
    # many = True means, serialize the all objects
    serializer = RoomSerializer(room,many=True)
    return Response(serializer.data)
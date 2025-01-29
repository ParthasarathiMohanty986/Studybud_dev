from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from . serializers import RoomSerializer

# Define your available API routes
routes = [
    'GET /api',
    'GET /api/rooms',
    'GET /api/rooms/:id'
]

# Define the view function with the @api_view decorator
@api_view(['GET'])  # Restrict to GET requests
def getRoutes(request):
    return Response(routes)  # Use Response instead of JsonResponse


@api_view(['GET'])  # Restrict to GET requests
def getRooms(request):
    rooms=Room.objects.all()
    serializer=RoomSerializer(rooms,many=True)
    return Response(serializer.data)  # Use Response instead of JsonResponse

@api_view(['GET'])  # Restrict to GET requests
def getRoom(request,pk):
    room=Room.objects.get(id=pk)
    serializer=RoomSerializer(room,many=False)
    return Response(serializer.data)  # Use Response instead of JsonResponse

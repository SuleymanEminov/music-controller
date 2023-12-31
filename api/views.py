from django.shortcuts import render
from rest_framework import generics, status
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'
    
    def get(self,request,format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if room.exists():
                # return room
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                # return response
                return Response(data, status=status.HTTP_200_OK)
            # return error
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)
        # return error
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    lookup_url_kwarg = 'code'

    def post(self,request,format='None'):
        if not self.request.session.exists(request.session.session_key):
            # create a session
            request.session.create()

        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            # get room
            room_result = Room.objects.filter(code=code)
            if room_result.exists():
                # get room
                room = room_result[0]
                # set session
                self.request.session['room_code'] = code
                # return response
                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)
            # return error
            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)
        
        # return error
        return Response({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not request.session.exists(request.session.session_key):
            # create a session
            request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # get data from serializer
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            # get session key
            host = request.session.session_key
            # check if room exists
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                # update room
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                # save room
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                # set session
                self.request.session['room_code'] = room.code
                # return response
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                # create room
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                # save room
                room.save()
                # set session
                self.request.session['room_code'] = room.code
                # return response
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        # return error
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
    
class UserInRoom(APIView):
    def get(self,request,format=None):
        if not self.request.session.exists(request.session.session_key):
            # create a session
            request.session.create()
        # get session key
        data = {
            'code': self.request.session.get('room_code')
        }
        # return response
        return Response(data, status=status.HTTP_200_OK)
    

class LeaveRoom(APIView):
    def post(self,request,format=None):
        if 'room_code' in self.request.session:
            # delete session
            self.request.session.pop('room_code')
            # get session key
            host_id = self.request.session.session_key
            # get room
            room_results = Room.objects.filter(host=host_id)
            if room_results.exists():
                # get room
                room = room_results[0]
                # delete room
                room.delete()
        # return response
        return Response({'Message': 'Success'}, status=status.HTTP_200_OK)
    

class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer
    def patch(self,request,format=None):
        if not self.request.session.exists(request.session.session_key):
            # create a session
            request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            # get session key
            code = serializer.data.get('code')
            # get room
            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                # return error
                return Response({'msg': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
            # get room
            room = queryset[0]
            # get session key
            user_id = self.request.session.session_key
            # check if user is host
            if room.host != user_id:
                # return error
                return Response({'msg': 'You are not the host of this room'}, status=status.HTTP_403_FORBIDDEN)
            # update room
            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            # save room
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            # return response
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        # return error
        return Response({'Bad Request': 'Invalid Data...'}, status=status.HTTP_400_BAD_REQUEST)
    

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.http import Http404
from rest_framework.response import Response
from .models import AthleteProfile, Pledge, ProgressUpdate, Badge
from .serializers import AthleteProfileSerializer, PledgeSerializer, ProgressUpdateSerializer, BadgeSerializer, AthleteProfileDetailSerializer, PledgeDetailSerializer
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly
from projects.models import Pledge, AthleteProfile


class AthleteProfileCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(f"User making the request: {request.user}")
        data = request.data
        data['owner'] = request.user.id  # Automatically assign the logged-in user as the owner
        serializer = AthleteProfileSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# AthleteProfile Views
class AthleteProfileList(APIView):
    authentication_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create

    def get(self, request):
        profiles = AthleteProfile.objects.all()
        serializer = AthleteProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Automatically set the owner to the logged-in user
        data = request.data
        data['owner'] = request.user.id  # Assign the user ID to the 'owner' field

        serializer = AthleteProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AthleteProfileDetail(APIView): #lows retrieving, updating, and deleting specific athlete profiles (GET, PUT, DELETE).
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            profile = AthleteProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except AthleteProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = AthleteProfileDetailSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = AthleteProfileDetailSerializer(
            instance=profile,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Pledge Views
class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)  # Assign the logged-in user as the supporter
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PledgeDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSupporterOrReadOnly
    ]

    def get_object(self, pk):
        try:
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(pledge)
        return Response(serializer.data)

    def put(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(
            instance=pledge,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ProgressUpdate Views
class ProgressUpdateList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        updates = ProgressUpdate.objects.all()
        serializer = ProgressUpdateSerializer(updates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProgressUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProgressUpdateDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            update = ProgressUpdate.objects.get(pk=pk)
            return update
        except ProgressUpdate.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        update = self.get_object(pk)
        serializer = ProgressUpdateSerializer(update)
        return Response(serializer.data)

    def put(self, request, pk):
        update = self.get_object(pk)
        serializer = ProgressUpdateSerializer(
            instance=update,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        update = self.get_object(pk)
        update.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BadgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        badges = Badge.objects.all()
        serializer = BadgeSerializer(badges, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Only authenticated users can post (this is handled by the permission_classes)
        serializer = BadgeSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BadgeDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Only authenticated users can update

    def get_object(self, pk):
        try:
            return Badge.objects.get(pk=pk)
        except Badge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # Retrieve a specific badge
        badge = self.get_object(pk)
        serializer = BadgeSerializer(badge)
        return Response(serializer.data)

    def put(self, request, pk):
        # Update an existing badge
        badge = self.get_object(pk)
        serializer = BadgeSerializer(badge, data=request.data, partial=True)  # partial=True allows partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
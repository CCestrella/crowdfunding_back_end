from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.http import Http404
from rest_framework.response import Response
from .models import AthleteProfile, Pledge, ProgressUpdate
from .serializers import (
    AthleteProfileSerializer,
    PledgeSerializer,
    ProgressUpdateSerializer,
    AthleteProfileDetailSerializer,
    PledgeDetailSerializer,ProgressUpdateSerializer
)
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.core.exceptions import ValidationError


# Athlete Profile Views
class AthleteProfileCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Only users with 'athlete' or 'both' roles can create profiles
        if request.user.role not in ['athlete', 'both']:
            return Response({"error": "You do not have permission to create an athlete profile."},
                            status=status.HTTP_403_FORBIDDEN)

        print(f"User making the request: {request.user}")
        data = request.data
        data['owner'] = request.user.id  # Automatically assign the logged-in user as the owner
        serializer = AthleteProfileSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AthleteProfileDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            profile = AthleteProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except AthleteProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = AthleteProfileDetailSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)

        # Ensure only 'athlete' or 'both' roles can update profiles
        if request.user.role not in ['athlete', 'both']:
            return Response({"error": "You do not have permission to edit this profile."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = AthleteProfileDetailSerializer(
            instance=profile,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AthleteProfileList(APIView):
    def get(self, request):
        athletes = AthleteProfile.objects.all()
        serializer = AthleteProfileSerializer(athletes, many=True)
        return Response(serializer.data)

# Pledge Views
class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        # Ensure only 'donor' or 'both' roles can create pledges
        if request.user.role not in ['donor', 'both']:
            return Response({"error": "You do not have permission to make pledges."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            print("Incoming request data:", request.data)
            serializer = PledgeSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                serializer.save(supporter=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Unexpected Error:", str(e))
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PledgeDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSupporterOrReadOnly]

    def get_object(self, pk):
        try:
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(pledge, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(
            instance=pledge,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProgressUpdateList(APIView):
    def get(self, request):
        updates = ProgressUpdate.objects.all()
        serializer = ProgressUpdateSerializer(updates, many=True)
        return Response(serializer.data)

class ProgressUpdateDetail(APIView):
    def get_object(self, pk):
        try:
            return ProgressUpdate.objects.get(pk=pk)
        except ProgressUpdate.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        update = self.get_object(pk)
        serializer = ProgressUpdateSerializer(update)
        return Response(serializer.data)
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.core.exceptions import ValidationError
from .models import AthleteProfile, Pledge, ProgressUpdate
from .serializers import (
    AthleteProfileSerializer,
    PledgeSerializer,
    ProgressUpdateSerializer,
    AthleteProfileDetailSerializer,
    UserSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly


# Sign-Up View
class SignUpView(APIView):
    """
    Handles user registration (sign-up).
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Athlete Profile Views
class AthleteProfileCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.role not in ['athlete', 'both']:
            return Response(
                {"error": "You do not have permission to create an athlete profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        data['owner'] = request.user.id
        serializer = AthleteProfileSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AthleteProfileList(APIView):
    def get(self, request):
        athletes = AthleteProfile.objects.all()
        serializer = AthleteProfileDetailSerializer(athletes, many=True)
        return Response(serializer.data)


class UserAthletesList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        athletes = AthleteProfile.objects.filter(owner=request.user)
        serializer = AthleteProfileDetailSerializer(athletes, many=True)
        return Response(serializer.data)


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
        serializer = AthleteProfileDetailSerializer(
            instance=profile,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        if serializer.is_valid():
            updated_profile = serializer.save()
            return Response(AthleteProfileDetailSerializer(updated_profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            profile = AthleteProfile.objects.get(pk=pk)
            if profile.owner != request.user:
                return Response(
                    {"detail": "You do not have permission to delete this profile."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AthleteProfile.DoesNotExist:
            raise Http404


# Pledge Views
class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        if request.user.role not in ['donor', 'both']:
            return Response(
                {"error": "You do not have permission to make pledges."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PledgeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = PledgeSerializer(pledge, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(
            instance=pledge,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Progress Update Views
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


class UserAthleteDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return AthleteProfile.objects.get(pk=pk)
        except AthleteProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        athlete = self.get_object(pk)
        serializer = AthleteProfileSerializer(athlete)
        return Response(serializer.data)

    def delete(self, request, pk):
        athlete = self.get_object(pk)
        athlete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

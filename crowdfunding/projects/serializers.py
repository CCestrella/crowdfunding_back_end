from rest_framework import serializers
from .models import AthleteProfile, Pledge, ProgressUpdate
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'role']
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be readable in responses
        }

    def validate(self, data):
        required_fields = ['username', 'password', 'first_name', 'last_name', 'email', 'role']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError({field: f'{field} is required.'})

        allowed_roles = ['athlete', 'donor', 'both']
        if data.get('role') not in allowed_roles:
            raise serializers.ValidationError({'role': f"Role must be one of {', '.join(allowed_roles)}."})

        return data

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


# Pledge Serializer
class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField(source='supporter.id')
    athlete_profile = serializers.PrimaryKeyRelatedField(queryset=AthleteProfile.objects.all())

    class Meta:
        model = Pledge
        fields = '__all__'

    def validate(self, data):
        # Check if the user's role is allowed to create a pledge
        if self.context['request'].user.role not in ['donor', 'both']:
            raise serializers.ValidationError(
                "Please log in as a donor to make a pledge."
            )
        
        # Check if the campaign is still open
        if not data['athlete_profile'].is_open:
            raise serializers.ValidationError(
                "Sorry, this campaign is no longer accepting donations."
            )
        
        return data


# Progress Update Serializer
class ProgressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressUpdate
        fields = ['id', 'athlete_profile', 'title', 'content', 'date_posted']
        read_only_fields = ['date_posted']

    def create(self, validated_data):
        return ProgressUpdate.objects.create(**validated_data)


# Athlete Profile Serializer
class AthleteProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = AthleteProfile
        fields = [
            'id', 'first_name', 'last_name', 'bio', 'age', 'sport', 'goal',
            'funds_raised', 'is_open', 'funding_breakdown', 'achievements',
            'image', 'video', 'progress_updates', 'owner'
        ]



# Athlete Profile Detail Serializer
class AthleteProfileDetailSerializer(serializers.ModelSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    updates = ProgressUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = AthleteProfile
        fields = [
            'id', 'first_name', 'last_name', 'bio', 'age', 'sport', 'goal',
            'funds_raised', 'is_open', 'funding_breakdown', 'achievements',
            'image', 'video', 'progress_updates', 'owner', 'pledges', 'updates'
        ]

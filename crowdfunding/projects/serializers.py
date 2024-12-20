from rest_framework import serializers
from .models import AthleteProfile, Pledge, ProgressUpdate
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

CustomUser = get_user_model()

# User Serializer
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'role']
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be readable in responses
        }

    def validate(self, data):
        """
        Validate the incoming payload to ensure all required fields are valid.
        """
        required_fields = ['username', 'password', 'first_name', 'last_name', 'email', 'role']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError({field: f'{field} is required.'})

        # Validate role field to ensure it matches allowed roles
        allowed_roles = ['athlete', 'donor', 'both']
        if data.get('role') not in allowed_roles:
            raise serializers.ValidationError({'role': f"Role must be one of {', '.join(allowed_roles)}."})

        return data

    def create(self, validated_data):
        """
        Create a new user using the validated payload.
        """
        # Use create_user to ensure password hashing
        user = CustomUser.objects.create_user(**validated_data)
        return user



# Pledge Serializer
class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField(source='supporter.id')
    athlete_profile = serializers.PrimaryKeyRelatedField(queryset=AthleteProfile.objects.all())

    class Meta:
        model = Pledge
        fields = '__all__'

    def validate(self, data):
        # Check that only 'donor' or 'both' roles can make pledges
        if self.context['request'].user.role not in ['donor', 'both']:
            raise serializers.ValidationError("You do not have permission to create a pledge.")
        if not data['athlete_profile'].is_open:
            raise serializers.ValidationError("This campaign is closed for pledging.")
        return data


# Pledge Detail Serializer
class PledgeDetailSerializer(PledgeSerializer):
    class Meta(PledgeSerializer.Meta):
        fields = PledgeSerializer.Meta.fields


# Athlete Profile Serializer
class AthleteProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = AthleteProfile
        fields = ['id', 'first_name', 'last_name', 'bio', 'age', 'sport', 'goal', 'funds_raised', 'owner']


# Athlete Profile Detail Serializer
class AthleteProfileDetailSerializer(AthleteProfileSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    class Meta:
        model = AthleteProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        # Check if the user role is 'athlete' or 'both'
        request = self.context['request']
        if request.user.role not in ['athlete', 'both']:
            raise serializers.ValidationError("You do not have permission to edit this profile.")

        # Update fields only if the user is allowed
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.age = validated_data.get('age', instance.age)
        instance.sport = validated_data.get('sport', instance.sport)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.funds_raised = validated_data.get('funds_raised', instance.funds_raised)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.funding_breakdown = validated_data.get('funding_breakdown', instance.funding_breakdown)
        instance.achievements = validated_data.get('achievements', instance.achievements)
        instance.image = validated_data.get('image', instance.image)
        instance.video = validated_data.get('video', instance.video)
        instance.progress_updates = validated_data.get('progress_updates', instance.progress_updates)
        instance.save()
        return instance


# Progress Update Serializer
class ProgressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressUpdate
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.date_posted = validated_data.get('date_posted', instance.date_posted)
        instance.save()
        return instance

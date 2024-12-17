from rest_framework import serializers
from .models import AthleteProfile, Pledge, ProgressUpdate, Badge


# Pledge Serializer
class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField(source='supporter.id')

    class Meta:
        model = Pledge
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.is_fulfilled = validated_data.get('is_fulfilled', instance.is_fulfilled)
        instance.save()
        return instance


# Pledge Detail Serializer (for more detailed information)
class PledgeDetailSerializer(PledgeSerializer):
    class Meta(PledgeSerializer.Meta):
        fields = PledgeSerializer.Meta.fields  # Inherit fields from PledgeSerializer

    # No need to nest pledges, as a pledge doesn't contain other pledges.


# Athlete Profile Serializer
class AthleteProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # Read-only field to show the username of the owner

    class Meta:
        model = AthleteProfile
        fields = ['id', 'first_name', 'last_name', 'bio', 'age', 'sport', 'goal', 'funds_raised', 'owner']


# Athlete Profile Detail Serializer (includes pledges)
class AthleteProfileDetailSerializer(AthleteProfileSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)  # Nested pledges

    class Meta:
        model = AthleteProfile
        fields = '__all__'

    def update(self, instance, validated_data):
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


# Badge Serializer
class BadgeSerializer(serializers.ModelSerializer):
    supporters = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Badge
        fields = '__all__'

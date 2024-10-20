from rest_framework import serializers
from django.apps import apps


class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField(source='supporter.id')

    class Meta:
        model = apps.get_model('projects.Pledge')
        fields = '__all__'


    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = apps.get_model('projects.Project')
        fields = '__all__'

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

def update(self, instance, validated_data):
    instance.title = validated_data.get('title', instance.title)
    instance.description = validated_data.get('description', instance.description)
    instance.goal = validated_data.get('goal', instance.goal)
    instance.image = validated_data.get('image', instance.image)
    instance.is_open = validated_data.get('is_open', instance.is_open)
    instance.date_created = validated_data.get('date_created', instance.date_created)
    instance.owner = validated_data.get('owner', instance.owner)
    instance.save()
    return instance

class PledgeDetailSerializer(PledgeSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

def update(self, instance, validated_data):
    instance.title = validated_data.get('title', instance.title)
    instance.description = validated_data.get('description', instance.description)
    instance.goal = validated_data.get('goal', instance.goal)
    instance.image = validated_data.get('image', instance.image)
    instance.is_open = validated_data.get('is_open', instance.is_open)
    instance.date_created = validated_data.get('date_created', instance.date_created)
    instance.owner = validated_data.get('owner', instance.owner)
    instance.save()
    return instance

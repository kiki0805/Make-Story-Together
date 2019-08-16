from rest_framework import serializers
from .models import Story, Tag
from writers.serializers import InfoSerializer
from writers.models import Writer
from groups.models import Group

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
    

class StorySerializer(serializers.ModelSerializer):
    maintainer = serializers.CharField(source='maintainer.name', required=False)
    creator = serializers.CharField(source='creator.screen_name')

    class Meta:
        model = Story
        fields = ['id', 'title', 'creator', 'maintainer', 'category', 'public', ]

    def validate_creator(self, value):
        user =  self.context['request'].user
        if user.account.screen_name == value:
            return value
        raise serializers.ValidationError(f"Invalid operation.")
    
    def validate_maintainer(self, value):
        user =  self.context['request'].user
        qs = Group.objects.filter(name=value)
        if not qs.exist():
            raise serializers.ValidationError(f"Wrong group name.")
        elif qs[0].owner != user:
            raise serializers.ValidationError(f"Not the owner.")
        return value

    def create(self, validated_data):
        creator = Writer.objects.get(screen_name=validated_data['creator']['screen_name'])
        story = Story.objects.create(title=validated_data['title'], creator=creator)
        return story

class StoryDetailSerializer(serializers.ModelSerializer):
    maintainer = serializers.CharField(source='maintainer.name', required=False)
    creator = serializers.CharField(source='creator.screen_name')

    class Meta:
        model = Story
        fields = ['id', 'title', 'creator', 'maintainer', 'category', 'public', 'plots_count', 'created_at']


class StoryMoreDetailSerializer(serializers.ModelSerializer):
    participators = InfoSerializer(many=True)
    maintainer = serializers.CharField(source='maintainer.name', required=False)
    creator = serializers.CharField(source='creator.screen_name')

    class Meta:
        model = Story
        fields = ['id', 'title', 'creator', 'maintainer', 'category', 'public', 'plots_count', 'rule', 'created_at', 'participators']

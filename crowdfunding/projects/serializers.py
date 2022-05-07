from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from django.db.models import Sum
from .models import Project, Pledge, Category, Comment


class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    date_start = serializers.DateTimeField()
    date_ending = serializers.DateTimeField()
    owner = serializers.ReadOnlyField(source='owner.id')
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    total_pledged = serializers.SerializerMethodField()

    def get_total_pledged(self, obj):
        return Project.objects.filter(pk=obj.id).annotate(
            total_pledged=Sum('pledges__amount')
        )[0].total_pledged

    def create(self, validated_data):
        return Project.objects.create(**validated_data)


class CategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    category_name = serializers.CharField(max_length=50)
    slug = serializers.SlugField() 

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username",read_only="true",)

    class Meta:
        model = Comment
        exclude = ['visible']


class ProjectCommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only="true",)

    class Meta:
        model = Comment
        exclude = ["visible", "project"]


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    date_created = serializers.ReadOnlyField()
    supporter = serializers.ReadOnlyField(source='supporter.id')
    project_id = serializers.IntegerField()
    
    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)


class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.date_start = validated_data.get('date_start', instance.date_start)
        instance.date_ending = validated_data.get('date_ending', instance.date_ending)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

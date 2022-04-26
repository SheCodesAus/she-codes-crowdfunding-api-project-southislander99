from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Badge, CustomUser


class BadgeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Badge
        fields = ['id', 'image', 'description', 'badge_type', 'badge_goal']

class BadgeDetailSerializer(BadgeSerializer):
        def update(self, instance, validated_data):
            instance.image = validated_data.get('image',instance.image)
            instance.description = validated_data.get('description',instance.description)
            instance.badge_type = validated_data.get('badge_type',instance.badge_type)
            instance.badge_goal = validated_data.get('badge_goal',instance.badge_goal)
            instance.save()
            return instance

class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    profile_image = serializers.URLField()
    bio = serializers.CharField(max_length=600)
    social = serializers.URLField()
    badges = BadgeSerializer(read_only=True, many=True)

    def create(self, validated_data):
          return CustomUser.objects.create(**validated_data)

class CustomUserDetailSerializer(CustomUserSerializer):
        def update(self, instance, validated_data):
            instance.username = validated_data.get('username',instance.username)
            instance.email = validated_data.get('email',instance.email)
            instance.profile_image = validated_data.get('profile_image', instance.profile_image)
            instance.bio = validated_data.get('bio', instance.bio)
            instance.social = validated_data.get('social', instance.social)
            instance.save()
            return instance


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
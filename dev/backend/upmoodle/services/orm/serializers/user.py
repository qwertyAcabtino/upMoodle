from rest_framework import serializers

from upmoodle.models import User
from upmoodle.services.orm.serializers import LevelSerializer


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
    rol = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    subjects = LevelSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'rol', 'email', 'nick', 'name', 'profilePic', 'lastTimeActive', 'joined', 'banned', 'subjects')


class UserSimpleSerializer(serializers.ModelSerializer):
    rol = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = User
        fields = ('id', 'rol', 'email', 'nick', 'name', 'profilePic', 'lastTimeActive', 'joined', 'banned')

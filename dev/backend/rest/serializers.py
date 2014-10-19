from django.forms import widgets
from rest_framework import serializers
from rest.models import NoteBoard
from rest.models import Level


class NoteBoardSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')

    class Meta:
        model = NoteBoard
        fields = ('id', 'topic', 'text', 'level')

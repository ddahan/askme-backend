from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import LetterType, Field

User = get_user_model()


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        exclude = ('created', 'modified')


class ShortLetterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LetterType
        fields = ('pk', 'purpose', 'description')


class DetailedLetterTypeSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)

    class Meta:
        model = LetterType
        fields = ('pk', 'purpose', 'fields')

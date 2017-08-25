from rest_framework import serializers

from .models import UserTeamRequest


class UserTeamRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTeamRequest
        fields = ('team',)


class UserTeamRequestListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserTeamRequest
        fields = ('datetime', 'user', 'status')

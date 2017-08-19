from rest_framework import serializers

from .models import Team


class ChallengeSolvedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name',)

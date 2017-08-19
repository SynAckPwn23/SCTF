from rest_framework import serializers

from accounts.models import Team, UserTeamRequest
from challenges.models import ChallengeSolved


class ChallengeSolverSerializer(serializers.Serializer):
    challenge = serializers.IntegerField()
    key = serializers.CharField()

    def create(self, validated_data):
        pass


class ChallengeSolvedSerializer(serializers.ModelSerializer):
    key = serializers.CharField()

    class Meta:
        model = ChallengeSolved
        fields = ('challenge', 'key')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name',)


class UserTeamRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTeamRequest
        fields = ('team', 'id',)
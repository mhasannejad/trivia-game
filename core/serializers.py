from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from authentication.models import User
from core.models import Challenge, Question, Option, Subject


class UserSerializerLite(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class UserSerializerWithStats(ModelSerializer):
    stats = serializers.ReadOnlyField()
    points = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'stats', 'points']


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title']


class ChallengeSerializerList(ModelSerializer):
    creator = UserSerializerLite()
    joiner = UserSerializerLite()
    subject = SubjectSerializer()

    class Meta:
        model = Challenge
        fields = ['id', 'creator','joiner', 'subject', 'created_at']


class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']


class QuestionSerializerFull(ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'options']


class ChallengeSerializerFull(ModelSerializer):
    creator = UserSerializerLite()
    joiner = UserSerializerLite()
    questions = QuestionSerializerFull(many=True)

    class Meta:
        model = Challenge
        fields = ['id', 'creator', 'joiner', 'questions', 'created_at']


class ChallengeSerializerResult(ModelSerializer):
    creator = UserSerializerLite()
    joiner = UserSerializerLite()
    result = serializers.ReadOnlyField()

    class Meta:
        model = Challenge
        fields = ['id', 'creator', 'joiner', 'result', 'created_at']

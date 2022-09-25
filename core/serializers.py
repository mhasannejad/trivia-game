from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from authentication.models import User
from core.models import Challenge, Question, Option, Subject, Level


class UserSerializerLite(ModelSerializer):
    symbol_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'symbol_name']


class UserSerializerWithStats(ModelSerializer):
    stats = serializers.ReadOnlyField()
    points = serializers.ReadOnlyField()
    level = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'stats', 'points', 'symbol_name', 'level']


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
        fields = ['id', 'creator', 'joiner', 'subject', 'created_at', 'private']


class ChallengeSerializerListForUser(ModelSerializer):
    creator = UserSerializerLite()
    joiner = UserSerializerLite()
    subject = SubjectSerializer()

    class Meta:
        model = Challenge
        fields = ['id', 'creator', 'joiner', 'subject', 'created_at', 'private', 'invitation_code']


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


class LevelSerializer(ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

# Create your views here.
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import *
from core.serializers import *


def default(request):
    pass


@api_view(['GET'])
def all_subjects(request):
    return Response(SubjectSerializer(Subject.objects.all(), many=True).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_available_challenges(request):
    return Response(
        ChallengeSerializerList(Challenge.objects.filter(joiner__isnull=True).order_by('-id'), many=True).data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_challenges_for_user(request):
    return Response(
        ChallengeSerializerList(Challenge.objects.filter(joiner__isnull=True).filter(~Q(creator=request.user)).order_by('-id'), many=True).data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_challenges(request):
    return Response(
        ChallengeSerializerList(reversed(request.user.challenges), many=True).data
    )


@api_view(['POST'])
def create_question(request):
    subject = Subject.objects.get(id=request.data['subject_id'])
    question = Question.objects.create(
        text=request.data['text'],
        subject=subject
    )
    for i in request.data['options']:
        option = Option.objects.create(text=i['text'])
        question.options.add(
            option
        )
        if i['is_right']:
            question.right_answer = option
            question.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_challenge(request):
    questions = Question.objects.filter(subject_id=request.data['subject_id']).order_by('?')[:5]
    challenge = Challenge.objects.create(
        creator=request.user,
        subject_id=request.data['subject_id']
    )
    challenge.questions.set(questions)

    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def challenge_someone(request):
    challenge = Challenge.objects.create(
        creator=request.user,
        subject_id=request.data['subject_id'],
        joiner_id=request.data['joiner_id']
    )

    subject = Subject.objects.get(id=request.data['subject_id'])

    questions = Question.objects.filter(subject=subject).order_by('?')[:5]
    print(questions)
    for i in questions:
        challenge.questions.add(i)

    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_challenge(request):
    challenge = Challenge.objects.get(id=request.data['challenge_id'])

    challenge.joiner = request.user
    challenge.save()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_challenge_result(request):
    return Response(
        ChallengeSerializerResult(
            list(map(lambda x: len(x.answers) == 10, Challenge.objects.all()))
        ).data
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_results(request):
    return Response(
        ChallengeSerializerResult(
            list(filter(lambda x: len(x.useranswersubmit_set.all()) == 10, request.user.challenges)), many=True
        ).data
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request):
    challenge = Challenge.objects.get(id=request.data['challenge_id'])
    question = Question.objects.get(id=request.data['question_id'])
    option = Option.objects.get(id=request.data['option_id'])

    if challenge.id not in list(map(lambda x: x.id, request.user.challenges)):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    if question.id not in list(map(lambda x: x.id, challenge.questions.all())):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    if option.id not in list(map(lambda x: x.id, question.options.all())):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    _, created = UserAnswerSubmit.objects.get_or_create(
        question=question,
        challenge=challenge,
        option=option,
        user=request.user
    )

    if not created:
        return Response(status=status.HTTP_208_ALREADY_REPORTED)
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_challenge_details(request, id):
    challenge = Challenge.objects.get(id=id)
    questions = list(map(lambda x: x[0], challenge.questions.values_list('id')))
    user_submitted_answers = UserAnswerSubmit.objects.filter(
        user=request.user,
        challenge_id=challenge.id,
    )

    user_submitted_answers = list(map(lambda x: x[0], user_submitted_answers.values_list('question_id')))
    to_be_sent_ids = list(set(list(questions)) - set(list(user_submitted_answers)))
    questions = Question.objects.filter(id__in=to_be_sent_ids)
    print(request.user.id)
    if challenge.id not in list(map(lambda x: x.id, request.user.challenges)):
        print(list(map(lambda x: x.id, request.user.challenges)))
        return Response(status=status.HTTP_409_CONFLICT)
    if len(questions) == 0:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    object_to_send = {
        'id': challenge.id,
        'creator': UserSerializerLite(challenge.creator).data,
        'joiner': UserSerializerLite(challenge.joiner).data,
        'subject': SubjectSerializer(challenge.subject).data,
        'questions': QuestionSerializerFull(questions, many=True).data
    }
    return Response(object_to_send, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_ranking(request):
    return Response(
        UserSerializerWithStats(
            sorted(User.objects.all(), key=lambda x: x.points, reverse=True), many=True
        ).data
    )

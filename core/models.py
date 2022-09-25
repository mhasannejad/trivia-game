from django.apps import apps
from django.db import models
# Create your models here.
from unixtimestampfield import UnixTimeStampField

from authentication.models import User


class Subject(models.Model):
    title = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=255)
    right_answer = models.ForeignKey('Option', on_delete=models.SET_NULL, null=True, related_name='right_option')
    # challenge = models.ManyToManyField(Challenge, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)


class Challenge(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    joiner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='joiner')
    questions = models.ManyToManyField('Question')
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True)
    created_at = UnixTimeStampField(auto_now_add=True)
    private = models.BooleanField(default=False)
    invitation_code = models.CharField(max_length=10, default='')

    @property
    def result(self):
        UserAnswerSubmitModel = apps.get_model('core', 'UserAnswerSubmit')
        creator_results = UserAnswerSubmitModel.objects.filter(
            user=self.creator,
            challenge_id=self.id
        )

        creator_final = 0
        for i in creator_results:
            if i.option.id == i.question.right_answer.id:
                creator_final += 1

        joiner_results = UserAnswerSubmitModel.objects.filter(
            user=self.joiner,
            challenge_id=self.id
        )
        joiner_final = 0
        for i in joiner_results:
            if i.option.id == i.question.right_answer.id:
                joiner_final += 1

        return {
            'creator': creator_final,
            'joiner': joiner_final
        }


class Option(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name='options')


class UserAnswerSubmit(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True, default=0)


class Level(models.Model):
    title = models.CharField(max_length=255, default='')
    icon = models.ImageField(upload_to='levels', default='')
    min_points = models.IntegerField(default=0)

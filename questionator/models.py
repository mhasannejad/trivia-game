from django.db import models

# Create your models here.
from authentication.models import User
from leitner.models import Daroo


class QCategory(models.Model):
    name = models.TextField(max_length=500, default='')


class Questionate(models.Model):
    title = models.TextField(max_length=500, default='')
    category = models.ForeignKey(QCategory, on_delete=models.CASCADE, null=True)


class Optionate(models.Model):
    questionate = models.ForeignKey(Questionate, on_delete=models.CASCADE, null=True)
    option = models.TextField(max_length=1000, default='')
    is_right = models.BooleanField(default=False)


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Questionate, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Optionate, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(default=False)
    daroo = models.ForeignKey(Daroo, on_delete=models.SET_NULL, null=True)

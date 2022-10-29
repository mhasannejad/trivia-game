from django.db import models

# Create your models here.
from authentication.models import User


class Pharma(models.Model):
    group = models.CharField(max_length=255, default=None, null=True)
    name = models.CharField(max_length=255, default=None, null=True)

    @property
    def props(self):
        return self.prop_set.all()


class Prop(models.Model):
    key = models.CharField(max_length=255, default=None, null=True)
    value = models.TextField(max_length=10000, default=None, null=True)
    pharma = models.ForeignKey(Pharma, on_delete=models.CASCADE, null=True)


class Card(models.Model):
    pharma = models.ForeignKey(Pharma, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    level = models.IntegerField(choices=(
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
    ), default=1)

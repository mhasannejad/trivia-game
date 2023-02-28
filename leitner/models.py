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


class Daroo(models.Model):
    clinicalAttentions = models.TextField(default='', null=True)
    pregnancyCategory = models.TextField(default='', null=True)
    tradeNames = models.TextField(default='', null=True)
    contraindications = models.TextField(default='', null=True)
    pregnancy = models.TextField(default='', null=True)
    treatmentCategory = models.TextField(default='', null=True)
    name = models.TextField(default='', null=True)
    pharmacologyCategory = models.TextField(default='', null=True)
    iranianGenericProducts = models.TextField(default='', null=True)
    indications = models.TextField(default='', null=True)
    pharmacoDynamics = models.TextField(default='', null=True)
    interactions = models.TextField(default='', null=True)
    sideEffects = models.TextField(default='', null=True)
    breastFeeding = models.TextField(default='', null=True)
    trainings = models.TextField(default='', null=True)
    block = models.IntegerField(default=0, null=True)
    block_combined = models.CharField(default='', null=True,max_length=25)


class FlashCard(models.Model):
    daroo = models.ForeignKey(Daroo, on_delete=models.CASCADE, null=True)
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

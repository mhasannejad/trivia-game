from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.db.models import Q

from authentication.managers import UserAccountManager


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserAccountManager()

    @property
    def challenges(self):
        Challenge = apps.get_model('core', 'Challenge')
        return Challenge.objects.filter(Q(creator=self) | Q(joiner=self))

    @property
    def completed_challenges(self):
        return list(filter(lambda x: len(x.useranswersubmit_set.all()) == 10, self.challenges))

    @property
    def stats(self):
        wins_count = 0
        loss_count = 0
        draw_count = 0
        for i in self.completed_challenges:
            if i.creator.id == self.id:
                if i.result['creator'] > i.result['joiner']:
                    wins_count += 1
                elif i.result['creator'] < i.result['joiner']:
                    loss_count += 1
                else:
                    draw_count += 1
            else:
                if i.result['creator'] > i.result['joiner']:
                    loss_count += 1
                elif i.result['creator'] < i.result['joiner']:
                    wins_count += 1
                else:
                    draw_count += 1

        return {
            'wins': wins_count,
            'losses': loss_count,
            'draws': draw_count
        }

    @property
    def points(self):
        return self.stats['wins'] * 5 + self.stats['losses'] * -1

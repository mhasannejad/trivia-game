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
    role = models.IntegerField(default=0, choices=(
        (0, 'user'),
        (1, 'moderator'),
    ))

    @property
    def symbol_name(self):
        return str(self.email).split('@')[0]

    @property
    def challenges(self):
        Challenge = apps.get_model('core', 'Challenge')
        return Challenge.objects.filter(Q(creator=self) | Q(joiner=self))

    @property
    def completed_challenges(self):
        return list(filter(lambda x: len(x.useranswersubmit_set.all()) == 10, self.challenges))

    @property
    def prescriptions_prescribed(self):
        PrescriptionModel = apps.get_model('drug', 'Prescription')
        return PrescriptionModel.objects.filter(prescriptionitem__pharmacist=self)

    @property
    def total_prescription_point(self):
        PrescriptionItemModel = apps.get_model('drug', 'PrescriptionItem')
        presitems = PrescriptionItemModel.objects.filter(
            pharmacist=self,
        )
        sum_points = sum(map(lambda x: x.point, presitems))

        return sum_points


    @property
    def correct_prescriptions_prescribed_len(self):
        return len(self.correct_prescriptions_prescribed)

    @property
    def wrong_prescriptions_prescribed_len(self):
        return len(self.wrong_prescriptions_prescribed)

    @property
    def correct_prescriptions_prescribed(self):
        corrects = []
        for i in self.prescriptions_prescribed:
            presitems = i.prescriptionitem_set.filter(pharmacist=self)
            sum_points = sum(map(lambda x: x.point, presitems))
            print(sum_points)
            print(len(presitems))
            print(sum_points / (len(presitems) * 5))
            if sum_points / (len(presitems) * 5) > 0.8:
                corrects.append(i)
        return corrects

    @property
    def wrong_prescriptions_prescribed(self):
        wrongs = []
        for i in self.prescriptions_prescribed:
            presitems = i.prescriptionitem_set.filter(pharmacist=self)
            sum_points = sum(map(lambda x: x.point, presitems))
            if sum_points / (len(presitems) * 5) < 0.8:
                wrongs.append(i)
        return wrongs

    @property
    def prescriptions_checked(self):
        PrescriptionModel = apps.get_model('drug', 'Prescription')
        return PrescriptionModel.objects.filter(prescriptionitem__prescriptionverification__verifier=self)

    @property
    def incompleted_challenges(self):
        return list(filter(lambda x: len(x.useranswersubmit_set.all()) < 10, self.challenges))

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

    def __str__(self):
        return f'{self.id} {self.email}'

    @property
    def points(self):
        return self.stats['wins'] * 5 + self.stats['losses'] * -1

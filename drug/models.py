from operator import itemgetter

from django.apps import apps
from django.db import models

from authentication.models import User


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


# Create your models here.
class Drug(models.Model):
    name = models.CharField(max_length=555, default='')


class DrugSubsets(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.SET_NULL, null=True)
    melh = models.CharField(max_length=255, default='')
    drug_form = models.CharField(max_length=255, default='')
    dose = models.CharField(max_length=255, default='')
    route_of_admin = models.CharField(max_length=255, default='')
    atc_code = models.CharField(max_length=255, default='')
    ingredient = models.CharField(max_length=255, default='')
    clinical = models.CharField(max_length=255, default='')
    access_level = models.CharField(max_length=255, default='')
    remarks = models.CharField(max_length=255, default='')
    date = models.CharField(max_length=255, default='')

    def __str__(self):
        return f'{self.drug.name} {self.drug_form} {self.dose}'


class Prescription(models.Model):
    image = models.ImageField(upload_to=upload_to)
    labeled = models.BooleanField(default=False)

    @property
    def image_url(self):
        return self.image.name

    @property
    def top_verified_label(self):
        pharmacist_point_complex = []
        PrescriptionItemModel = apps.get_model('drug', 'PrescriptionItem')
        for i in self.pharmacists:
            presitems = PrescriptionItemModel.objects.filter(
                pharmacist=i,
                prescription=self
            )
            points = 0
            for j in presitems:
                if len(j.prescriptionverification_set.all()) > 5:
                    points += j.point

            pharmacist_point_complex.append({
                'pharmacist': i,
                'points': points / (len(presitems) * 5),
                'items': presitems
            })

        pharmacist_point_complex = sorted(pharmacist_point_complex, key=itemgetter('points'))

        return pharmacist_point_complex[0]['items'] if len(pharmacist_point_complex) > 0 else []

    @property
    def unverified_prescription_items(self):
        unverified = []
        pres_items = self.prescriptionitem_set.all()
        for i in pres_items:
            if len(i.prescriptionverification_set.all()) < 5:
                unverified.append(i)
        return unverified

    @property
    def pharmacists(self):
        return User.objects.filter(id__in=list(set(map(lambda x: x.pharmacist.id, self.prescriptionitem_set.all()))))

    @property
    def checkers(self):
        verifiers = []
        for i in self.prescriptionitem_set.all():
            for j in i.prescriptionverification_set.all():
                verifiers.append(j.verifier)
        return verifiers

    def __str__(self):
        return f'checked by {len(self.pharmacists)} verified by: {len(self.checkers)} top-label-count: {len(self.top_verified_label)}'


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True)
    drug = models.ForeignKey(DrugSubsets, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(null=True)
    per_time = models.CharField(max_length=255, null=True)
    pharmacist = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trading_name = models.CharField(max_length=255, null=True,default='')

    @property
    def verifications(self):
        return self.prescriptionverification_set.all()

    @property
    def point(self):
        point = 0
        for i in self.prescriptionverification_set.all():
            if i.is_correct:
                point += 1
            else:
                point -= 0
        return point

    @property
    def is_verified(self):

        if len(self.prescriptionverification_set.all()) >= 5:
            if self.point > 3:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return str(self.id) + ' ' + self.pharmacist.symbol_name + ' | ' + self.drug.drug.name + ' pres: ' + str(
            self.prescription.id)


class PrescriptionVerification(models.Model):
    prescription_item = models.ForeignKey(PrescriptionItem, on_delete=models.SET_NULL, null=True)
    verifier = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(default=False)
    comment = models.CharField(max_length=500, default='', null=True)

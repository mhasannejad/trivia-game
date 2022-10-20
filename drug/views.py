# Create your views here.
import json
import random
import re
from statistics import mean

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drug.serializers import *


@api_view(['GET'])
def init_drugs(request):
    f = open('dude.json', 'r')
    drugs = json.loads(f.read())
    for k, v in drugs.items():
        drug = Drug.objects.create(
            name=k
        )
        for i in v:
            DrugSubsets.objects.create(
                drug=drug,
                melh=i['melh'],
                drug_form=i['drug_form'],
                dose=i['form'],
                route_of_admin=i['route_of_admin'],
                atc_code=i['atc_code'],
                ingredient='',
                clinical='',
                access_level=i['access_level'],
                remarks=i['remarks'],
                date=i['date'],
            )
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def init_drugs_web(request):
    f = request.data
    print(f)
    print(f)
    drug = Drug.objects.create(
        name=f['name']
    )
    for i in f['subs']:
        DrugSubsets.objects.create(
            drug=drug,
            melh=i['melh'],
            drug_form=i['drug_form'],
            dose=i['form'],
            route_of_admin=i['route_of_admin'],
            atc_code=i['atc_code'],
            ingredient='',
            clinical='',
            access_level=i['access_level'],
            remarks=i['remarks'],
            date=i['date'],
        )
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def fill_the_dosage_question(request):
    drugs = Drug.objects.all()
    drugs_with_3_subset = []
    for i in drugs:
        if len(i.drugsubsets_set.all()) == 3:
            drugs_with_3_subset.append(i)
    questions = []
    for i in drugs_with_3_subset:
        options = []
        for j in i.drugsubsets_set.all():
            options.append({
                'text': j.dose,
                'is_right': False
            })

        list_of_possible_suffixes = list(map(lambda x: re.sub('[0123456789]', '', x.dose), i.drugsubsets_set.all()))
        try:
            avrage_of_dose_by_2 = str(int(mean(
                map(lambda x: float(re.sub('[abcdefghi/jklmnopqrstuv]', '', x.dose)),
                    i.drugsubsets_set.all())) * 2)) + random.choice(list_of_possible_suffixes)


        except Exception as e:
            avrage_of_dose_by_2 = '2 mg/ml'

        options.append({
            'text': avrage_of_dose_by_2,
            'is_right': True
        })
        random.shuffle(options)
        questions.append(
            {
                'text': f"which one is not a dosage for {i.name} ?",
                'subject_id': 1,
                'options': options
            }
        )

    with open('qs.json', 'w') as f:
        f.write(json.dumps(questions))
    return Response(questions)


@api_view(['GET'])
def get_drug_list(request):
    return Response(DrugSerializer(Drug.objects.all(), many=True).data)


@api_view(['GET'])
def get_subsets_for(request, drug):
    drugss_list = DrugSubsets.objects.filter(drug__name=drug)
    dosage_list = list(set(list(map(lambda x: x[0], list(drugss_list.values_list('dose'))))))
    form_list = list(set(list(map(lambda x: x[0], list(drugss_list.values_list('drug_form'))))))
    return Response(DrugSubsetSerializer(drugss_list, many=True).data)


@api_view(['POST'])
def add_drug_to_prescription(request):
    pass


@api_view(['POST'])
def upload_prescription(request):
    myfile = request.FILES.get('image')
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    Prescription.objects.create(
        image=uploaded_file_url
    )

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_random_prescription_to_label(request):
    # get some random pres which is not verified
    prescriptions = []
    for i in Prescription.objects.filter(Q(labeled=False)):
        if len(list(set(map(lambda x: x.pharmacist.id, i.prescriptionitem_set.all())))) < 5:
            prescriptions.append(i)
    random.shuffle(prescriptions)
    return Response(PrescriptionSerializer(prescriptions[0]).data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_drug_to_prescription(request):
    drugsubset = DrugSubsets.objects.get(id=request.data['drugsubset_id'])
    prescription = Prescription.objects.get(id=request.data['prescription_id'])
    PrescriptionItem.objects.create(
        drug=drugsubset,
        count=request.data['count'],
        per_time=request.data['per_time'],
        trading_name=request.data['trading_name'],
        pharmacist=request.user,
        prescription=prescription,
    )
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_prescription_with_items_for_moderation(request):
    if User.objects.get(id=request.user.id).is_valid_to_moderate is False:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    prescriptions_with_items_prescribed_by_morethan_5 = []
    for i in Prescription.objects.all():

        if len(i.pharmacists) >= 5:
            prescriptions_with_items_prescribed_by_morethan_5.append(i)
    random.shuffle(prescriptions_with_items_prescribed_by_morethan_5)
    prescription = prescriptions_with_items_prescribed_by_morethan_5[0]
    pharmacists_who_submitted = User.objects.filter(id__in=list(set(map(lambda x: x.id, User.objects.filter(
        prescriptionitem__prescription=prescription)))))
    object_to_be_send = []
    for i in pharmacists_who_submitted:
        presitems = PrescriptionItem.objects.filter(
            prescription=prescription,
            pharmacist=i
        ).filter(~Q(prescriptionverification__verifier=request.user))
        presitems = list(filter(lambda x: len(x.prescriptionverification_set.all()) <= 5, presitems))
        if len(presitems) > 0:
            object_to_be_send.append({
                'pharmacist': UserSerializerLite(i).data,
                'prescription_items': PrescriptionItemSerializer(presitems, many=True).data
            })

    return Response({'prescription': PrescriptionSerializer(prescription).data, 'items': object_to_be_send},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_verification_for_prescription(request):
    if request.user.role != 1:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    prescription_item = PrescriptionItem.objects.get(id=request.data['prescription_id'])
    PrescriptionVerification.objects.create(
        prescription_item=prescription_item,
        verifier=request.user,
        is_correct=request.data['is_correct'],
        comment=request.data['comment']
    )
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prescription_profile_for_user(request):
    correct_prescriptions = []
    wrong_prescriptions = []

    user = User.objects.get(id=request.user.id)
    for i in user.correct_prescriptions_prescribed:
        correct_prescriptions.append({
            'prescription': PrescriptionSerializer(i).data,
            'presitems': PrescriptionItemSerializerWithResults(i.prescriptionitem_set.filter(pharmacist=user),
                                                               many=True).data
        })

    for i in user.wrong_prescriptions_prescribed:
        wrong_prescriptions.append({
            'prescription': PrescriptionSerializer(i).data,
            'presitems': PrescriptionItemSerializerWithResults(i.prescriptionitem_set.filter(pharmacist=user),
                                                               many=True).data
        })

    object_to_be_sent = {
        'user': UserSerializerLite(request.user).data,
        'correct_prescriptions': correct_prescriptions,
        'wrong_prescriptions': wrong_prescriptions
    }

    return Response(object_to_be_sent, status=status.HTTP_200_OK)


@api_view(['GET'])
def ranking(request):
    users = User.objects.all()
    users = sorted(users, key=lambda x: x.total_prescription_point)
    return Response(UserSerializerWithPrescriptionStats(reversed(users), many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prescription_stats(request):
    user = User.objects.get(id=request.user.id)
    return Response({
        'total_prescriptions': len(user.prescriptions_prescribed),
        'points_earned': user.total_prescription_point,
        'correct_prescribed': user.correct_prescriptions_prescribed_len,
        'wrong_prescribed': user.wrong_prescriptions_prescribed_len,

    })

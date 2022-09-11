# Create your views here.
import json
import random
import re
from statistics import mean

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drug.models import Drug, DrugSubsets
from drug.serializers import DrugSerializer, DrugSubsetSerializer


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
                'subject_id':1,
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

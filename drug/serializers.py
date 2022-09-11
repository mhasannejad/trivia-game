from rest_framework.serializers import ModelSerializer

from drug.models import Drug, DrugSubsets


class DrugSerializer(ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'



class DrugSubsetSerializer(ModelSerializer):
    class Meta:
        model = DrugSubsets
        fields = '__all__'

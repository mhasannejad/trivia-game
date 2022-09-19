from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.serializers import UserSerializerLite
from drug.models import *


class DrugSerializer(ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'


class DrugSubsetSerializer(ModelSerializer):
    drug = DrugSerializer()

    class Meta:
        model = DrugSubsets
        fields = '__all__'
        depth = 3


class PrescriptionSerializer(ModelSerializer):
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = Prescription
        fields = ['id', 'image_url', 'labeled']


class PrescriptionItemSerializer(ModelSerializer):
    prescription = PrescriptionSerializer()
    drug = DrugSubsetSerializer()
    pharmacist = UserSerializerLite()

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'prescription', 'drug', 'pharmacist', 'count', 'per_time']


class PrescriptionItemSerializerWithResults(ModelSerializer):
    prescription = PrescriptionSerializer()
    drug = DrugSubsetSerializer()
    pharmacist = UserSerializerLite()
    point = serializers.ReadOnlyField()
    is_verified = serializers.ReadOnlyField()

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'prescription', 'drug', 'pharmacist', 'count', 'per_time', 'point', 'is_verified']


class PrescriptionWithLabelsSerializer(ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id']


class UserSerializerWithPrescriptionStats(ModelSerializer):
    symbol_name = serializers.ReadOnlyField()
    correct_prescriptions_prescribed_len = serializers.ReadOnlyField()
    wrong_prescriptions_prescribed_len = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'symbol_name', 'email', 'total_prescription_point', 'correct_prescriptions_prescribed_len',
                  'wrong_prescriptions_prescribed_len']

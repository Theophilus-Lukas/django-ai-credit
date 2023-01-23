import imp
from pyexpat import model
from rest_framework import serializers
from .models import Predictor


class PredictorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predictor
        fields = ['id', 'user_name']

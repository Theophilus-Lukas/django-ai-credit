from django.http import JsonResponse
from .models import Predictor
from .serializers import PredictorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .functions import oracle_v1


@api_view(['GET'])
def get_prediction(request):
    predictor_id = request.data['id']
    predictor = Predictor.objects.get(id=predictor_id)
    prediction = oracle_v1.predict(predictor)
    data_result = {'data': {
        'prediction': prediction
    }}
    return Response(data_result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_predictor(request):
    all_predictor = Predictor.objects.all()
    predictor_serializer = PredictorSerializer(all_predictor, many=True)
    data_result = {
        'status': status.HTTP_200_OK,
        'data': predictor_serializer.data
    }
    return JsonResponse(data_result)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def crud_predictor(request):

    if (request.method == 'POST'):
        predictor_serializer = PredictorSerializer(data=request.data)
        if (predictor_serializer.is_valid()):
            predictor_serializer.save()
            data_result = {'data': predictor_serializer.data}
            return Response(data_result, status=status.HTTP_201_CREATED)

    elif (request.method == 'GET'):
        predictor_id = request.data['id']
        data = Predictor.objects.get(id=predictor_id)
        data_serializer = PredictorSerializer(data)
        data_result = {'data': data_serializer.data}
        return Response(data_result, status=status.HTTP_200_OK)

    elif (request.method == 'PUT'):
        predictor_id = request.data['id']
        data_result = {'data': predictor_id}
        return Response(data_result, status=status.HTTP_200_OK)

    elif (request.method == 'DELETE'):
        predictor_id = request.data['id']
        data_result = {'data': predictor_id}
        return Response(data_result, status=status.HTTP_200_OK)

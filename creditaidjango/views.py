from django.http import JsonResponse
from .models import Predictor
from .serializers import PredictorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .functions import oracle_v1


@api_view(['GET'])
def ping(request):
    data_result = {'data': {'message': "Hello World"}}
    return Response(data_result, status=status.HTTP_200_OK)


@api_view(['POST'])
def test(request):
    test_result = {'data': {'message': "success"}}

    # BEGIN TESTING BLOCK
    # predictor_serializer = PredictorSerializer(data=request.data)
    # if (predictor_serializer.is_valid()):
    #     predictor_serializer.save()
    #     test_result = {'data': predictor_serializer.data}
    # END TESTING BLOCK

    return Response(test_result, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_prediction(request):
    ocr_result = oracle_v1.id_score(request.data['id'])

    prediction_result = {'data': {
        'result': ocr_result
    }}
    return Response(prediction_result, status=status.HTTP_200_OK)


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
            predictor_result = {'data': predictor_serializer.data}
            return Response(predictor_result, status=status.HTTP_201_CREATED)
    else:
        predictor_id = request.data['id']
        try:
            predictor = Predictor.objects.get(id=predictor_id)
        except Predictor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if (request.method == 'GET'):
            predictor_serializer = PredictorSerializer(predictor)
            predictor_result = {'data': predictor_serializer.data}
            return Response(predictor_result, status=status.HTTP_200_OK)

        elif (request.method == 'PUT'):
            predictor_serializer = PredictorSerializer(
                predictor, data=request.data)

            if predictor_serializer.is_valid():
                predictor_serializer.save()
                predictor_result = {'data': predictor_serializer.data}
                return Response(predictor_result, status=status.HTTP_200_OK)
            return Response(predictor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif (request.method == 'DELETE'):
            predictor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

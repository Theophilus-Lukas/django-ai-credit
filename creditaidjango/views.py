from django.http import JsonResponse
from .models import Predictor
from .serializers import PredictorSerializer
from rest_framework.decorators import api_view
from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
from .csrfexempt import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import os

from .functions import feature1, feature2

authentication_classes = (CsrfExemptSessionAuthentication)

# GENERAL FUNCTIONS


def save_image(data):
    predictor_serializer = PredictorSerializer(data=data)
    if (predictor_serializer.is_valid()):
        predictor_serializer.save()
    return predictor_serializer


def delete_image(id):
    try:
        image = Predictor.objects.get(id=id)
        os.remove(image.image.path)
        image.delete()
    except Predictor.DoesNotExist:
        return JsonResponse({'message': "PREDICTOR_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
    return True


def get_image(id):
    try:
        predictor = Predictor.objects.get(id=id)
    except Predictor.DoesNotExist:
        return JsonResponse({'message': "PREDICTOR_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
    return predictor


def build_result(data):
    result = {
        "status": status.HTTP_400_BAD_REQUEST,
        "data": data
    }
    return result


# BASIC ENDPOINTS


@api_view(['GET'])
def ping(request):
    result = build_result({'message': "Hello World"})
    return JsonResponse(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_image(request):
    all_predictor = Predictor.objects.all()
    predictor_serializer = PredictorSerializer(all_predictor, many=True)
    result = build_result({"images": predictor_serializer.data})
    return JsonResponse(result)

# @csrf_exempt


@api_view(['POST'])
def upload_image_data(request):
    predictor_serializer = save_image(request.data)
    result = build_result({'image': predictor_serializer.data})
    return JsonResponse(result, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_image_data(request):
    id = request.data["id"]
    delete_image(id)
    return JsonResponse(build_result())


@api_view(['GET'])
def get_image_data(request):
    predictor_id = request.data['id']
    try:
        predictor = Predictor.objects.get(id=predictor_id)
    except Predictor.DoesNotExist:
        return JsonResponse({'message': "PREDICTOR_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

    predictor_serializer = PredictorSerializer(predictor)
    result = build_result({'data': predictor_serializer.data})
    return JsonResponse(result, status=status.HTTP_200_OK)

# FEATURES 1


@api_view(['GET'])
def ktp_verification(request):
    ktpid = request.data['ktpid']
    selfieid = request.data['selfieid']

    try:
        ktp = Predictor.objects.get(id=ktpid)
        selfie = Predictor.objects.get(id=selfieid)
    except Predictor.DoesNotExist:
        return JsonResponse({'message': "PREDICTOR_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)

    paths = {
        "ktpppath": ktp.image,
        "selfiepath": selfie.image
    }

    ocr_result = feature1.id_score(paths['selfiepath'], paths['ktpppath'])

    result = build_result({'result': ocr_result})
    return JsonResponse(result, status=status.HTTP_200_OK)

# FEATURE 2


@api_view(['GET'])
def nib_extract(request):
    predictor_id = request.query_params['id']
    image_path = get_image(predictor_id).image
    nib_result = feature2.ocrnib(image_path)
    result = build_result({"result": nib_result})
    return JsonResponse(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def siup_extract(request):
    predictor_id = request.query_params['id']
    image_path = get_image(predictor_id).image
    siup_result = feature2.ocrnib(image_path)
    result = build_result({"result": siup_result})
    return JsonResponse(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def tdp_extract(request):
    predictor_id = request.query_params['id']
    image_path = get_image(predictor_id).image
    tdp_result = feature2.ocrnib(image_path)
    result = build_result({"result": tdp_result})
    return JsonResponse(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def skdp_extract(request):
    predictor_id = request.query_params['id']
    image_path = get_image(predictor_id).image
    skdp_result = feature2.ocrnib(image_path)
    result = build_result({"result": skdp_result})
    return JsonResponse(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def npwp_extract(request):
    predictor_id = request.query_params['id']
    image_path = get_image(predictor_id).image
    npwp_result = feature2.ocrnib(image_path)
    result = build_result({"result": npwp_result})
    return JsonResponse(result, status=status.HTTP_200_OK)


upload_image_data.authentication_classes = []
upload_image_data.permission_classes = []

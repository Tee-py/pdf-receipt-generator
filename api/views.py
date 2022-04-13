from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.decorators import api_view
from api.models import Receipt
from .serializers import GenerateReceiptSerializer, ReceiptSerializer, UserSerializer
from .constants import ErrorCodes

@api_view(['GET'])
def root(request):
    return Response({"status": True, "message": "Hello World ✅"})


class CreateUserView(APIView):

    permission_classes = []
    authentication_classes = []
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        ser = UserSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, "error_code": ErrorCodes.VALIDATION_ERROR.value, "message": "Validation Error", "data": ser.errors}, status.HTTP_400_BAD_REQUEST)
        ser.save()
        return Response({"status": True, "message": 'User Created Succesfully', "error_code": None, "data": None}, status.HTTP_201_CREATED)


@extend_schema(
    responses={
        200: inline_serializer("Fetch Receipts", {"status": serializers.BooleanField(), "error_code": None, "message": serializers.CharField(), "data": ReceiptSerializer()}), 
        401: inline_serializer("No Auth", {"detail": serializers.CharField(),})
    },
    methods=["GET"],
)
@extend_schema(
    request=GenerateReceiptSerializer,
    responses={
        201: inline_serializer("Receipt Created", {"status": {"status": serializers.BooleanField(), "error_code": None, "message": serializers.CharField(), "data": None}}),
        400: inline_serializer("Validation Error", {"status": serializers.BooleanField(default=False), "error_code": serializers.IntegerField(default=100), "message": serializers.CharField(), "data": serializers.DictField()}),
        401: inline_serializer("No Auth", {"detail": serializers.CharField(),})
    },
    methods=["POST"]
)
class ReceiptView(APIView):

    def get(self, request, **kwargs):
        recpts = Receipt.objects.filter(user=request.user)
        ser = ReceiptSerializer(recpts, many=True)
        return Response({"status": True, "error_code": None, "message": "success", "data": ser.data})
    
    def post(self, request, **kwargs):
        ser = GenerateReceiptSerializer(data=request.data, context={"request": request})
        if not ser.is_valid():
            return Response({"status": False, "error_code": ErrorCodes.VALIDATION_ERROR.value, "message": "Validation Error", "data": ser.errors}, status.HTTP_400_BAD_REQUEST)
        ser.save()
        return Response({"status": True, "error_code": None, "message": "Receipt Generated Successfully", "data": None}, status.HTTP_201_CREATED)

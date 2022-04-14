from rest_framework import serializers
from django.db import transaction
from .models import FilePDF, Receipt, User
from .utils import PDFGenerator
import json

generator = PDFGenerator('receipt.html')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "password",)
    
    def save(self):
        User.objects.create_user(**self.validated_data)

class ItemSerializer(serializers.Serializer):

    description = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)

class GenerateReceiptSerializer(serializers.Serializer):

    company_name = serializers.CharField()
    company_address = serializers.CharField()
    customer_name = serializers.CharField()
    customer_email = serializers.EmailField()
    customer_address = serializers.CharField()
    customer_mobile = serializers.CharField()
    items = ItemSerializer(many=True)

    def save(self):
        data = self.validated_data
        user = self.context['request'].user
        with transaction.atomic():
            payload = json.dumps(self.context['request'].data)
            recpt = Receipt.objects.create(user=user, payload=payload)
            total = sum([it['unit_price']*it['quantity'] for it in data['items']])
            data['total'] = total
            data['receipt_id'] = recpt.rid
            data['date'] = recpt.created_at.strftime("%d %B, %Y")
            for i in range(10):
                pdf = generator.generate_pdf(data)
                file = FilePDF.objects.create(pdf=pdf)
                recpt.files.add(file)
        return recpt
            
class ReceiptSerializer(serializers.ModelSerializer):

    file = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_file(self, obj):
        return obj.files.first().pdf.url      
    
    def get_data(self, obj):
        return json.loads(obj.payload)

    class Meta:
        model = Receipt
        fields = ("rid", "file", "data")
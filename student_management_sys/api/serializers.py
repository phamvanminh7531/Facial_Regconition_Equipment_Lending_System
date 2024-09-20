from .models import *
from rest_framework import serializers
from django.conf import settings

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['category_name']

class ItemSerializer(serializers.ModelSerializer):
    category = ItemCategorySerializer(read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'category', 'item_name', 'status', 'qr_code_img']

class ItemBorrowSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only = True)
    student = StudentSerializer(read_only = True)
    date = serializers.DateField(format=settings.DATE_FORMAT)
    borrow_time = serializers.TimeField(format=settings.TIME_FORMAT)
    return_time = serializers.TimeField(format=settings.TIME_FORMAT)
    class Meta:
        model = ItemBorrow
        fields = ['id', 'student', 'item', 'date', 'borrow_time', 'return_time', 'status']
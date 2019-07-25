from api.models import *
from api.serializers import *
from rest_framework import generics, viewsets
from django.shortcuts import render

class TableView(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class CategoriesView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


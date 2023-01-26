from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..serializers import *
from ..models import *
from rest_framework import permissions

class CustomerListAPIView(ListCreateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.all()


class CustomerDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Customer.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.all()
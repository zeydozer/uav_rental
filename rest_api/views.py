from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import UAV, Rental
from .serializers import UserSerializer, UAVSerializer, RentalSerializer
from .services.rental_service import RentalService
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import UAVFilter, RentalFilter

# 📄 Pagination for DataTable
class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'length'
    page_query_param = 'start'
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'draw': self.request.query_params.get('draw', None),
            'recordsTotal': self.page.paginator.count,
            'recordsFiltered': self.page.paginator.count,
            'data': data
        })

# 👤 User Authentication Views

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# 🚁 UAV Management Views

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering = ['username']
    # 🔒 Restrict access to authenticated users
    permission_classes = [permissions.IsAuthenticated]

class UAVListCreateView(generics.ListCreateAPIView):
    queryset = UAV.objects.all()
    serializer_class = UAVSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UAVFilter
    search_fields = ['brand', 'model', 'category', 'weight']
    ordering_fields = '__all__'
    ordering = ['brand']

class UAVRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UAV.objects.all()
    serializer_class = UAVSerializer
    permission_classes = [permissions.IsAuthenticated]

class RentalListView(generics.ListAPIView):
    queryset = Rental.objects.all().order_by('id')
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RentalFilter
    search_fields = ['uav__brand', 'uav__model', 'uav__category', 'renting_member__username', 'start_date', 'end_date']
    ordering_fields = ['uav__brand', 'renting_member__username', 'start_date', 'end_date']
    ordering = ['start_date']

# 📅 Rental Management Views

class RentalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

# 🎯 UAV Rental Action View
class RentUAVView(generics.GenericAPIView):
    queryset = UAV.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        uav = get_object_or_404(UAV, pk=kwargs['pk'])
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        rental = RentalService.rent_uav(uav, request.user, start_date, end_date)
        serializer = RentalSerializer(rental)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
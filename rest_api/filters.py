from django_filters import rest_framework as filters
from .models import UAV, Rental

class UAVFilter(filters.FilterSet):
    brand = filters.CharFilter(field_name='brand', lookup_expr='icontains')
    model = filters.CharFilter(field_name='model', lookup_expr='icontains')
    weight = filters.CharFilter(field_name='weight', lookup_expr='icontains')
    weight__gte = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')
    class Meta:
        model = UAV
        fields = ['brand', 'model', 'weight', 'weight__gte', 'category']

class RentalFilter(filters.FilterSet):
    uav__brand = filters.CharFilter(field_name='uav__brand', lookup_expr='icontains')
    renting_member__username = filters.CharFilter(field_name='renting_member__username', lookup_expr='icontains')
    start_date = filters.CharFilter(field_name='start_date', lookup_expr='icontains')
    start_date__gte = filters.DateTimeFilter(field_name='start_date', lookup_expr='gte')
    start_date__lte = filters.DateTimeFilter(field_name='start_date', lookup_expr='lte')
    end_date = filters.CharFilter(field_name='end_date', lookup_expr='icontains')
    class Meta:
        model = Rental
        fields = ['uav__brand', 'renting_member__username', 'start_date', 'start_date__gte', 'start_date__lte', 'end_date']
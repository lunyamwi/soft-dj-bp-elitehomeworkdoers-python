from django import forms
from .models import Assignments
import django_filters

class AssignmentFilter(django_filters.FilterSet):
    level = django_filters.CharFilter(lookup_expr='icontains')
    types = django_filters.CharFilter(lookup_expr='icontains')
    country= django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Assignments
        fields = ['level', 'types', 'country',]
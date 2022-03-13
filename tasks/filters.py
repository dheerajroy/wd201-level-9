from django_filters.rest_framework import FilterSet, CharFilter, ChoiceFilter, DateFilter
from tasks.models import STATUS_CHOICES

class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    status = ChoiceFilter(choices=STATUS_CHOICES)

class TaskChangeFilter(FilterSet):
    updated_at = DateFilter()
    prev_status = ChoiceFilter(choices=STATUS_CHOICES)
    curr_status = ChoiceFilter(choices=STATUS_CHOICES)

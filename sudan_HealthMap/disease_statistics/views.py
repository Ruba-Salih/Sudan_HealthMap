from django.shortcuts import render
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .statistics import calculate_disease_statistics
from case.models import Case


def disease_statistics(request):
    """
    View to render the disease statistics HTML page.
    This page will fetch data from the API dynamically.
    """
    return render(request, 'disease_statistics/main_statistics.html')


class DiseaseStatisticsAPIView(APIView):
    """
    API view to calculate and return disease statistics.
    """

    def get(self, request, *args, **kwargs):
        # Calculate statistics
        common_diseases, state_disease_stats, unique_states = calculate_disease_statistics()

        if common_diseases is None:
            return Response(
                {"detail": "No disease statistics available."},
                status=status.HTTP_204_NO_CONTENT
            )

        # Convert DataFrames to dictionaries for API response
        common_diseases_data = common_diseases.to_dict('records')
        state_disease_stats_data = state_disease_stats.to_dict('records')

        # Build API response
        response_data = {
            "common_diseases": common_diseases_data,
            "state_disease_stats": state_disease_stats_data,
            "unique_states": unique_states,
        }

        return Response(response_data, status=status.HTTP_200_OK)

class FilteredCasesAPIView(APIView):
    """
    API view to return filtered cases data.
    """

    def get(self, request, *args, **kwargs):
        disease_name = request.query_params.get('disease')
        filter_category = request.query_params.get('filter')

        if not disease_name or not filter_category:
            return Response({"error": "Disease and filter category are required."}, status=400)

        # Filter cases by disease
        cases = Case.objects.filter(disease__name=disease_name)

        # Aggregate data based on filter category
        filter_mapping = {
            "age": "patient_age",
            "sex": "patient_sex",
            "season": "season",
            "main_symptom": "main_symptom_causing_death",
            "blood_type": "patient_blood_type",
        }

        if filter_category not in filter_mapping:
            return Response({"error": "Invalid filter category."}, status=400)

        filter_field = filter_mapping[filter_category]
        aggregated_data = cases.values(filter_field).annotate(count=Count('id')).order_by(filter_field)

        # Format the response
        response_data = [{"label": item[filter_field], "count": item["count"]} for item in aggregated_data]

        return Response(response_data)
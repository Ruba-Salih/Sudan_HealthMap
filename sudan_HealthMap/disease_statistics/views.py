from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from hospital.hospital_tok import HospitalToken, HospitalTokenAuthentication
from django.core.exceptions import PermissionDenied
from .statistics import calculate_disease_statistics, calculate_hospital_statistics
from case.models import Case
from hospital.models import Hospital
from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)


def hospital_statistics_view(request):
    """
    View to render the Hospital Statistics template.
    """
    token_key = request.session.get('api_token') or request.headers.get('Authorization', '').split('Token ')[-1]

    if not token_key:
        raise PermissionDenied("No token provided. Please log in again.")
    
    try:
            # Validate the token
        hospital_token = HospitalToken.objects.get(key=token_key)
    except HospitalToken.DoesNotExist:
            raise PermissionDenied("Invalid token. Please log in again.")

    return render(request, 'hospital/statistics.html', {'api_token': token_key})

class HospitalStatisticsAPIView(APIView):
    """
    API endpoint to calculate and retrieve hospital statistics.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [HospitalTokenAuthentication]

    def get(self, request, *args, **kwargs):
        hospital = request.user  # The authenticated hospital
        # Ensure hospital is not None
        if not hospital:
            raise AuthenticationFailed("Authentication failed.")
        if not isinstance(hospital, Hospital):
                return Response({"error": "Access denied. Only hospitals can view this endpoint."}, status=403)

        # Calculate statistics
        common, recovered, deaths, daily_stats = calculate_hospital_statistics(hospital)

        response_data = {
            'common_disease': common.to_dict(orient='records') if common is not None else [],
            'recovered_disease': recovered.to_dict(orient='records') if recovered is not None else [],
            'death_disease': deaths.to_dict(orient='records') if deaths is not None else [],
            'daily_stats': daily_stats.to_dict(orient='records') if daily_stats is not None else [],
        }

        logger.debug("Response data: %s", response_data)

        try:
            return Response(response_data)
        except ValueError as e:
            print("Serialization error:", str(e))
            return JsonResponse(
                {"error": "Serialization error. Check for invalid values in data."},
                status=500,
            )

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
        # Fetch common diseases, state statistics, and unique states
        common_diseases, state_disease_stats, unique_states, seasonal_stats = calculate_disease_statistics()

        if common_diseases is None:
            return Response(
                {"detail": "No disease statistics available."},
                status=status.HTTP_204_NO_CONTENT
            )

        # Convert DataFrames to dictionaries for API response
        common_diseases_data = common_diseases.to_dict('records')
        state_disease_stats_data = state_disease_stats.to_dict('records')

        # Format seasonal statistics
        seasonal_data = {}
        for _, row in seasonal_stats.iterrows():
            season = row['season']
            if season not in seasonal_data:
                seasonal_data[season] = []
            seasonal_data[season].append({
                "disease": row['disease__name'],
                "total_cases": row['total_cases']
            })

        # Build API response
        response_data = {
            "common_diseases": common_diseases_data,
            "state_disease_stats": state_disease_stats_data,
            "unique_states": unique_states,
            "seasonal_stats": seasonal_data,
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

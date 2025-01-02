import csv
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from hospital.models import Hospital
from state.models import State
from case.models import Case
from django.db.models import Count

def generate_report(hospital_id, report_type, response_format):
    """
    Generate a reports for hospitals.
    """
    hospital = get_object_or_404(Hospital, id=hospital_id)

    if report_type == "simple":
        data = (
            Case.objects.filter(hospital=hospital)
            .values('disease__name')
            .annotate(cases=Count('id'))
            .order_by('-cases')
        )

        for entry in data:
            entry['disease__name'] = entry.get('disease__name') or "Unknown Disease"

        if response_format == "json":
            return JsonResponse(list(data), safe=False)
        elif response_format == "csv":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="simple_report_hospital_{hospital.name}.csv"'

            writer = csv.writer(response)
            writer.writerow(['Disease', 'Cases'])
            for entry in data:
                writer.writerow([entry['disease__name'], entry['cases']])

            return response

    elif report_type == "detailed":
        data = Case.objects.filter(hospital=hospital).values(
            'patient_number', 'patient_age', 'patient_sex', 'patient_blood_type','disease__name',
            'patient_status', 'main_symptom_causing_death', 'season', 'date_reported'
        )
        if response_format == "json":
            return JsonResponse(list(data), safe=False)
        elif response_format == "csv":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="detailed_report_hospital_{hospital.name}.csv"'

            writer = csv.writer(response)
            writer.writerow(['Case Number', 'Age', 'Sex', 'Blood Type', 'Disease', 'Status', 'Main Symptom', 'Season', 'Date Reported'])
            for entry in data:
                writer.writerow([
                    entry['patient_number'], entry['patient_age'], entry['patient_sex'], entry['patient_blood_type'],
                    entry['disease__name'], entry['patient_status'], entry['main_symptom_causing_death'],
                    entry['season'], entry['date_reported']
                ])

            return response

    else:
        return JsonResponse({'error': 'Invalid report type'}, status=400)

def generate_state_report(state_id, response_format="json"):
    """
    Generate a report for a state, showing hospitals, diseases, and case counts.
    """
    state = get_object_or_404(State, id=state_id)
    queryset = Case.objects.filter(hospital__state=state)

    data = (
        queryset.values('hospital__name', 'disease__name')
        .annotate(cases=Count('id'))
        .order_by('hospital__name', '-cases')
    )
    for entry in data:
        entry['disease__name'] = entry.get('disease__name')

    if response_format == "json":
        return JsonResponse(list(data), safe=False)
    elif response_format == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="state_{state.name}_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Hospital', 'Disease', 'Cases'])
        for entry in data:
            writer.writerow([entry['hospital__name'], entry['disease__name'], entry['cases']])
        return response
    else:
        return JsonResponse({'error': 'Invalid response format'}, status=400)

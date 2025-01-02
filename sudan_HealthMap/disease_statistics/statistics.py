from django.db.models import Count, Q
import pandas as pd
from case.models import Case
from supervisor.serializers import StateSerializer
from state.models import State  # Replace with the correct path to your State model


def calculate_disease_statistics():
    # Query and group data by disease and hospital (join Hospital for state data)
    queryset = (
        Case.objects.select_related('disease', 'hospital')
        .values('disease__name', 'hospital__state__name', 'hospital__name')  # Use hospital__state__name
        .annotate(
            total_cases=Count('id'),  # Total number of cases for this disease
            total_deaths=Count('id', filter=Q(patient_status='deceased'))  # Total deaths for this disease
        )
    )

    # Convert queryset to Pandas DataFrame for processing
    df = pd.DataFrame(list(queryset))

    if df.empty:
        return None, None, None

    # Aggregating statistics
    # 1. Most common diseases
    common_diseases = (
        df.groupby('disease__name')['total_cases']
        .sum()
        .reset_index()
        .sort_values(by='total_cases', ascending=False)
    )

    # 2. State-level disease prevalence
    state_disease_stats = (
        df.groupby(['hospital__state__name', 'disease__name'])
        .agg(
            total_cases=('total_cases', 'sum'),
            total_deaths=('total_deaths', 'sum')
        )
        .reset_index()
    )

    # Fetch unique states using the StateSerializer
    states = State.objects.all()
    serializer = StateSerializer(states, many=True)
    unique_states = serializer.data  # Serialized state data

    return common_diseases, state_disease_stats, unique_states

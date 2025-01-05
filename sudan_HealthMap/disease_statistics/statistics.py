from django.db.models import Count, Q
import pandas as pd
from case.models import Case
from supervisor.serializers import StateSerializer
from state.models import State


def calculate_disease_statistics():
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

def calculate_hospital_statistics(hospital):
    """
    Calculate statistics for the currently logged-in hospital.
    - Most common disease related to the hospital.
    - Disease with the most recoveries.
    - Disease with the most deaths.
    - Rate of increase or decrease in cases over days.
    """
    # Filter cases for the given hospital
    queryset = (
        Case.objects.filter(hospital=hospital)
        .select_related('disease')
        .values('disease__name')
        .annotate(
            total_cases=Count('id'),  # Total number of cases for the disease
            total_recovered=Count('id', filter=Q(patient_status='recovered')),  # Recoveries for the disease
            total_deaths=Count('id', filter=Q(patient_status='deceased'))  # Deaths for the disease
        )
    )

    # Convert queryset to Pandas DataFrame for processing
    df = pd.DataFrame(list(queryset))

    if df.empty:
        return None, None, None, None

    # 1. Most common disease
    most_common_disease = df.sort_values(by='total_cases', ascending=False)

    # 2. Disease with the most recoveries
    most_recovered_disease = df.sort_values(by='total_recovered', ascending=False)

    # 3. Disease with the most deaths
    most_death_disease = df.sort_values(by='total_deaths', ascending=False)

    # 4. Rate of increase or decrease in cases over days
    daily_cases = (
        Case.objects.filter(hospital=hospital)
        .values('disease__name', 'date_reported')  # Use the correct field name
        .annotate(daily_total=Count('id'))
    )

    # Convert daily data to Pandas DataFrame
    daily_df = pd.DataFrame(list(daily_cases))

    if not daily_df.empty:
        daily_df['date_reported'] = pd.to_datetime(daily_df['date_reported'])
        daily_df = daily_df.sort_values(by=['disease__name', 'date_reported'])

        daily_df['daily_change'] = (
            daily_df.groupby('disease__name')['daily_total'].diff()
        )
    
        daily_df['rate_of_change'] = (
            daily_df.groupby('disease__name')['daily_change'].transform(lambda x: x.diff() / x.shift(1) * 100)
        )
    else:
        daily_df = None

    most_common_disease = clean_dataframe(most_common_disease)
    most_recovered_disease = clean_dataframe(most_recovered_disease)
    most_death_disease = clean_dataframe(most_death_disease)
    daily_df = clean_dataframe(daily_df)

    return most_common_disease, most_recovered_disease, most_death_disease, daily_df

def clean_dataframe(df):
    if df is not None:
        df = df.fillna(0)  # Replace NaN with 0
        df = df.replace([float('inf'), float('-inf')], 0)  # Replace Infinity with 0
        if 'date_reported' in df.columns:
            df['date_reported'] = df['date_reported'].astype(str)  # Convert Timestamps to strings
    return df
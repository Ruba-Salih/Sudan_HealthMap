from django.db.models import Count, Q
import pandas as pd
from case.models import Case
from state.serializers import StateSerializer
from state.models import State


def calculate_disease_statistics():
    queryset = (
        Case.objects.select_related('disease', 'hospital')
        .values('disease__name', 'hospital__state__name', 'hospital__name', 'season')
        .annotate(
            total_cases=Count('id'),
            total_deaths=Count('id', filter=Q(patient_status='deceased'))
        )
    )

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return None, None, None, None

    ''' Most common diseases'''
    common_diseases = (
        df.groupby('disease__name')['total_cases']
        .sum()
        .reset_index()
        .sort_values(by='total_cases', ascending=False)
    )

    ''' State-level disease prevalence '''
    state_disease_stats = (
        df.groupby(['hospital__state__name', 'disease__name'])
        .agg(
            total_cases=('total_cases', 'sum'),
            total_deaths=('total_deaths', 'sum')
        )
        .reset_index()
    )

    ''' Seasonal disease distribution '''
    seasonal_disease_stats = (
        df.groupby(['season', 'disease__name'])
        .agg(
            total_cases=('total_cases', 'sum')
        )
        .reset_index()
        .sort_values(by=['season', 'total_cases'], ascending=[True, False])
    )

    states = State.objects.all()
    serializer = StateSerializer(states, many=True)
    unique_states = serializer.data

    return common_diseases, state_disease_stats, unique_states, seasonal_disease_stats

def calculate_hospital_statistics(hospital):
    """
    Calculate statistics for the currently logged-in hospital.
    - Most common disease related to the hospital.
    - Disease with the most recoveries.
    - Disease with the most deaths.
    - Rate of increase or decrease in cases over days.
    """
    queryset = (
        Case.objects.filter(hospital=hospital)
        .select_related('disease')
        .values('disease__name')
        .annotate(
            total_cases=Count('id'),
            total_recovered=Count('id', filter=Q(patient_status='recovered')),
            total_deaths=Count('id', filter=Q(patient_status='deceased'))
        )
    )

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return None, None, None, None

    ''' Most common disease '''
    most_common_disease = df.sort_values(by='total_cases', ascending=False)

    ''' Disease with the most recoveries '''
    most_recovered_disease = df.sort_values(by='total_recovered', ascending=False)

    ''' Disease with the most deaths '''
    most_death_disease = df.sort_values(by='total_deaths', ascending=False)

    ''' Rate of increase or decrease in cases in days '''
    daily_cases = (
        Case.objects.filter(hospital=hospital)
        .values('disease__name', 'date_reported')
        .annotate(total_cases=Count('id'))
    )

    daily_df = pd.DataFrame(list(daily_cases))

    if not daily_df.empty:
        # Format date and sort
        daily_df['date_reported'] = pd.to_datetime(daily_df['date_reported']).dt.strftime('%Y-%m-%d')
        daily_df = daily_df.sort_values(by=['disease__name', 'date_reported'])

        # Fill missing dates for consistency in the frontend
        all_dates = pd.date_range(start=daily_df['date_reported'].min(), end=daily_df['date_reported'].max())
        disease_groups = daily_df.groupby('disease__name')

        filled_dfs = []
        for disease, group in disease_groups:
            group = group.set_index('date_reported')
            group = group.reindex(all_dates.strftime('%Y-%m-%d'), fill_value=0)
            group['disease__name'] = disease
            filled_dfs.append(group.reset_index().rename(columns={'index': 'date_reported'}))

        daily_df = pd.concat(filled_dfs, ignore_index=True)

    else:
        daily_df = pd.DataFrame(columns=['disease__name', 'date_reported', 'total_cases'])

    return most_common_disease, most_recovered_disease, most_death_disease, daily_df

import pandas as pd
from django.db.models import Sum, Count
import matplotlib.pyplot as plt
from .models import DiseaseStatistics

def calculate_disease_statistics():
    # Query DiseaseStatistics and related fields
    queryset = DiseaseStatistics.objects.select_related('disease', 'hospital').values(
        'disease__name', 'hospital__state', 'cases', 'deaths'
    )

    # Convert to a Pandas DataFrame
    df = pd.DataFrame(list(queryset))

    # Aggregating statistics
    # 1. Most common diseases
    common_diseases = df.groupby('disease__name')['cases'].sum().reset_index().sort_values(by='cases', ascending=False)

    # 2. State-level disease prevalence
    state_disease_stats = df.groupby(['hospital__state', 'disease__name']).agg(
        total_cases=('cases', 'sum'),
        total_deaths=('deaths', 'sum')
    ).reset_index()

    # 3. Spread Rate (mock total population for each state)
    state_population = {
        'State A': 500000,
        'State B': 300000,
        'State C': 400000,
    }
    df['spread_rate'] = df.apply(
        lambda row: (row['cases'] / state_population.get(row['hospital__state'], 1)) * 100,
        axis=1
    )

    # Display the statistics
    print("Most Common Diseases")
    print(common_diseases)

    print("\nState-Level Disease Statistics")
    print(state_disease_stats)

    print("\nSpread Rate by Disease and State")
    print(df[['hospital__state', 'disease__name', 'spread_rate']])

    # Visualization
    plt.figure(figsize=(10, 6))
    plt.bar(common_diseases['disease__name'], common_diseases['cases'], color='skyblue')
    plt.title('Most Common Diseases')
    plt.xlabel('Disease')
    plt.ylabel('Number of Cases')
    plt.xticks(rotation=45)
    plt.show()

    return common_diseases, state_disease_stats, df


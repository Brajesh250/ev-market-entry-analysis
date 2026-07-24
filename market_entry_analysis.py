"""
EV Market Entry Strategy — Tier-2 City Analysis
Data-driven market prioritisation for Indian EV expansion
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

np.random.seed(21)

# ── 1. Tier-2 City Dataset ────────────────────────────────────────────────────
cities = {
    'City': [
        'Jaipur', 'Lucknow', 'Indore', 'Nagpur', 'Bhopal',
        'Visakhapatnam', 'Patna', 'Vadodara', 'Coimbatore', 'Kochi',
        'Chandigarh', 'Surat', 'Agra', 'Nashik', 'Rajkot',
        'Madurai', 'Varanasi', 'Amritsar', 'Faridabad', 'Meerut'
    ],
    'State': [
        'Rajasthan', 'UP', 'MP', 'Maharashtra', 'MP',
        'AP', 'Bihar', 'Gujarat', 'Tamil Nadu', 'Kerala',
        'Punjab', 'Gujarat', 'UP', 'Maharashtra', 'Gujarat',
        'Tamil Nadu', 'UP', 'Punjab', 'Haryana', 'UP'
    ],
    'Population_M': [
        3.46, 3.72, 2.17, 2.92, 1.88,
        2.04, 2.35, 2.18, 1.06, 0.68,
        1.06, 6.06, 1.75, 1.49, 1.39,
        1.48, 1.43, 1.18, 1.73, 1.31
    ],
    'Per_Capita_Income_K': [
        142, 138, 156, 148, 135,
        165, 110, 172, 180, 210,
        195, 168, 120, 145, 158,
        130, 112, 175, 185, 128
    ],
    'EV_Penetration_Pct': [
        3.2, 2.8, 4.1, 3.8, 2.9,
        4.5, 1.8, 5.2, 6.8, 7.2,
        6.1, 5.8, 2.1, 3.5, 4.8,
        3.0, 1.9, 4.2, 5.5, 2.3
    ],
    'Charging_Infra_Score': [  # 1–10, 10 = best
        6.2, 5.8, 7.1, 6.8, 5.5,
        7.5, 4.2, 8.1, 8.5, 9.0,
        8.2, 7.8, 4.8, 6.1, 7.2,
        5.5, 4.5, 6.8, 7.5, 4.9
    ],
    'Govt_EV_Policy_Score': [  # 1–10
        8.5, 7.0, 8.8, 7.5, 8.2,
        7.8, 6.5, 9.0, 8.5, 8.8,
        8.0, 8.5, 6.8, 7.2, 8.0,
        7.5, 6.2, 7.8, 8.2, 6.8
    ],
    'Avg_Commute_KM': [
        18, 22, 16, 20, 15,
        19, 25, 14, 12, 11,
        13, 17, 23, 18, 15,
        14, 20, 16, 21, 19
    ],
    'Two_Wheeler_Share_Pct': [
        68, 72, 65, 60, 70,
        62, 78, 58, 55, 48,
        52, 60, 75, 65, 62,
        58, 76, 60, 65, 72
    ],
    'Air_Quality_Index': [  # higher = worse
        185, 210, 145, 130, 155,
        90, 240, 105, 85, 70,
        95, 120, 255, 135, 110,
        80, 265, 140, 220, 230
    ],
}

df = pd.DataFrame(cities)

# ── 2. Market Opportunity Score (composite) ───────────────────────────────────
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

df['score_income']    = normalize(df['Per_Capita_Income_K'])
df['score_infra']     = normalize(df['Charging_Infra_Score'])
df['score_policy']    = normalize(df['Govt_EV_Policy_Score'])
df['score_aqi']       = normalize(df['Air_Quality_Index'])       # high AQI → high urgency
df['score_pop']       = normalize(df['Population_M'])
df['score_2w']        = normalize(df['Two_Wheeler_Share_Pct'])   # 2W dominance = larger EV TAM

# Weighted composite score
weights = {
    'score_income': 0.20,
    'score_infra':  0.25,
    'score_policy': 0.20,
    'score_aqi':    0.15,
    'score_pop':    0.10,
    'score_2w':     0.10,
}
df['Market_Score'] = sum(df[col] * w for col, w in weights.items())
df['Market_Score'] = (df['Market_Score'] * 100).round(1)

# Priority tier
df['Priority'] = pd.cut(df['Market_Score'],
                         bins=[0, 45, 60, 75, 100],
                         labels=['Watch', 'Moderate', 'High', 'Immediate'])

df = df.sort_values('Market_Score', ascending=False).reset_index(drop=True)
df['Rank'] = range(1, len(df)+1)

# ── 3. Console Report ─────────────────────────────────────────────────────────
print("=" * 75)
print("   EV MARKET ENTRY STRATEGY — TIER-2 INDIA ANALYSIS")
print("=" * 75)

print("\n🏆 TOP 10 CITIES BY MARKET OPPORTUNITY SCORE")
print("-" * 75)
top10 = df.head(10)[['Rank','City','State','Market_Score','Priority',
                       'EV_Penetration_Pct','Charging_Infra_Score','Govt_EV_Policy_Score']]
print(top10.to_string(index=False))

print("\n📊 SEGMENT BREAKDOWN")
print(df['Priority'].value_counts().to_string())

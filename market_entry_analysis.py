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

print("\n🔑 KEY METRICS — TOP 5 vs BOTTOM 5")
print("Top 5 avg income:  ₹{:.0f}K | Bottom 5: ₹{:.0f}K".format(
    df.head(5)['Per_Capita_Income_K'].mean(), df.tail(5)['Per_Capita_Income_K'].mean()))
print("Top 5 avg infra score: {:.1f} | Bottom 5: {:.1f}".format(
    df.head(5)['Charging_Infra_Score'].mean(), df.tail(5)['Charging_Infra_Score'].mean()))
print("Top 5 avg EV penetration: {:.1f}% | Bottom 5: {:.1f}%".format(
    df.head(5)['EV_Penetration_Pct'].mean(), df.tail(5)['EV_Penetration_Pct'].mean()))

# ── 4. Strategy Dashboard ─────────────────────────────────────────────────────
COLORS_PRIORITY = {
    'Immediate': '#3fb950',
    'High':      '#58a6ff',
    'Moderate':  '#ffa657',
    'Watch':     '#6e7681',
}
BG, TEXT = '#0d1117', '#e6edf3'
PANEL_BG = '#161b22'

fig = plt.figure(figsize=(20, 14), facecolor=BG)
fig.suptitle('EV Market Entry Strategy — Tier-2 India', fontsize=24,
             fontweight='bold', color=TEXT, y=0.98)

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.38)

def ax_style(ax, title):
    ax.set_facecolor(PANEL_BG)
    ax.set_title(title, color=TEXT, fontsize=12, fontweight='bold', pad=10)
    ax.tick_params(colors=TEXT, labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')
    return ax

# Chart 1: Top 10 cities — Market Score bar
ax1 = ax_style(fig.add_subplot(gs[0, :2]), '🏆 Top 10 Cities — Market Opportunity Score')
top10_plot = df.head(10)
bar_colors = [COLORS_PRIORITY[p] for p in top10_plot['Priority']]
bars = ax1.barh(top10_plot['City'][::-1], top10_plot['Market_Score'][::-1],
                color=bar_colors[::-1], edgecolor='none', height=0.7)
for bar, score in zip(bars, top10_plot['Market_Score'][::-1]):
    ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
             f'{score}', va='center', color=TEXT, fontweight='bold', fontsize=9)
ax1.set_xlabel('Market Opportunity Score (0–100)', color=TEXT, fontsize=9)
ax1.set_xlim(0, 100)
patches = [mpatches.Patch(color=v, label=k) for k,v in COLORS_PRIORITY.items()]
ax1.legend(handles=patches, fontsize=8, facecolor=PANEL_BG,
           labelcolor=TEXT, loc='lower right', framealpha=0.7)
ax1.grid(axis='x', color='#30363d', linestyle='--', alpha=0.4)

# Chart 2: Priority tier distribution — donut
ax2 = ax_style(fig.add_subplot(gs[0, 2]), '🎯 Priority Tier Distribution')
tier_counts = df['Priority'].value_counts()
wedge_colors = [COLORS_PRIORITY[t] for t in tier_counts.index]
wedges, texts, autotexts = ax2.pie(tier_counts, labels=tier_counts.index,
                                    autopct='%1.0f%%', colors=wedge_colors,
                                    startangle=140, wedgeprops={'width':0.6})
for t in texts + autotexts:
    t.set_color(TEXT); t.set_fontsize(9)

# Chart 3: Infra Score vs EV Penetration scatter
ax3 = ax_style(fig.add_subplot(gs[1, 0]), '📡 Infra Score vs EV Penetration')
for priority, color in COLORS_PRIORITY.items():
    subset = df[df['Priority'] == priority]
    ax3.scatter(subset['Charging_Infra_Score'], subset['EV_Penetration_Pct'],
                color=color, s=subset['Market_Score']*4, alpha=0.85,
                label=priority, edgecolors='none')
    for _, row in subset.iterrows():
        if row['Rank'] <= 8:
            ax3.annotate(row['City'], (row['Charging_Infra_Score'], row['EV_Penetration_Pct']),
                         fontsize=6.5, color=TEXT, textcoords='offset points', xytext=(4, 3))
ax3.set_xlabel('Charging Infrastructure Score', color=TEXT, fontsize=9)
ax3.set_ylabel('Current EV Penetration (%)', color=TEXT, fontsize=9)
ax3.legend(fontsize=7, facecolor=PANEL_BG, labelcolor=TEXT, framealpha=0.7)
ax3.grid(color='#30363d', linestyle='--', alpha=0.4)

# Chart 4: Income vs Market Score
ax4 = ax_style(fig.add_subplot(gs[1, 1]), '💰 Income vs Market Score')
for priority, color in COLORS_PRIORITY.items():
    subset = df[df['Priority'] == priority]
    ax4.scatter(subset['Per_Capita_Income_K'], subset['Market_Score'],
                color=color, s=70, alpha=0.85, label=priority, edgecolors='none')
    for _, row in subset.iterrows():
        if row['Rank'] <= 8:
            ax4.annotate(row['City'], (row['Per_Capita_Income_K'], row['Market_Score']),
                         fontsize=6.5, color=TEXT, textcoords='offset points', xytext=(4, 2))
ax4.set_xlabel('Per Capita Income (₹K)', color=TEXT, fontsize=9)
ax4.set_ylabel('Market Opportunity Score', color=TEXT, fontsize=9)
ax4.legend(fontsize=7, facecolor=PANEL_BG, labelcolor=TEXT, framealpha=0.7)
ax4.grid(color='#30363d', linestyle='--', alpha=0.4)

# Chart 5: AQI vs 2W share (urgency quadrant)
ax5 = ax_style(fig.add_subplot(gs[1, 2]), '🌍 AQI vs 2-Wheeler Share (Urgency)')
for priority, color in COLORS_PRIORITY.items():
    subset = df[df['Priority'] == priority]
    ax5.scatter(subset['Two_Wheeler_Share_Pct'], subset['Air_Quality_Index'],
                color=color, s=70, alpha=0.85, label=priority, edgecolors='none')
    for _, row in subset.iterrows():
        if row['Rank'] <= 6:
            ax5.annotate(row['City'], (row['Two_Wheeler_Share_Pct'], row['Air_Quality_Index']),
                         fontsize=6.5, color=TEXT, textcoords='offset points', xytext=(3, 3))
ax5.set_xlabel('2-Wheeler Market Share (%)', color=TEXT, fontsize=9)
ax5.set_ylabel('Air Quality Index (Higher = Worse)', color=TEXT, fontsize=9)
ax5.axhline(y=150, color='#f78166', linestyle='--', alpha=0.5, linewidth=1.5,
            label='WHO Threshold')
ax5.legend(fontsize=7, facecolor=PANEL_BG, labelcolor=TEXT, framealpha=0.7)
ax5.grid(color='#30363d', linestyle='--', alpha=0.4)

plt.savefig('market_entry_analysis.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("\n✅ Dashboard saved → market_entry_analysis.png")
plt.close()

# Save ranked data
df.to_csv('city_market_scores.csv', index=False)
print("✅ Data saved  → city_market_scores.csv")

print("\n🎯 RECOMMENDED ENTRY SEQUENCE:")
immediate = df[df['Priority'] == 'Immediate']['City'].tolist()
high      = df[df['Priority'] == 'High']['City'].tolist()
print(f"   Phase 1 (0–6 months)  — Immediate: {', '.join(immediate)}")
print(f"   Phase 2 (6–12 months) — High:      {', '.join(high)}")

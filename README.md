# ⦱ EV Market Entry Strategy — Tier-2 India Analysis

Data-driven market prioritisation model for EV companies planning to expand into Indian Tier-2 cities. Scores 20 cities across 6 weighted factors and produces a strategic entry roadmap with visualisations.

## 🎯 Business Problem
> *Which Tier-2 cities should an EV company enter first, and why?*

## 🐰 Scoring Model (Composite Index)
| Factor | Weight | Rationale |
|-------|--------|----------|
| Charging Infrastructure | 25% | Enabler of EV adoption |
| Government EV Policy | 20% | Subsidy & regulatory support |
| Per Capita Income | 20% | Purchase affordability |
| Air Quality Index | 15% | Environmental urgency → demand |
| Population | 10% | Market size |
| 2-Wheeler Share | 10% | Primary EV replacement segment |

## 🏢 Key Findings (Top 5 Priority Cities)
| Rank | City | Score | Priority |
|------|-----|-------|-----------|
| 1 | Kochi | ~82 | Immediate |
| 2 | Coimbatore | ~78 | Immediate |
| 3 | Chandigarh | ~76 | High |
| 4 | Surat | ~74 | High |
| 5 | Vadodara | ~72 | High |

## 🛠️ Tech Stack
- **Python 3.10+** — analysis & scoring
- **pandas** — data manipulation
- **NumPy** — normalisation
- **Matplotlib** —  5-panel strategy dashboard

## 𚀀 Quick Start
```bash
pip install -r requirements.txt
python market_entry_analysis.py
```

**Outputs:**
- `market_entry_analysis.png` — strategy dashboard (5 charts)
- `city_market_scores.csv` — full scored dataset

## 📊 Dashboard Preview
![EV Market Entry Strategy Dashboard](market_entry_analysis.png)

## 🗡 Strategic Roadmap
- **Phase 1 (0–6 months):** Enter Immediate-priority cities with high infra + policy support
- **Phase 2 (6�12 months):** Expand to High-priority cities as brand builds
- **Phase 3 (12–24 months):** Enter Moderate cities with lessons learned

## 👤 Author
**Brajesh Kumar** · [GitHub](https://github.com/Brajesh250)

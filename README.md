# 🌾 Seasonal Agriculture Performance Analysis

**VOIS AICTE Batch1 2026–2027 | Major Project**

| Field | Details |
|-------|---------|
| **Student** | Arghya Khamaru |
| **Program** | VOIS AICTE Batch1 2026–2027 |
| **AICTE STU ID** | STU6a53a0adb2ea31783865517 |
| **Course Completed** | Data Visualization — ID: VFLMS26_162540 |

---

## 📌 Problem Statement

Agricultural activities are influenced by seasonal variations in environmental conditions, farming practices, resource availability, and market conditions. Raw data does not clearly reveal how performance differs across seasons.

This project analyzes a real-world agricultural dataset to **identify seasonal patterns, trends, and relationships** across Kharif, Rabi, and Zaid seasons.

---

## 🗂️ Repository Structure

```
seasonal-agriculture-analysis/
│
├── seasonal_agriculture_analysis.ipynb          ← Main Jupyter Notebook
├── seasonal_agriculture_performance_dataset.csv ← Dataset (4,000 records)
├── README.md                                    ← This file
│
└── output_charts/                               ← Saved visualisation images
    ├── yield_by_season.png
    ├── profit_distribution.png
    ├── rainfall_vs_yield.png
    ├── irrigation_heatmap.png
    └── economic_outcomes.png
```

---

## 📊 Dataset Overview

| Attribute | Value |
|-----------|-------|
| Records | 4,000 farm entries |
| Seasons | Kharif, Rabi, Zaid |
| States | 8 Indian states |
| Crops | Wheat, Maize, Rice, Pulses, Cotton, Chilli, Groundnut, Sugarcane |
| Features | 28 columns |

**Feature categories:**
- **Environmental:** Rainfall, Temperature, Humidity, Sunlight, Soil pH, Soil Moisture
- **Resources:** Irrigation Method, Fertilizer, Pesticide, Water Used
- **Economic:** Yield, Production, Market Price, Revenue, Profit

---

## 🔍 Key Findings

### Yield Analysis
| Season | Avg Yield (t/ha) | Avg Rainfall (mm) |
|--------|-----------------|-------------------|
| Kharif | **5.64** | 852.1 |
| Rabi   | 5.08 | 436.0 |
| Zaid   | 4.67 | 299.4 |

> Sugarcane is the highest-yielding crop across all seasons.

### Profitability
| Season | Profitable Farms | Avg Profit (₹) |
|--------|-----------------|----------------|
| Kharif | **57.8%** | +1,78,915 |
| Rabi   | 48.9% | +87,689 |
| Zaid   | 35.5% | **-24,805** |

### Environmental Risk
- Kharif has the **highest disease/pest risk at 54.5%** due to high humidity
- Rabi: 40.5% | Zaid: 38.2%

### Water Efficiency (t per 1000 m³)
- Kharif: 5.89 > Rabi: 5.19 > Zaid: 4.41
- **Drip irrigation** delivers 18–22% better efficiency than Flood irrigation

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3.x | Programming language |
| Pandas | Data cleaning & aggregation |
| NumPy | Numerical computation |
| Matplotlib | Charts and plots |
| Seaborn | Statistical visualisations |
| Jupyter Notebook | Interactive analysis & documentation |
| GitHub | Version control & project sharing |

---

## 🚀 How to Run

### Option 1: Google Colab (No installation needed)
1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Click **File → Upload notebook**
3. Upload `seasonal_agriculture_analysis.ipynb`
4. Upload `seasonal_agriculture_performance_dataset.csv` to the Colab files panel
5. Click **Runtime → Run all**

### Option 2: Local Setup
```bash
# Clone the repository
git clone https://github.com/[your-username]/seasonal-agriculture-analysis.git
cd seasonal-agriculture-analysis

# Install required libraries
pip install pandas numpy matplotlib seaborn jupyter

# Launch Jupyter Notebook
jupyter notebook seasonal_agriculture_analysis.ipynb
```

---

## 📈 Recommendations

1. **Promote drip irrigation in Zaid** — reduces water waste and improves efficiency
2. **Prioritise Cotton & Chilli in Rabi** — higher market prices improve profitability
3. **Strengthen pest-control in Kharif** — 54.5% disease risk needs targeted intervention
4. **Support Zaid farmers** — policy-level subsidies needed as 64.5% run at a loss

---

## 🔭 Future Scope

- Machine Learning models for yield prediction
- Real-time weather data integration
- Extension to all 28 Indian states
- Crop recommendation mobile/web application
- Climate change impact modelling

---

## 📜 Certificate

Arghya Khamaru has completed the **Data Visualization** course under VOIS × Edunet Foundation  
**Certificate ID:** VFLMS26_162540 | **Issued:** September 8, 2026

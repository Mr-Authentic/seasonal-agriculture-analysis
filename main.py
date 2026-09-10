#================================================================
# MAJOR PROJECT
# Seasonal Agriculture Performance Analysis
#================================================================

import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import pearsonr, f_oneway

warnings.filterwarnings("ignore")


# CONFIGURATION

# Change this path if your CSV file is stored somewhere else
FILE_PATH = "seasonal_agriculture_performance_dataset.csv"

OUTPUT_DIR = "outputs"
PLOT_DIR = os.path.join(OUTPUT_DIR, "plots")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

print("=" * 70)
print("SEASONAL AGRICULTURE PERFORMANCE ANALYSIS")
print("=" * 70)


# LOAD DATASET

print("\n[1] Loading dataset...")

try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print("\nERROR: Dataset file not found.")
    print("Please check FILE_PATH.")
    raise

print("\nDataset loaded successfully.")

print("\nNumber of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\nFirst 5 records:")
print(df.head())


# BASIC DATASET INFORMATION

print("\n" + "=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nDataset information:")
df.info()

print("\nStatistical description:")
print(df.describe(include="all").T)


# Save descriptive statistics
df.describe(include="all").T.to_csv(
    os.path.join(OUTPUT_DIR, "descriptive_statistics.csv")
)


# CHECK DUPLICATES

print("\n" + "=" * 70)
print("DUPLICATE ANALYSIS")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print("Number of duplicate rows:", duplicate_count)

if duplicate_count > 0:
    df = df.drop_duplicates()
    print("Duplicate rows removed.")

else:
    print("No duplicate rows found.")


# MISSING VALUE ANALYSIS

print("\n" + "=" * 70)
print("MISSING VALUE ANALYSIS")
print("=" * 70)

missing_values = df.isnull().sum()

missing_percentage = (
    df.isnull().sum() / len(df) * 100
).round(2)

missing_table = pd.DataFrame({
    "Missing_Count": missing_values,
    "Missing_Percentage": missing_percentage
})

print(missing_table)

missing_table.to_csv(
    os.path.join(OUTPUT_DIR, "missing_values.csv")
)


# DATA CLEANING

print("\n" + "=" * 70)
print("DATA CLEANING")
print("=" * 70)

# Identify numerical columns
numeric_columns = df.select_dtypes(
    include=np.number
).columns

# Fill numerical missing values using median
for column in numeric_columns:

    if df[column].isnull().sum() > 0:
        median_value = df[column].median()

        df[column] = df[column].fillna(median_value)

        print(
            f"Filled missing values in {column} "
            f"using median = {median_value:.2f}"
        )


# Identify categorical columns
categorical_columns = df.select_dtypes(
    include="object"
).columns

# Fill categorical missing values using mode
for column in categorical_columns:

    if df[column].isnull().sum() > 0:

        mode_value = df[column].mode()[0]

        df[column] = df[column].fillna(mode_value)

        print(
            f"Filled missing values in {column} "
            f"using mode = {mode_value}"
        )


# Remove remaining duplicates
df = df.drop_duplicates()


print("\nMissing values after cleaning:")
print(df.isnull().sum().sum())

print("Final dataset shape:", df.shape)


# Save cleaned dataset
df.to_csv(
    os.path.join(OUTPUT_DIR, "cleaned_dataset.csv"),
    index=False
)


# SEASON DISTRIBUTION

print("\n" + "=" * 70)
print("SEASON DISTRIBUTION")
print("=" * 70)

season_counts = df["Season"].value_counts()

print(season_counts)

season_counts.to_csv(
    os.path.join(OUTPUT_DIR, "season_distribution.csv")
)


# CROP DISTRIBUTION

print("\n" + "=" * 70)
print("CROP DISTRIBUTION")
print("=" * 70)

crop_counts = df["Crop"].value_counts()

print(crop_counts)

crop_counts.to_csv(
    os.path.join(OUTPUT_DIR, "crop_distribution.csv")
)


# SEASONAL PERFORMANCE SUMMARY

print("\n" + "=" * 70)
print("SEASONAL PERFORMANCE ANALYSIS")
print("=" * 70)

performance_columns = [
    "Farm_Area_Hectares",
    "Rainfall_mm",
    "Avg_Temperature_C",
    "Humidity_pct",
    "Sunlight_Hours_Day",
    "Soil_Moisture_pct",
    "Fertilizer_kg_ha",
    "Pesticide_Litre_ha",
    "Seed_Quality_Score",
    "Yield_Tonnes_Ha",
    "Production_Tonnes",
    "Market_Price_INR_Tonne",
    "Total_Cost_INR",
    "Revenue_INR",
    "Profit_INR",
    "Water_Used_m3",
    "Water_Efficiency_t_per_1000m3",
    "Disease_Pest_Risk_pct"
]

performance_columns = [
    col for col in performance_columns
    if col in df.columns
]


seasonal_summary = df.groupby(
    "Season"
)[performance_columns].mean().round(2)

print("\nAverage performance by season:")
print(seasonal_summary)

seasonal_summary.to_csv(
    os.path.join(OUTPUT_DIR, "seasonal_summary.csv")
)


# SEASONAL MEDIAN ANALYSIS

seasonal_median = df.groupby(
    "Season"
)[performance_columns].median().round(2)

seasonal_median.to_csv(
    os.path.join(OUTPUT_DIR, "seasonal_median_summary.csv")
)


# CROP-WISE SEASONAL ANALYSIS

print("\n" + "=" * 70)
print("CROP-WISE SEASONAL ANALYSIS")
print("=" * 70)

crop_season_summary = df.groupby(
    ["Season", "Crop"]
)[[
    "Yield_Tonnes_Ha",
    "Production_Tonnes",
    "Revenue_INR",
    "Profit_INR"
]].mean().round(2)

print(crop_season_summary)

crop_season_summary.to_csv(
    os.path.join(OUTPUT_DIR, "crop_season_summary.csv")
)


# IRRIGATION METHOD ANALYSIS

print("\n" + "=" * 70)
print("IRRIGATION ANALYSIS")
print("=" * 70)

irrigation_summary = df.groupby(
    ["Season", "Irrigation_Method"]
)[[
    "Yield_Tonnes_Ha",
    "Water_Used_m3",
    "Water_Efficiency_t_per_1000m3",
    "Profit_INR"
]].mean().round(2)

print(irrigation_summary)

irrigation_summary.to_csv(
    os.path.join(OUTPUT_DIR, "irrigation_season_summary.csv")
)


# BEST SEASON BASED ON DIFFERENT PARAMETERS

print("\n" + "=" * 70)
print("BEST SEASON ANALYSIS")
print("=" * 70)

metrics = [
    "Yield_Tonnes_Ha",
    "Production_Tonnes",
    "Revenue_INR",
    "Profit_INR",
    "Water_Efficiency_t_per_1000m3"
]

for metric in metrics:

    if metric in seasonal_summary.columns:

        best_season = seasonal_summary[metric].idxmax()
        best_value = seasonal_summary[metric].max()

        print(
            f"Best season for {metric}: "
            f"{best_season} ({best_value:.2f})"
        )


# WORST SEASON ANALYSIS

print("\n" + "=" * 70)
print("LOWEST PERFORMANCE ANALYSIS")
print("=" * 70)

for metric in metrics:

    if metric in seasonal_summary.columns:

        worst_season = seasonal_summary[metric].idxmin()
        worst_value = seasonal_summary[metric].min()

        print(
            f"Lowest season for {metric}: "
            f"{worst_season} ({worst_value:.2f})"
        )


# PLOT 1 - NUMBER OF FARMS/RECORDS BY SEASON

plt.figure(figsize=(9, 6))

sns.countplot(
    data=df,
    x="Season",
    order=df["Season"].value_counts().index
)

plt.title(
    "Distribution of Agricultural Records by Season",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Number of Records")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "01_season_distribution.png"
    ),
    dpi=300
)

plt.show()


# PLOT 2 - AVERAGE YIELD BY SEASON

yield_by_season = df.groupby(
    "Season"
)["Yield_Tonnes_Ha"].mean().sort_values(
    ascending=False
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=yield_by_season.index,
    y=yield_by_season.values
)

plt.title(
    "Average Agricultural Yield by Season",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Average Yield (Tonnes/Ha)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "02_average_yield_by_season.png"
    ),
    dpi=300
)

plt.show()


# PLOT 3 - PRODUCTION BY SEASON

production_by_season = df.groupby(
    "Season"
)["Production_Tonnes"].mean().sort_values(
    ascending=False
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=production_by_season.index,
    y=production_by_season.values
)

plt.title(
    "Average Production by Season",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Average Production (Tonnes)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "03_production_by_season.png"
    ),
    dpi=300
)

plt.show()


# PLOT 4 - PROFIT BY SEASON

profit_by_season = df.groupby(
    "Season"
)["Profit_INR"].mean().sort_values(
    ascending=False
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=profit_by_season.index,
    y=profit_by_season.values
)

plt.title(
    "Average Profit by Season",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Average Profit (INR)")

plt.axhline(
    y=0,
    linestyle="--"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "04_profit_by_season.png"
    ),
    dpi=300
)

plt.show()


# PLOT 5 - REVENUE VS COST

economic_summary = df.groupby(
    "Season"
)[[
    "Revenue_INR",
    "Total_Cost_INR"
]].mean()

economic_summary.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title(
    "Average Revenue and Cost by Season",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Amount (INR)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "05_revenue_vs_cost.png"
    ),
    dpi=300
)

plt.show()


# PLOT 6 - RAINFALL BY SEASON

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="Season",
    y="Rainfall_mm"
)

plt.title(
    "Rainfall Variation Across Seasons",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Rainfall (mm)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "06_rainfall_by_season.png"
    ),
    dpi=300
)

plt.show()


# PLOT 7 - TEMPERATURE BY SEASON

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="Season",
    y="Avg_Temperature_C"
)

plt.title(
    "Temperature Variation Across Seasons",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Average Temperature (°C)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "07_temperature_by_season.png"
    ),
    dpi=300
)

plt.show()


# PLOT 8 - WATER USAGE BY SEASON

water_summary = df.groupby(
    "Season"
)["Water_Used_m3"].mean().sort_values(
    ascending=False
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=water_summary.index,
    y=water_summary.values
)

plt.title(
    "Average Water Usage by Season",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Water Used (m³)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "08_water_usage_by_season.png"
    ),
    dpi=300
)

plt.show()


# PLOT 9 - WATER EFFICIENCY

efficiency_summary = df.groupby(
    "Season"
)["Water_Efficiency_t_per_1000m3"].mean().sort_values(
    ascending=False
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=efficiency_summary.index,
    y=efficiency_summary.values
)

plt.title(
    "Water Efficiency Across Seasons",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel(
    "Water Efficiency "
    "(Tonnes per 1000 m³)"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "09_water_efficiency.png"
    ),
    dpi=300
)

plt.show()


# PLOT 10 - DISEASE/PEST RISK

risk_summary = df.groupby(
    "Season"
)["Disease_Pest_Risk_pct"].mean().sort_values(
    ascending=False
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=risk_summary.index,
    y=risk_summary.values
)

plt.title(
    "Average Disease and Pest Risk by Season",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Disease/Pest Risk (%)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "10_disease_pest_risk.png"
    ),
    dpi=300
)

plt.show()


# PLOT 11 - YIELD DISTRIBUTION BY SEASON

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="Season",
    y="Yield_Tonnes_Ha"
)

plt.title(
    "Yield Distribution Across Seasons",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Yield (Tonnes/Ha)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "11_yield_distribution.png"
    ),
    dpi=300
)

plt.show()


# PLOT 12 - CROP VS SEASON YIELD

crop_yield = df.pivot_table(
    index="Crop",
    columns="Season",
    values="Yield_Tonnes_Ha",
    aggfunc="mean"
)

plt.figure(figsize=(12, 7))

sns.heatmap(
    crop_yield,
    annot=True,
    fmt=".2f",
    cmap="YlGnBu"
)

plt.title(
    "Average Crop Yield Across Seasons",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Crop")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "12_crop_season_yield_heatmap.png"
    ),
    dpi=300
)

plt.show()


# PLOT 13 - IRRIGATION METHOD VS YIELD

plt.figure(figsize=(11, 6))

sns.barplot(
    data=df,
    x="Irrigation_Method",
    y="Yield_Tonnes_Ha",
    hue="Season"
)

plt.title(
    "Yield by Irrigation Method and Season",
    fontsize=15
)

plt.xlabel("Irrigation Method")
plt.ylabel("Average Yield (Tonnes/Ha)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "13_irrigation_yield.png"
    ),
    dpi=300
)

plt.show()


# PLOT 14 - FERTILIZER VS YIELD

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="Fertilizer_kg_ha",
    y="Yield_Tonnes_Ha",
    hue="Season",
    alpha=0.6
)

plt.title(
    "Relationship Between Fertilizer Use and Yield",
    fontsize=15
)

plt.xlabel("Fertilizer (kg/ha)")
plt.ylabel("Yield (Tonnes/Ha)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "14_fertilizer_vs_yield.png"
    ),
    dpi=300
)

plt.show()


# PLOT 15 - RAINFALL VS YIELD

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="Rainfall_mm",
    y="Yield_Tonnes_Ha",
    hue="Season",
    alpha=0.6
)

plt.title(
    "Relationship Between Rainfall and Yield",
    fontsize=15
)

plt.xlabel("Rainfall (mm)")
plt.ylabel("Yield (Tonnes/Ha)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "15_rainfall_vs_yield.png"
    ),
    dpi=300
)

plt.show()


# PLOT 16 - TEMPERATURE VS YIELD

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="Avg_Temperature_C",
    y="Yield_Tonnes_Ha",
    hue="Season",
    alpha=0.6
)

plt.title(
    "Relationship Between Temperature and Yield",
    fontsize=15
)

plt.xlabel("Average Temperature (°C)")
plt.ylabel("Yield (Tonnes/Ha)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "16_temperature_vs_yield.png"
    ),
    dpi=300
)

plt.show()


# PLOT 17 - SOIL MOISTURE VS YIELD

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="Soil_Moisture_pct",
    y="Yield_Tonnes_Ha",
    hue="Season",
    alpha=0.6
)

plt.title(
    "Relationship Between Soil Moisture and Yield",
    fontsize=15
)

plt.xlabel("Soil Moisture (%)")
plt.ylabel("Yield (Tonnes/Ha)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "17_soil_moisture_vs_yield.png"
    ),
    dpi=300
)

plt.show()


# CORRELATION ANALYSIS

print("\n" + "=" * 70)
print("CORRELATION ANALYSIS")
print("=" * 70)

correlation_data = df.select_dtypes(
    include=np.number
)

correlation_matrix = correlation_data.corr()

print(
    correlation_matrix[
        "Yield_Tonnes_Ha"
    ].sort_values(
        ascending=False
    )
)

correlation_matrix.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "correlation_matrix.csv"
    )
)


# CORRELATION HEATMAP

plt.figure(figsize=(16, 12))

sns.heatmap(
    correlation_matrix,
    cmap="coolwarm",
    center=0,
    annot=False
)

plt.title(
    "Correlation Matrix of Agricultural Variables",
    fontsize=16
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "18_correlation_heatmap.png"
    ),
    dpi=300
)

plt.show()


# PEARSON CORRELATION WITH YIELD

print("\n" + "=" * 70)
print("PEARSON CORRELATION WITH YIELD")
print("=" * 70)

target = "Yield_Tonnes_Ha"

correlation_results = []

for column in numeric_columns:

    if column == target:
        continue

    try:

        temp = df[[column, target]].dropna()

        correlation, p_value = pearsonr(
            temp[column],
            temp[target]
        )

        correlation_results.append({
            "Variable": column,
            "Correlation": correlation,
            "P_Value": p_value
        })

    except Exception:
        pass


correlation_results = pd.DataFrame(
    correlation_results
).sort_values(
    "Correlation",
    ascending=False
)

print(correlation_results)

correlation_results.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "yield_pearson_correlation.csv"
    ),
    index=False
)


# ANOVA - YIELD DIFFERENCE BETWEEN SEASONS

print("\n" + "=" * 70)
print("ANOVA TEST: YIELD VS SEASON")
print("=" * 70)

season_groups = []

for season in df["Season"].dropna().unique():

    values = df.loc[
        df["Season"] == season,
        "Yield_Tonnes_Ha"
    ].dropna()

    season_groups.append(values)


if len(season_groups) >= 2:

    f_statistic, p_value = f_oneway(
        *season_groups
    )

    print("F-statistic:", round(f_statistic, 4))
    print("P-value:", round(p_value, 6))

    if p_value < 0.05:

        print(
            "\nConclusion: There is a statistically "
            "significant difference in average yield "
            "between at least some seasons."
        )

    else:

        print(
            "\nConclusion: No statistically significant "
            "difference in average yield was detected "
            "between seasons."
        )


# PROFITABILITY ANALYSIS

print("\n" + "=" * 70)
print("PROFITABILITY ANALYSIS")
print("=" * 70)

profitability = df.groupby(
    "Season"
).agg(
    Average_Revenue=("Revenue_INR", "mean"),
    Average_Cost=("Total_Cost_INR", "mean"),
    Average_Profit=("Profit_INR", "mean")
)

profitability[
    "Average_Profit_Margin_Percent"
] = (
    profitability["Average_Profit"]
    / profitability["Average_Revenue"]
) * 100

profitability = profitability.round(2)

print(profitability)

profitability.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "seasonal_profitability.csv"
    )
)


# PROFIT MARGIN PLOT

plt.figure(figsize=(9, 6))

sns.barplot(
    x=profitability.index,
    y=profitability[
        "Average_Profit_Margin_Percent"
    ]
)

plt.title(
    "Average Profit Margin by Season",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Profit Margin (%)")

plt.axhline(
    y=0,
    linestyle="--"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "19_profit_margin_by_season.png"
    ),
    dpi=300
)

plt.show()


# TOP PERFORMING CROPS

print("\n" + "=" * 70)
print("TOP PERFORMING CROPS")
print("=" * 70)

crop_performance = df.groupby(
    "Crop"
).agg(
    Average_Yield=("Yield_Tonnes_Ha", "mean"),
    Average_Production=("Production_Tonnes", "mean"),
    Average_Revenue=("Revenue_INR", "mean"),
    Average_Profit=("Profit_INR", "mean")
).sort_values(
    "Average_Yield",
    ascending=False
).round(2)

print(crop_performance)

crop_performance.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "crop_performance.csv"
    )
)


# TOP STATES

print("\n" + "=" * 70)
print("STATE-WISE PERFORMANCE")
print("=" * 70)

state_performance = df.groupby(
    "State"
).agg(
    Average_Yield=("Yield_Tonnes_Ha", "mean"),
    Average_Production=("Production_Tonnes", "mean"),
    Average_Revenue=("Revenue_INR", "mean"),
    Average_Profit=("Profit_INR", "mean")
).sort_values(
    "Average_Yield",
    ascending=False
).round(2)

print(state_performance)

state_performance.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "state_performance.csv"
    )
)


# SEASON × CROP PROFIT ANALYSIS

season_crop_profit = df.pivot_table(
    index="Crop",
    columns="Season",
    values="Profit_INR",
    aggfunc="mean"
)

plt.figure(figsize=(12, 8))

sns.heatmap(
    season_crop_profit,
    annot=True,
    fmt=".0f",
    cmap="RdYlGn",
    center=0
)

plt.title(
    "Average Profit by Crop and Season",
    fontsize=15
)

plt.xlabel("Season")
plt.ylabel("Crop")

plt.tight_layout()

plt.savefig(
    os.path.join(
        PLOT_DIR,
        "20_crop_season_profit_heatmap.png"
    ),
    dpi=300
)

plt.show()


# OUTLIER ANALYSIS

print("\n" + "=" * 70)
print("OUTLIER ANALYSIS")
print("=" * 70)

outlier_results = []

outlier_columns = [
    "Yield_Tonnes_Ha",
    "Production_Tonnes",
    "Revenue_INR",
    "Profit_INR",
    "Water_Used_m3"
]

for column in outlier_columns:

    if column not in df.columns:
        continue

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    outlier_results.append({
        "Variable": column,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "Lower_Bound": lower_bound,
        "Upper_Bound": upper_bound,
        "Outlier_Count": len(outliers)
    })

    print(
        f"{column}: {len(outliers)} outliers"
    )


outlier_results = pd.DataFrame(
    outlier_results
)

outlier_results.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "outlier_analysis.csv"
    ),
    index=False
)


# AUTOMATIC KEY INSIGHTS

print("\n" + "=" * 70)
print("KEY DATA-DRIVEN INSIGHTS")
print("=" * 70)

best_yield_season = seasonal_summary[
    "Yield_Tonnes_Ha"
].idxmax()

best_profit_season = seasonal_summary[
    "Profit_INR"
].idxmax()

best_efficiency_season = seasonal_summary[
    "Water_Efficiency_t_per_1000m3"
].idxmax()

highest_risk_season = seasonal_summary[
    "Disease_Pest_Risk_pct"
].idxmax()

highest_rainfall_season = seasonal_summary[
    "Rainfall_mm"
].idxmax()

lowest_water_usage_season = seasonal_summary[
    "Water_Used_m3"
].idxmin()

print(
    f"\n1. Highest average yield: {best_yield_season}"
)

print(
    f"2. Highest average profit: {best_profit_season}"
)

print(
    f"3. Highest water efficiency: "
    f"{best_efficiency_season}"
)

print(
    f"4. Highest disease/pest risk: "
    f"{highest_risk_season}"
)

print(
    f"5. Highest average rainfall: "
    f"{highest_rainfall_season}"
)

print(
    f"6. Lowest average water usage: "
    f"{lowest_water_usage_season}"
)


# GENERATE TEXT REPORT

report_path = os.path.join(
    OUTPUT_DIR,
    "analysis_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "SEASONAL AGRICULTURE PERFORMANCE ANALYSIS\n"
    )

    report.write("=" * 60 + "\n\n")

    report.write(
        f"Total records: {len(df)}\n"
    )

    report.write(
        f"Total variables: {len(df.columns)}\n\n"
    )

    report.write(
        "KEY INSIGHTS\n"
    )

    report.write("-" * 60 + "\n")

    report.write(
        f"Highest average yield season: "
        f"{best_yield_season}\n"
    )

    report.write(
        f"Highest average profit season: "
        f"{best_profit_season}\n"
    )

    report.write(
        f"Highest water efficiency season: "
        f"{best_efficiency_season}\n"
    )

    report.write(
        f"Highest disease/pest risk season: "
        f"{highest_risk_season}\n"
    )

    report.write(
        f"Highest rainfall season: "
        f"{highest_rainfall_season}\n"
    )

    report.write(
        f"Lowest water usage season: "
        f"{lowest_water_usage_season}\n"
    )

    report.write("\n\nSEASONAL SUMMARY\n")
    report.write("-" * 60 + "\n")

    report.write(
        seasonal_summary.to_string()
    )


# FINAL OUTPUT

print("\n" + "=" * 70)
print("PROJECT ANALYSIS COMPLETED")
print("=" * 70)

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nGenerated files include:")

for root, directories, files in os.walk(OUTPUT_DIR):

    for file in files:

        print(
            os.path.join(root, file)
        )

print("\nAll analysis and plots have been generated successfully.")
print("=" * 70)
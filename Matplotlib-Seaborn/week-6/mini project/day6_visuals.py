import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================================================
# DAY 6: VISUALIZATION
# Dataset: Bangalore Zomato Data (zomato_features.csv & long)
# Purpose: Generate Dashboard 1, Dashboard 2, and Story Chart.
# Rules: Title, labeled axes, question answered on every chart.
#        plt.savefig() called BEFORE plt.close().
# ============================================================

current_dir = Path(__file__).resolve().parent
output_dir = current_dir / "outputs"
output_dir.mkdir(exist_ok=True)

features_file = current_dir / "zomato_features.csv"
long_file = current_dir / "zomato_cuisines_long.csv"

df = pd.read_csv(features_file)
df_long = pd.read_csv(long_file)

sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.size": 10, "figure.autolayout": False})

print("=" * 70)
print("DAY 6: DATA VISUALIZATION GENERATION")
print("=" * 70)


# ------------------------------------------------------------
# 1. DASHBOARD 1: OVERVIEW & MARKET STRUCTURE (2x2)
# ------------------------------------------------------------
print("\n[1/3] Generating Dashboard 1: Market Structure Overview...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Bangalore Zomato Overview — Dashboard 1: Market Structure & Distribution", fontsize=18, fontweight="bold", y=0.98)

# [0, 0] Top 10 Locations
top_locs = df["area"].value_counts().head(10)
palette1 = sns.color_palette("mako", len(top_locs))
sns.barplot(x=top_locs.values, y=top_locs.index, ax=axes[0, 0], palette=palette1, hue=top_locs.index, legend=False)
axes[0, 0].set_title("Q: Where is Bangalore's restaurant scene concentrated?\nTop 10 Locations by Restaurant Count", fontweight="bold", pad=10)
axes[0, 0].set_xlabel("Number of Restaurants")
axes[0, 0].set_ylabel("Neighborhood / Area")
for i, v in enumerate(top_locs.values):
    axes[0, 0].text(v + 5, i, f"{v:,}", va="center", fontsize=9, fontweight="semibold")

# [0, 1] Delivery Rating Distribution
valid_ratings = df["delivery_ratings"].dropna()
sns.histplot(valid_ratings, bins=25, kde=True, ax=axes[0, 1], color="#3498DB", edgecolor="black", alpha=0.6)
mean_r = valid_ratings.mean()
median_r = valid_ratings.median()
axes[0, 1].axvline(mean_r, color="#E74C3C", linestyle="--", linewidth=2, label=f"Mean: {mean_r:.2f}")
axes[0, 1].axvline(median_r, color="#2ECC71", linestyle="-.", linewidth=2, label=f"Median: {median_r:.2f}")
axes[0, 1].set_title("Q: How are customer ratings distributed across the city?\nDelivery Rating Distribution", fontweight="bold", pad=10)
axes[0, 1].set_xlabel("Delivery Rating (out of 5.0)")
axes[0, 1].set_ylabel("Restaurant Count")
axes[0, 1].legend(loc="upper left")

# [1, 0] Price Band Distribution
price_counts = df["price_band"].value_counts(sort=False)
palette2 = sns.color_palette("viridis", len(price_counts))
bars = axes[1, 0].bar(price_counts.index.astype(str), price_counts.values, color=palette2, edgecolor="black")
axes[1, 0].set_title("Q: What is the dominant price tier for dining in Bangalore?\nRestaurant Volume by Price Band", fontweight="bold", pad=10)
axes[1, 0].set_xlabel("Price Band (Average Cost for Two in INR)")
axes[1, 0].set_ylabel("Restaurant Count")
axes[1, 0].tick_params(axis="x", rotation=15)
total_eats = len(df)
for bar in bars:
    yval = bar.get_height()
    pct = (yval / total_eats) * 100
    axes[1, 0].text(bar.get_x() + bar.get_width()/2, yval + 50, f"{yval:,}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9)

# [1, 1] Indoor Seating vs Delivery Rating Boxplot
box_df = df.dropna(subset=["delivery_ratings"]).copy()
box_df["seating_label"] = box_df["is_indoor_seating"].map({0: "Takeaway / Cloud Kitchen (0)", 1: "Dine-in / Seating Available (1)"})
sns.boxplot(x="seating_label", y="delivery_ratings", data=box_df, ax=axes[1, 1], palette=["#E67E22", "#1ABC9C"], hue="seating_label", legend=False, width=0.45)
axes[1, 1].set_title("Q: Does providing dine-in seating correlate with higher delivery satisfaction?\nIndoor Seating vs Delivery Rating", fontweight="bold", pad=10)
axes[1, 1].set_xlabel("Operational Format")
axes[1, 1].set_ylabel("Delivery Rating")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
dash1_path = output_dir / "dashboard_1_overview.png"
plt.savefig(dash1_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"-> Saved: {dash1_path.name}")


# ------------------------------------------------------------
# 2. DASHBOARD 2: DEEP DIVE — CUISINES, ECONOMICS & HEATMAP (2x2)
# ------------------------------------------------------------
print("\n[2/3] Generating Dashboard 2: Deep Dive Analytics...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Bangalore Zomato Deep Dive — Dashboard 2: Cuisines, Economics & Geographies", fontsize=18, fontweight="bold", y=0.98)

# [0, 0] Location x Price Band Rating Heatmap
top_8_areas = df["area"].value_counts().head(8).index
heat_data = df[df["area"].isin(top_8_areas)].pivot_table(
    index="area",
    columns="price_band",
    values="delivery_ratings",
    aggfunc="mean"
)
sns.heatmap(heat_data, ax=axes[0, 0], cmap="YlGnBu", annot=True, fmt=".2f", vmin=3.5, vmax=4.3, cbar_kws={"label": "Avg Delivery Rating"})
axes[0, 0].set_title("Q: Which neighborhoods deliver highest satisfaction per price band?\nAverage Delivery Rating by Area and Price Band", fontweight="bold", pad=10)
axes[0, 0].set_xlabel("Price Band")
axes[0, 0].set_ylabel("Neighborhood")

# [0, 1] Top 10 Cuisines (from exploded long table)
top_cuisines = df_long["cuisine"].value_counts().head(10)
sns.barplot(x=top_cuisines.values, y=top_cuisines.index, ax=axes[0, 1], palette="flare", hue=top_cuisines.index, legend=False)
axes[0, 1].set_title("Q: What are Bangalore's most widely available individual cuisines?\nTop 10 Cuisines (Exploded Table)", fontweight="bold", pad=10)
axes[0, 1].set_xlabel("Frequency (Outlets Offering Cuisine)")
axes[0, 1].set_ylabel("Cuisine")
for i, v in enumerate(top_cuisines.values):
    axes[0, 1].text(v + 20, i, f"{v:,}", va="center", fontsize=9)

# [1, 0] Average Cost vs Delivery Rating Scatter
scatter_df = df.dropna(subset=["delivery_ratings", "average_cost"]).copy()
scatter_df = scatter_df[scatter_df["average_cost"] <= 2500]  # Focus view on mainstream spectrum
sns.scatterplot(
    x="average_cost",
    y="delivery_ratings",
    hue="is_indoor_seating",
    palette={0: "#E67E22", 1: "#2980B9"},
    data=scatter_df,
    alpha=0.5,
    s=35,
    ax=axes[1, 0]
)
axes[1, 0].axhline(4.0, color="gray", linestyle=":", linewidth=1.5)
axes[1, 0].set_title("Q: Does spending more money guarantee better customer ratings?\nAverage Cost vs Delivery Rating (Filtered <= ₹2,500)", fontweight="bold", pad=10)
axes[1, 0].set_xlabel("Average Cost for Two (INR)")
axes[1, 0].set_ylabel("Delivery Rating")
axes[1, 0].legend(title="Seating", labels=["Takeaway/Cloud", "Dine-in"], loc="lower right")

# [1, 1] Vegetarian vs Non-Vegetarian Cost Distribution
veg_df = df.copy()
veg_df["diet_type"] = veg_df["is_veg_only"].map({0: "Non-Veg / Multi-Diet (92.8%)", 1: "Pure Vegetarian (7.2%)"})
sns.boxplot(x="diet_type", y="average_cost", data=veg_df, ax=axes[1, 1], palette=["#C0392B", "#27AE60"], hue="diet_type", legend=False, width=0.45, showfliers=False)
axes[1, 1].set_title("Q: Do pure vegetarian eateries charge differently than non-veg places?\nCost Distribution by Diet Type (Excluding Extreme Fliers)", fontweight="bold", pad=10)
axes[1, 1].set_xlabel("Dietary Category")
axes[1, 1].set_ylabel("Average Cost for Two (INR)")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
dash2_path = output_dir / "dashboard_2_deep_dive.png"
plt.savefig(dash2_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"-> Saved: {dash2_path.name}")


# ------------------------------------------------------------
# 3. STORY CHART: THE SWEET SPOT OF BANGALORE DINING
# ------------------------------------------------------------
print("\n[3/3] Generating Annotated Story Chart: The Bangalore Sweet Spot...")

fig, ax = plt.subplots(figsize=(12, 8))

# Filter focused range for visualization
story_data = df.dropna(subset=["delivery_ratings"]).copy()
story_data = story_data[story_data["average_cost"] <= 2000]

# Scatter plot
sns.scatterplot(
    x="average_cost",
    y="delivery_ratings",
    size="total_reviews",
    sizes=(25, 400),
    color="#34495E",
    alpha=0.4,
    data=story_data,
    ax=ax,
    legend=False
)

# Reference boundary lines for "The Sweet Spot"
ax.axhline(4.2, color="#27AE60", linestyle="--", linewidth=2, label="High Quality Benchmark (Rating >= 4.2)")
ax.axvline(300, color="#E67E22", linestyle="--", linewidth=2, label="Budget Boundary (Cost <= ₹300)")

# Highlight Sweet Spot Box
ax.axvspan(0, 300, ymin=(4.2 - 2.0)/(5.0 - 2.0), ymax=1.0, color="#2ECC71", alpha=0.15)
ax.text(150, 4.85, "THE SWEET SPOT\n(High Quality, Budget Cost)", color="#196F3D", fontsize=12, fontweight="bold", ha="center", bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#27AE60", lw=1.5))

# Annotations for key iconic institutions
sweet_spot_sample = story_data[(story_data["average_cost"] <= 250) & (story_data["delivery_ratings"] >= 4.5) & (story_data["total_reviews"] > 3000)].head(3)

for _, r in sweet_spot_sample.iterrows():
    ax.annotate(
        f"{r['name']}\n(INR {r['average_cost']}, Rating: {r['delivery_ratings']}, {r['total_reviews']:,} rev)",
        xy=(r["average_cost"], r["delivery_ratings"]),
        xytext=(r["average_cost"] + 120, r["delivery_ratings"] - 0.15),
        arrowprops=dict(facecolor="#196F3D", shrink=0.08, width=1.5, headwidth=6),
        fontsize=9,
        fontweight="bold",
        color="#145A32",
        bbox=dict(boxstyle="round,pad=0.3", fc="#E8F8F5", ec="#27AE60", alpha=0.9)
    )

# Annotate the Overrated Luxury quadrant
ax.annotate(
    "OVERRATED ZONE\n(Cost >= ₹1,000, Rating < 3.6)\nHigh spend does NOT guarantee\ncustomer satisfaction",
    xy=(1400, 3.2),
    xytext=(1100, 2.5),
    arrowprops=dict(facecolor="#C0392B", shrink=0.08, width=1.5, headwidth=6),
    fontsize=9,
    fontweight="bold",
    color="#922B21",
    bbox=dict(boxstyle="round,pad=0.3", fc="#FDEDEC", ec="#C0392B", alpha=0.9)
)

ax.set_title(
    "The Bangalore Dining Sweet Spot: High Satisfaction Thrives at Low Price Points\n"
    "Key Insight: Over 700 restaurants achieve elite 4.2+ ratings under ₹300, proving price is decoupled from food excellence.",
    fontsize=13,
    fontweight="bold",
    pad=15
)
ax.set_xlabel("Average Cost for Two in INR (₹)", fontsize=11, fontweight="bold")
ax.set_ylabel("Customer Delivery Rating (out of 5.0)", fontsize=11, fontweight="bold")
ax.set_ylim(2.0, 5.0)
ax.set_xlim(0, 2000)
ax.legend(loc="lower left", frameon=True)

story_path = output_dir / "story_chart_annotated.png"
plt.savefig(story_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"-> Saved: {story_path.name}")

print("\n" + "=" * 70)
print("DAY 6 VISUALIZATION COMPLETE — ALL OUTPUTS GENERATED")
print("=" * 70)

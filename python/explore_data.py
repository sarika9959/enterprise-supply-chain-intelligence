import pandas as pd

orders = pd.read_csv(r"C:\Users\banot\Supply-Chain-Project\data\orders.csv")
suppliers = pd.read_csv(r"C:\Users\banot\Supply-Chain-Project\data\suppliers.csv")

print(orders.shape)
print(orders.head())
print(orders["status"].value_counts())
on_time_rate = (orders["status"] == "Delivered").sum() / len(orders) * 100
print(f"\nOn-time delivery rate: {on_time_rate:.2f}%")

delayed_rate = (orders["status"] == "Delayed").sum() / len(orders) * 100
print(f"Delayed rate: {delayed_rate:.2f}%")

# Merge orders with supplier info so we can see supplier names, not just IDs
merged = orders.merge(suppliers, on="supplier_id")

# Calculate on-time rate per supplier
supplier_performance = merged.groupby("supplier_name").apply(
    lambda x: (x["status"] == "Delivered").sum() / len(x) * 100
).reset_index(name="on_time_rate")

# Sort worst to best
supplier_performance = supplier_performance.sort_values("on_time_rate")

print("\n--- WORST 10 SUPPLIERS (by on-time rate) ---")
print(supplier_performance.head(10).to_string(index=False))

print("\n--- BEST 10 SUPPLIERS (by on-time rate) ---")
print(supplier_performance.tail(10).to_string(index=False))

print("\n--- ON-TIME RATE BY SUPPLIER RELIABILITY TIER ---")
tier_perf = merged.groupby("reliability_tier").apply(
    lambda x: (x["status"] == "Delivered").sum() / len(x) * 100
).reset_index(name="on_time_rate")
print(tier_perf.to_string(index=False))

print("\n--- ON-TIME RATE BY REGION ---")
region_perf = merged.groupby("region").apply(
    lambda x: (x["status"] == "Delivered").sum() / len(x) * 100
).reset_index(name="on_time_rate")
print(region_perf.sort_values("on_time_rate").to_string(index=False))

print("\n--- ON-TIME RATE BY ORDER PRIORITY ---")
priority_perf = merged.groupby("priority").apply(
    lambda x: (x["status"] == "Delivered").sum() / len(x) * 100
).reset_index(name="on_time_rate")
print(priority_perf.sort_values("on_time_rate").to_string(index=False))

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Professional styling settings
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.titleweight"] = "bold"

COLOR_PRIMARY = "#003057"   # deep navy - looks corporate/Volvo-like
COLOR_ACCENT = "#00A8E8"    # bright blue accent
COLOR_WARN = "#E63946"      # red for "bad" values

# ---------- Chart 1: On-Time Rate by Supplier Tier ----------
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(tier_perf["reliability_tier"], tier_perf["on_time_rate"],
              color=[COLOR_PRIMARY, COLOR_ACCENT, COLOR_WARN])
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f"{height:.1f}%",
            ha="center", fontsize=11, fontweight="bold")
ax.set_title("On-Time Delivery Rate by Supplier Reliability Tier", fontsize=14, pad=15)
ax.set_ylabel("On-Time Rate (%)", fontsize=11)
ax.set_xlabel("Supplier Tier", fontsize=11)
ax.set_ylim(0, 100)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(r"C:\Users\banot\Supply-Chain-Project\charts\ontime_by_tier.png", dpi=200)
plt.show()

# ---------- Chart 2: Worst 10 Suppliers ----------
fig, ax = plt.subplots(figsize=(9, 5.5))
worst10 = supplier_performance.head(10).sort_values("on_time_rate")
bars = ax.barh(worst10["supplier_name"], worst10["on_time_rate"], color=COLOR_WARN)
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, f"{width:.1f}%",
            va="center", fontsize=10, fontweight="bold")
ax.set_title("10 Lowest-Performing Suppliers by On-Time Rate", fontsize=14, pad=15)
ax.set_xlabel("On-Time Rate (%)", fontsize=11)
ax.set_xlim(0, 100)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(r"C:\Users\banot\Supply-Chain-Project\charts\worst_suppliers.png", dpi=200)
plt.show()

# ---------- Chart 3: Delay Trend Over Time ----------
orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["order_month"] = orders["order_date"].dt.to_period("M")
monthly_delay = orders.groupby("order_month").apply(
    lambda x: (x["status"] == "Delayed").sum() / len(x) * 100
)
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(monthly_delay.index.astype(str), monthly_delay.values,
        marker="o", markersize=4, linewidth=2, color=COLOR_PRIMARY)
ax.fill_between(range(len(monthly_delay)), monthly_delay.values, alpha=0.1, color=COLOR_PRIMARY)
ax.set_title("Monthly Delay Rate Trend", fontsize=14, pad=15)
ax.set_ylabel("Delay Rate (%)", fontsize=11)
ax.set_xlabel("Month", fontsize=11)
ax.tick_params(axis="x", rotation=45, labelsize=8)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig(r"C:\Users\banot\Supply-Chain-Project\charts\delay_trend.png", dpi=200)
plt.show()

print("\n✅ All charts saved to charts/ folder")
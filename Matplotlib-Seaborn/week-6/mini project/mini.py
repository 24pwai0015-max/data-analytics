import subprocess
import sys
from pathlib import Path

# ============================================================
# BANGALORE ZOMATO MINI PROJECT — MASTER RUNNER
# Script: mini.py
# Purpose: Orchestrates and runs the complete 7-Day EDA Pipeline
# ============================================================

current_dir = Path(__file__).resolve().parent

DAYS = [
    ("Day 1: Inspection & Null/Duplicate Auditing", "day1_inspect.py"),
    ("Day 2: Structure, Types & Stage 1 Cleaning", "day2_clean_types.py"),
    ("Day 3: Feature Engineering & Exploded Cuisines", "day3_features.py"),
    ("Day 4: Aggregation, Crosstabs & Pivot Analysis", "day4_analysis1.py"),
    ("Day 5: Filtering, Correlations & Value Outliers", "day5_analysis2.py"),
    ("Day 6: Visualization Dashboards & Story Chart", "day6_visuals.py"),
    ("Day 7: Audit & Verification of Findings", "day7_verify.py"),
]

def run_pipeline():
    print("=" * 75)
    print("   BANGALORE ZOMATO RESTAURANT EDA — 7-DAY MINI PROJECT RUNNER")
    print("=" * 75)
    print(f"Working Directory: {current_dir}\n")

    for idx, (title, script_name) in enumerate(DAYS, start=1):
        script_path = current_dir / script_name
        print(f"\n[{idx}/7] EXECUTING: {title} ({script_name})...")
        print("-" * 75)

        if not script_path.exists():
            print(f"[ERROR] Required script '{script_name}' not found!")
            sys.exit(1)

        result = subprocess.run([sys.executable, str(script_path)], cwd=str(current_dir))

        if result.returncode != 0:
            print(f"\n[FAILURE] Execution stopped on {script_name} with return code {result.returncode}")
            sys.exit(result.returncode)

    print("\n" + "=" * 75)
    print("   ALL 7 DAYS COMPLETED & VERIFIED SUCCESSFULLY!")
    print("=" * 75)
    print("\nDeliverables generated in this directory:")
    print("  - data_dictionary.csv       (Data dictionary of 19 original columns)")
    print("  - zomato_stage1.csv         (Cleaned types, deduplicated dataset)")
    print("  - zomato_features.csv       (Engineered bands, IQR outlier flags)")
    print("  - zomato_cuisines_long.csv  (Exploded 1-to-many cuisine dataset)")
    print("  - outputs/                  (Dashboard 1, Dashboard 2, Story Chart PNGs)")
    print("  - FINDINGS.md               (8 core data-backed findings)")
    print("  - README.md                 (Project documentation & reflection)")
    print("=" * 75)

if __name__ == "__main__":
    run_pipeline()

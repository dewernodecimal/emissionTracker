import pandas as pd
import numpy as np
import os

np.random.seed(99)

OUTPUT_DIR = r"C:\Users\vedug\OneDrive\Desktop\internshipProject\test_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────
# DATASET 1: COMBINED MESSY SHEET — all 3 categories in one file
# This is the hardest test: AI must figure out what category each row is
# ─────────────────────────────────────────────────────────────────────
def make_combined_messy():

    rows = []

    # --- Cat 6: Business Travel rows mixed in ---
    travel_rows = [
        {"entry_type": "travel",    "description": "Flight BOM to LHR",       "amount": 7200,  "unit": "km",           "mode": "flight",          "date": "12/03/2024", "dept": "Sales",       "employee": "Ravi K",    "disposal": "",        "vehicle": ""},
        {"entry_type": "TRAVEL",    "description": "train journey pune-mumbai","amount": 180,   "unit": "KM",           "mode": "Train",           "date": "2024-03-15", "dept": "hr",          "employee": "Priya M",   "disposal": "",        "vehicle": ""},
        {"entry_type": "Trip",      "description": "cab to airport",           "amount": 34,    "unit": "miles",        "mode": "Taxi",            "date": "15-Mar-24",  "dept": "Finance",     "employee": "EMP2201",   "disposal": "",        "vehicle": ""},
        {"entry_type": "travel",    "description": "Hotel stay Singapore",     "amount": 3,     "unit": "nights",       "mode": "hotel",           "date": "20/03/2024", "dept": "Sales",       "employee": "Ravi K",    "disposal": "",        "vehicle": ""},
        {"entry_type": "FLIGHT",    "description": "del to sin business class","amount": 5700,  "unit": "km",           "mode": "FLIGHT",          "date": "2024-04-01", "dept": "Management",  "employee": "CEO",       "disposal": "",        "vehicle": ""},
        {"entry_type": "travel",    "description": "rental car 3 days",        "amount": "",    "unit": "",             "mode": "Car",             "date": "2024-04-02", "dept": "Sales",       "employee": "Anita S",   "disposal": "",        "vehicle": ""},   # blank amount
    ]

    # --- Cat 7: Employee Commute rows mixed in ---
    commute_rows = [
        {"entry_type": "commute",   "description": "daily drive to office",    "amount": 22,    "unit": "km",           "mode": "",                "date": "01/04/2024", "dept": "Engineering", "employee": "Suresh P",  "disposal": "",        "vehicle": "Petrol Car"},
        {"entry_type": "Commute",   "description": "metro to work",            "amount": 14,    "unit": "Km",           "mode": "",                "date": "01-04-2024", "dept": "Ops",         "employee": "Fatima Z",  "disposal": "",        "vehicle": "metro"},
        {"entry_type": "COMMUTING", "description": "bike ride",                "amount": 8,     "unit": "miles",        "mode": "",                "date": "2024-04-01", "dept": "R&D",         "employee": "Nikhil B",  "disposal": "",        "vehicle": "2-wheeler"},
        {"entry_type": "commute",   "description": "ev car",                   "amount": 30,    "unit": "km",           "mode": "",                "date": "2024/04/02", "dept": "hr",          "employee": "Meera J",   "disposal": "",        "vehicle": "EV"},
        {"entry_type": "commute",   "description": "auto rickshaw",            "amount": 5,     "unit": "KM",           "mode": "",                "date": "02/04/2024", "dept": "Ops",         "employee": "Raju D",    "disposal": "",        "vehicle": "Auto"},
        {"entry_type": "commute",   "description": "work from home",           "amount": 0,     "unit": "km",           "mode": "",                "date": "03/04/2024", "dept": "Engineering", "employee": "Suresh P",  "disposal": "",        "vehicle": "WFH"},   # edge: WFH = 0 emissions
    ]

    # --- Cat 5: Waste rows mixed in ---
    waste_rows = [
        {"entry_type": "waste",     "description": "paper shredding",          "amount": 45,    "unit": "kg",           "mode": "",                "date": "01/04/2024", "dept": "Admin",       "employee": "",          "disposal": "Recycled","vehicle": ""},
        {"entry_type": "Waste",     "description": "cafeteria food leftovers", "amount": 12.5,  "unit": "KG",           "mode": "",                "date": "2024-04-01", "dept": "Admin",       "employee": "",          "disposal": "compost", "vehicle": ""},
        {"entry_type": "WASTE",     "description": "old lab plastics",         "amount": 3,     "unit": "metric ton",   "mode": "",                "date": "01-04-2024", "dept": "Lab",         "employee": "",          "disposal": "LANDFILL","vehicle": ""},
        {"entry_type": "disposal",  "description": "broken monitors x4",       "amount": 60,    "unit": "kg",           "mode": "",                "date": "05/04/2024", "dept": "IT",          "employee": "",          "disposal": "e-waste", "vehicle": ""},
        {"entry_type": "waste",     "description": "packaging cardboard",      "amount": "",    "unit": "kg",           "mode": "",                "date": "2024-04-06", "dept": "Warehouse",   "employee": "",          "disposal": "recycling","vehicle": ""},  # blank amount
        {"entry_type": "waste",     "description": "???",                      "amount": 20,    "unit": "",             "mode": "",                "date": "07/04/2024", "dept": "",            "employee": "",          "disposal": "",        "vehicle": ""},   # totally unknown
    ]

    rows = travel_rows + commute_rows + waste_rows

    # shuffle so they're not neatly grouped — AI must classify each row
    np.random.shuffle(rows)

    df = pd.DataFrame(rows)

    path = os.path.join(OUTPUT_DIR, "combined_messy_all_categories.csv")
    df.to_csv(path, index=False)
    print(f"Saved: {path}")


# ─────────────────────────────────────────────────────────────────────
# DATASET 2: EXTREME EDGE CASES
# ─────────────────────────────────────────────────────────────────────
def make_extreme_cases():

    # --- Extreme 1: All blank values except headers ---
    df1 = pd.DataFrame({
        "date": [None]*10,
        "employee": [None]*10,
        "mode": [None]*10,
        "distance": [None]*10,
        "unit": [None]*10,
    })
    df1.to_csv(os.path.join(OUTPUT_DIR, "extreme_all_nulls.csv"), index=False)
    print("Saved: extreme_all_nulls.csv")

    # --- Extreme 2: 10,000 rows — large volume stress test ---
    n = 10000
    df2 = pd.DataFrame({
        "employee_id"   : [f"E{np.random.randint(1000,9999)}" for _ in range(n)],
        "travel_date"   : pd.date_range("2023-01-01", periods=n, freq="1h").strftime("%Y-%m-%d"),
        "mode"          : np.random.choice(["Flight","Train","Car","Bus","Metro","Hotel"], n),
        "distance_km"   : np.round(np.random.uniform(0.5, 12000, n), 2),
        "department"    : np.random.choice(["Sales","HR","Engineering","Finance","Ops","R&D"], n),
        "cost_inr"      : np.round(np.random.uniform(100, 500000, n), 2),
    })
    df2.to_csv(os.path.join(OUTPUT_DIR, "extreme_10000_rows.csv"), index=False)
    print("Saved: extreme_10000_rows.csv")

    # --- Extreme 3: Completely wrong columns — not related to emissions at all ---
    df3 = pd.DataFrame({
        "Invoice No"    : [f"INV{i}" for i in range(20)],
        "Client Name"   : np.random.choice(["ABC Corp","XYZ Ltd","Acme"], 20),
        "Product"       : np.random.choice(["Widget A","Widget B"], 20),
        "Price (USD)"   : np.round(np.random.uniform(10, 5000, 20), 2),
        "Paid"          : np.random.choice(["Yes","No"], 20),
    })
    df3.to_csv(os.path.join(OUTPUT_DIR, "extreme_wrong_columns.csv"), index=False)
    print("Saved: extreme_wrong_columns.csv")

    # --- Extreme 4: Duplicate everything — 50 rows all identical ---
    base_row = {"date": "01/04/2024", "employee": "Ravi K", "mode": "Flight", "distance": 7200, "unit": "km"}
    df4 = pd.DataFrame([base_row] * 50)   # exact same row repeated 50 times
    df4.to_csv(os.path.join(OUTPUT_DIR, "extreme_all_duplicates.csv"), index=False)
    print("Saved: extreme_all_duplicates.csv")

    # --- Extreme 5: Negative and zero values ---
    df5 = pd.DataFrame({
        "employee"  : ["E001","E002","E003","E004","E005"],
        "mode"      : ["Flight","Car","Bus","Metro","Train"],
        "distance"  : [-500, 0, -1, 99999, -0.001],   # negative and zero distances make no sense
        "unit"      : ["km","km","km","km","km"],
        "date"      : ["2024-01-01"]*5,
    })
    df5.to_csv(os.path.join(OUTPUT_DIR, "extreme_negative_values.csv"), index=False)
    print("Saved: extreme_negative_values.csv")

    # --- Extreme 6: Mixed languages / special characters in cells ---
    df6 = pd.DataFrame({
        "कर्मचारी"      : ["राहुल", "प्रिया", "Ravi", "Fatima", "João"],       # Hindi + English + Portuguese names
        "mode"          : ["उड़ान", "Flight", "vol", "フライト", "🛫"],           # flight in Hindi, French, Japanese, emoji
        "distance"      : [1200, 850, None, 3400, 200],
        "unit"          : ["km", "KM", "Miles", "किमी", ""],
        "date"          : ["01/01/2024", "2024-01-02", "Jan 3 2024", "04-01-24", ""],
    })
    df6.to_csv(os.path.join(OUTPUT_DIR, "extreme_special_characters.csv"), index=False, encoding="utf-8-sig")
    print("Saved: extreme_special_characters.csv")


# ── run all ──
if __name__ == "__main__":
    make_combined_messy()
    make_extreme_cases()
    print("\nAll datasets saved to:", OUTPUT_DIR)

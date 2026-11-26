import pandas as pd       # pandas to create and save dataframes
import numpy as np        # numpy for random number generation
import os                 # to handle file paths

# set a random seed so results are reproducible every time you run this
np.random.seed(42)

# folder where all test files will be saved
OUTPUT_DIR = r"C:\Users\vedug\OneDrive\Desktop\internshipProject\test_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)   # create the folder if it doesn't already exist


# ─────────────────────────────────────────────
# DATASET 1: Business Travel Log (Category 6)
# messy: weird column names, mixed date formats, blank cells, random typos in mode
# ─────────────────────────────────────────────
def make_travel_log():

    n = 40   # number of rows

    # messy column names — not standard, like a real employee-submitted sheet
    df = pd.DataFrame({
        "Emp ID"          : [f"EMP{np.random.randint(100,999)}" for _ in range(n)],
        "travel date"     : [
                                # mix two date formats randomly across rows
                                d.strftime("%d/%m/%Y") if np.random.rand() > 0.5
                                else d.strftime("%Y-%m-%d")
                                for d in pd.date_range("2024-01-01", periods=n, freq="3D")
                            ],
        "MODE of Travel"  : np.random.choice(
                                # intentional typos and inconsistent naming
                                ["Flight", "flight", "FLIGHT", "Train", "train",
                                 "Car", "car ", "Taxi", "hotel", "Hotel"],
                                n),
        "distance (km)"   : np.random.choice(
                                # some blanks (NaN) mixed in
                                [np.nan if np.random.rand() < 0.1
                                 else round(np.random.uniform(50, 8000), 1)
                                 for _ in range(n)]),
        "Origin"          : np.random.choice(["Mumbai", "Delhi", "Pune", "BOM", "DEL", ""], n),
        "Destination City": np.random.choice(["London", "Singapore", "Chennai", "LHR", "SIN"], n),
        "No. of nights"   : np.random.choice([None, 1, 2, 3, 5, np.nan], n),   # hotel nights, often blank
        "dept"            : np.random.choice(["Sales", "HR", "R&D", "sales", "rd", "Finance"], n),
        "cost (INR)"      : [round(np.random.uniform(500, 150000), 2) for _ in range(n)],
    })

    # randomly blank out a few distance values to simulate missing data
    df.loc[df.sample(frac=0.1).index, "distance (km)"] = np.nan

    path = os.path.join(OUTPUT_DIR, "messy_travel_log.csv")   # file path
    df.to_csv(path, index=False)                               # save as CSV
    print(f"Saved: {path}")


# ─────────────────────────────────────────────
# DATASET 2: Employee Commute Survey (Category 7)
# messy: inconsistent vehicle names, distance in mixed units, missing employee IDs
# ─────────────────────────────────────────────
def make_commute_survey():

    n = 50

    df = pd.DataFrame({
        "employee_id"      : [f"E{np.random.randint(1000,9999)}" if np.random.rand() > 0.1
                               else ""   # 10% missing employee IDs
                               for _ in range(n)],
        "Vehicle Type"     : np.random.choice(
                                # messy: abbreviations, typos, mixed case
                                ["Car - Petrol", "petrol car", "PETROL", "Diesel Car",
                                 "diesel", "EV", "Electric Vehicle", "ev",
                                 "bike", "Motorcycle", "2-wheeler",
                                 "Bus", "bus", "Metro", "metro rail", "Auto"],
                                n),
        "one_way_km"       : [round(np.random.uniform(1, 60), 1)
                               if np.random.rand() > 0.05 else None   # 5% missing
                               for _ in range(n)],
        "unit"             : np.random.choice(["km", "KM", "miles", "Km", ""], n),   # mixed units
        "days_per_week"    : np.random.choice([1, 2, 3, 4, 5, None], n),
        "Department"       : np.random.choice(["Engineering", "HR", "Ops", "eng", "operations"], n),
        "wfh days"         : np.random.choice([0, 1, 2, 3, np.nan], n),   # work from home days
    })

    path = os.path.join(OUTPUT_DIR, "messy_commute_survey.csv")
    df.to_csv(path, index=False)
    print(f"Saved: {path}")


# ─────────────────────────────────────────────
# DATASET 3: Waste Records Log (Category 5)
# messy: quantity in different units, vague waste descriptions, duplicate rows
# ─────────────────────────────────────────────
def make_waste_log():

    n = 35

    df = pd.DataFrame({
        "Date"           : pd.date_range("2024-01-01", periods=n, freq="7D").strftime("%d-%b-%Y"),
        "Waste Type"     : np.random.choice(
                                # vague and inconsistent naming
                                ["Paper", "paper waste", "Mixed Paper",
                                 "Plastic", "plastics", "packaging plastic",
                                 "Food", "food waste", "organic",
                                 "E-waste", "electronics", "old devices",
                                 "General", "MSW", "mixed waste"],
                                n),
        "qty"            : [round(np.random.uniform(0.5, 500), 2) for _ in range(n)],
        "Unit"           : np.random.choice(["kg", "KG", "tons", "metric ton", "g", "lbs"], n),
        "Disposal Method": np.random.choice(
                                ["Landfill", "landfill", "LANDFILL",
                                 "Recycled", "recycling", "recycle",
                                 "Composted", "compost",
                                 "Incinerated", "burned", ""],   # blank = unknown
                                n),
        "Vendor"         : np.random.choice(["GreenDispose Pvt", "MunicipalCorp", "EcoRecycle", "", "N/A"], n),
        "Location"       : np.random.choice(["Pune HQ", "Mumbai Office", "Lab Block A", ""], n),
    })

    # add ~5 duplicate rows to simulate real-world data entry errors
    duplicates = df.sample(5)                       # pick 5 random rows
    df = pd.concat([df, duplicates], ignore_index=True)   # append them as duplicates

    path = os.path.join(OUTPUT_DIR, "messy_waste_log.csv")
    df.to_csv(path, index=False)
    print(f"Saved: {path}")


# ─────────────────────────────────────────────
# DATASET 4: Completely empty file (edge case test)
# ─────────────────────────────────────────────
def make_empty_file():
    path = os.path.join(OUTPUT_DIR, "empty_file.csv")
    open(path, "w").close()     # create a file with nothing in it
    print(f"Saved: {path}")


# ─────────────────────────────────────────────
# DATASET 5: Headers only, no data rows (edge case test)
# ─────────────────────────────────────────────
def make_headers_only():
    df = pd.DataFrame(columns=["date", "employee", "mode", "distance", "unit"])  # columns but no rows
    path = os.path.join(OUTPUT_DIR, "headers_only.csv")
    df.to_csv(path, index=False)
    print(f"Saved: {path}")


# ── run all generators ──
if __name__ == "__main__":
    make_travel_log()       # Category 6
    make_commute_survey()   # Category 7
    make_waste_log()        # Category 5
    make_empty_file()       # edge case: empty
    make_headers_only()     # edge case: no data rows
    print("\nAll test datasets saved to:", OUTPUT_DIR)

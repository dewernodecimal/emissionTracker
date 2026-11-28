import streamlit as st                    # streamlit for the web UI
import pandas as pd                      # pandas to read CSV and Excel files
from classify import classify_dataset    # our AI classifier we wrote in classify.py

MAX_FILE_SIZE_MB    = 10                              # max file size we allow
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # convert to bytes


# ── safely load an uploaded file into a dataframe ──
def load_file(file):

    if file.size == 0:                               # file is completely empty
        st.warning(f"'{file.name}' is empty. Skipping.")
        return None

    if file.size > MAX_FILE_SIZE_BYTES:              # file is too large
        mb = file.size / (1024 * 1024)
        st.error(f"'{file.name}' is {mb:.1f} MB — exceeds the {MAX_FILE_SIZE_MB} MB limit.")
        return None

    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)                   # read CSV

        elif file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)                 # read Excel

        else:
            st.error(f"'{file.name}' is not a supported file type.")
            return None

    except Exception as e:
        st.error(f"Could not read '{file.name}'. It may be corrupted. Error: {e}")
        return None

    if df.empty:                                     # file read fine but has no rows
        st.warning(f"'{file.name}' contains no data. Skipping.")
        return None

    if len(df.columns) == 0:                         # file has no columns at all
        st.warning(f"'{file.name}' has no columns. Skipping.")
        return None

    return df                                        # all good — return the dataframe


# ── main app ──

st.title("Carbon Tracker - File Upload & AI Classifier")

st.write("Upload your CSV or Excel files. The AI will classify each file as Travel, Commute, or Waste.")
st.caption(f"Max file size: {MAX_FILE_SIZE_MB} MB. Accepted: CSV, XLSX, XLS.")

# the upload widget
uploaded_files = st.file_uploader(
    label="Choose files",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:

    for file in uploaded_files:

        st.subheader(f" {file.name}")
        st.caption(f"Size: {file.size / 1024:.1f} KB")

        # step 1: load the file into a dataframe
        df = load_file(file)

        if df is not None:

            # step 2: show basic file info
            st.write(f"**Rows:** {df.shape[0]}  |  **Columns:** {df.shape[1]}")
            st.dataframe(df.head(10))    # show first 10 rows as a table

            # step 3: send the dataframe to our AI classifier
            st.write("Classifying...")

            with st.spinner("Classifying..."):      # show a loading spinner while AI thinks
                try:
                    category = classify_dataset(df)     # call our classify function
                except Exception as e:
                    # if the API call fails (network error, quota exceeded, etc.)
                    category = "Unknown"
                    st.error(f"AI classification failed: {e}")

            # step 4: show the result — handles single or multiple categories
            category_map = {
                "Travel"  : "✈️  Category 6 — Business Travel",
                "Commute" : "🚗  Category 7 — Employee Commuting",
                "Waste"   : "🗑️  Category 5 — Waste Generated in Operations",
            }

            # split in case AI returned multiple e.g. "Travel, Waste"
            detected = [c.strip() for c in category.split(",")]

            if category == "Unknown" or not detected:
                st.warning("❓ AI could not confidently classify this file.")

            else:
                for cat in detected:                          # loop through each detected category
                    if cat in category_map:
                        st.success(f"AI detected: **{cat}** — {category_map[cat]}")

                # if more than one category found, show a note explaining why
                if len(detected) > 1:
                    st.info("ℹ️ This file contains mixed data from multiple categories.")

        st.divider()    # draw a horizontal line between files

else:
    st.info("No files uploaded yet. Please upload a CSV or Excel file.")

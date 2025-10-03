import streamlit as st
import pandas as pd
from itertools import combinations

st.set_page_config(page_title="Rail Utilisation Optimizer 🚂", layout="centered")

st.title("Rail Utilisation Optimizer 🚂")
st.write(
    "Upload an Excel (.xlsx/.xls) or CSV file with numeric values in the **first column**. "
    "The app will group them into triplets, pairs, and singles (≤ Rail Size)."
)

# Upload file
uploaded_file = st.file_uploader("Upload your file", type=["xlsx", "xls", "csv"])

# User input for rail size
target = st.number_input("Enter Rail Size", min_value=1, value=170, step=1)

def best_fit_group(values, target, r):
    best_combo = None
    best_sum = -1
    for combo in combinations(values, r):
        s = sum(combo)
        if s <= target and s > best_sum:
            best_sum = s
            best_combo = combo
    return list(best_combo) if best_combo else None, best_sum

def make_groups(values, target, r):
    groups = []
    remaining = values.copy()
    while len(remaining) >= r:
        combo, total = best_fit_group(remaining, target, r)
        if not combo:
            break
        groups.append((combo, total))
        for v in combo:
            remaining.remove(v)
    return groups, remaining

if uploaded_file:
    try:
        # Handle CSV files
        if uploaded_file.name.endswith(".csv"):
            try:
                # Try UTF-8 first
                df = pd.read_csv(uploaded_file, encoding='utf-8', sep=None, engine='python', header=None)
            except UnicodeDecodeError:
                # Fallback to Latin1
                df = pd.read_csv(uploaded_file, encoding='latin1', sep=None, engine='python', header=None)
        else:
            # Handle Excel files
            try:
                df = pd.read_excel(uploaded_file, sheet_name=0)  # first sheet
            except:
                # fallback: read all sheets and concatenate
                xls = pd.ExcelFile(uploaded_file)
                df = pd.concat([xls.parse(sheet) for sheet in xls.sheet_names])
                st.info("Excel file loaded successfully as CSV internally.")

        # Take first column
        if df.shape[1] == 0:
            st.error("No columns found in the file.")
            st.stop()

        values = df.iloc[:, 0].dropna().tolist()

        # Keep only numeric values
        cleaned_values = []
        for v in values:
            try:
                cleaned_values.append(float(v))
            except:
                pass

        if not cleaned_values:
            st.error("No numeric values found in the first column.")
            st.stop()

        # Build groups
        triplets, rem1 = make_groups(cleaned_values, target, 3)
        pairs, rem2 = make_groups(rem1, target, 2)
        singles, rem3 = make_groups(rem2, target, 1)

        st.subheader("📌 Triplets")
        if triplets:
            for g, s in triplets:
                st.write(f"{g} → Sum: {s}")
        else:
            st.write("No valid triplets found.")

        st.subheader("📌 Pairs")
        if pairs:
            for g, s in pairs:
                st.write(f"{g} → Sum: {s}")
        else:
            st.write("No valid pairs found.")

        st.subheader("📌 Singles")
        if singles:
            for g, s in singles:
                st.write(f"{g} → Sum: {s}")
        else:
            st.write("No valid singles found.")

        if rem3:
            st.subheader("📌 Unassigned values")
            st.write(rem3)

    except Exception as e:
        st.error(f"Error reading file: {e}")

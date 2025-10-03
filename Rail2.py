import streamlit as st
from itertools import combinations

st.set_page_config(page_title="Rail Utilisation Optimizer 🚂", layout="centered")

st.title("Rail Utilisation Optimizer 🚂")
st.write(
    "Paste your numeric values below (comma, space, or newline separated). "
    "The app will group them into triplets, pairs, and singles (≤ Rail Size)."
)

# Text input
input_text = st.text_area("Paste your numbers here", height=150)

# Rail size
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

if input_text:
    # Split by commas, spaces, or newlines
    import re
    raw_values = re.split(r'[,\s]+', input_text.strip())
    
    # Keep only numeric values
    values = []
    for v in raw_values:
        try:
            values.append(float(v))
        except:
            pass
    
    if not values:
        st.error("No numeric values found in the input.")
    else:
        # Build groups
        triplets, rem1 = make_groups(values, target, 3)
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

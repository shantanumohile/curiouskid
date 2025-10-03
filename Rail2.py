import streamlit as st
from itertools import combinations
import copy

st.set_page_config(page_title="Rail Optimizer - Optimal Solution", layout="centered")

st.title("Rail Optimiser 🚂 (Optimal)")
st.write(
    "Paste your numeric values below (comma, space, or newline separated). "
    "The app will group them into rails (≤ Rail Size) to **minimize total rails used**."
)

# Input numbers
input_text = st.text_area("Paste your numbers here", height=150)
target = st.number_input("Enter Rail Size", min_value=1, value=170, step=1)

def parse_input(input_text):
    import re
    raw_values = re.split(r'[,\s]+', input_text.strip())
    values = []
    for v in raw_values:
        try:
            values.append(float(v))
        except:
            pass
    return values

def find_best_bin_packing(values, rail_size):
    """
    Try all combinations of 1, 2, or 3 numbers to fill rails optimally.
    Returns list of rails.
    """
    remaining = sorted(values, reverse=True)
    rails = []

    while remaining:
        best_combo = None
        best_sum = -1

        # Generate all combos of size 1,2,3
        for r in range(3, 0, -1):
            for combo in combinations(remaining, r):
                s = sum(combo)
                if s <= rail_size and s > best_sum:
                    best_sum = s
                    best_combo = combo

        # If no combo found (shouldn't happen), take largest single
        if not best_combo:
            best_combo = [remaining[0]]
            best_sum = remaining[0]

        rails.append((list(best_combo), best_sum))
        # Remove used numbers
        for num in best_combo:
            remaining.remove(num)

    return rails

if input_text:
    values = parse_input(input_text)
    if not values:
        st.error("No numeric values found in the input.")
    else:
        rails = find_best_bin_packing(values, target)
        
        # Calculate total wastage
        total_wastage = sum(target - s for _, s in rails)
        total_rails = len(rails)
        
        # Display summary at the top
        st.subheader("📊 Summary")
        st.write(f"**Total Rails:** {total_rails}")
        st.write(f"**Total Wastage:** {total_wastage}")

        # Display each rail
        st.subheader("📌 Rails")
        for i, (nums, s) in enumerate(rails, 1):
            st.write(f"Rail {i}: {nums} → Sum: {s} (Wastage: {target - s})")

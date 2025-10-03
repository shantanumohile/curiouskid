{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNCg4/B6Oln/hxFveIDaM2f",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/shantanumohile/curiouskid/blob/main/Rail2.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "QPlnX2SeOcU5"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "from itertools import combinations\n",
        "\n",
        "st.title(\"Rail Utilisation Optimizer 🚂\")\n",
        "st.write(\"Upload an Excel file with values in the **first column**. \"\n",
        "         \"The app will group them into triplets, pairs, and singles (<= 170).\")\n",
        "\n",
        "uploaded_file = st.file_uploader(\"Upload your Excel file\", type=[\"xlsx\", \"xls\"])\n",
        "\n",
        "target = st.number_input(\"Enter Rail Size (default = 170)\", min_value=1, value=170)\n",
        "\n",
        "def best_fit_group(values, target, r):\n",
        "    best_combo = None\n",
        "    best_sum = -1\n",
        "    for combo in combinations(values, r):\n",
        "        s = sum(combo)\n",
        "        if s <= target and s > best_sum:\n",
        "            best_sum = s\n",
        "            best_combo = combo\n",
        "    return list(best_combo) if best_combo else None, best_sum\n",
        "\n",
        "def make_groups(values, target, r):\n",
        "    groups = []\n",
        "    remaining = values.copy()\n",
        "\n",
        "    while len(remaining) >= r:\n",
        "        combo, total = best_fit_group(remaining, target, r)\n",
        "        if not combo:\n",
        "            break\n",
        "        groups.append((combo, total))\n",
        "        for v in combo:\n",
        "            remaining.remove(v)\n",
        "    return groups, remaining\n",
        "\n",
        "if uploaded_file:\n",
        "    try:\n",
        "        df = pd.read_excel(uploaded_file)\n",
        "        values = df[df.columns[0]].dropna().tolist()  # Always take the first column\n",
        "\n",
        "        # Convert to numbers safely\n",
        "        values = [float(v) for v in values if str(v).replace('.', '', 1).isdigit()]\n",
        "\n",
        "        if not values:\n",
        "            st.error(\"No numeric values found in the first column of your Excel file.\")\n",
        "        else:\n",
        "            triplets, remaining_after_triplets = make_groups(values, target, 3)\n",
        "            pairs, remaining_after_pairs = make_groups(remaining_after_triplets, target, 2)\n",
        "            singles, remaining_final = make_groups(remaining_after_pairs, target, 1)\n",
        "\n",
        "            st.subheader(\"📌 Triplets\")\n",
        "            for g, s in triplets:\n",
        "                st.write(f\"{g} → Sum: {s}\")\n",
        "\n",
        "            st.subheader(\"📌 Pairs\")\n",
        "            for g, s in pairs:\n",
        "                st.write(f\"{g} → Sum: {s}\")\n",
        "\n",
        "            st.subheader(\"📌 Singles\")\n",
        "            for g, s in singles:\n",
        "                st.write(f\"{g} → Sum: {s}\")\n",
        "\n",
        "            if remaining_final:\n",
        "                st.subheader(\"📌 Unassigned values\")\n",
        "                st.write(remaining_final)\n",
        "\n",
        "    except Exception as e:\n",
        "        st.error(f\"Error reading Excel file: {e}\")\n"
      ]
    }
  ]
}
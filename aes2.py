import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Function definitions
def walsh_transform(s_box, output_mask):
    n = len(s_box)
    walsh = np.zeros(n, dtype=int)
    for a in range(n):
        sum_value = 0
        for x in range(n):
            input_parity = bin(x & a).count("1") % 2
            output_parity = bin(s_box[x] & output_mask).count("1") % 2
            sum_value += (-1) ** (input_parity ^ output_parity)
        walsh[a] = sum_value
    return walsh

def calculate_nonlinearity(s_box):
    n = len(s_box)
    m = int(np.log2(n))
    max_walsh = 0
    for output_mask in range(1, n):
        walsh = walsh_transform(s_box, output_mask)
        max_walsh = max(max_walsh, np.max(np.abs(walsh)))
    nonlinearity = (2 ** (m - 1)) - (max_walsh // 2)
    return nonlinearity

def hamming_distance(bin_str1, bin_str2):
    return sum(b1 != b2 for b1, b2 in zip(bin_str1, bin_str2))

def calculate_sac(s_box):
    n = len(s_box)
    m = int(np.log2(n))
    sac_values = []
    for i in range(m):
        sac_count = 0
        for x in range(n):
            flipped_x = x ^ (1 << i)
            output1 = s_box[x]
            output2 = s_box[flipped_x]
            hamming_dist = hamming_distance(bin(output1)[2:].zfill(m), bin(output2)[2:].zfill(m))
            sac_count += hamming_dist
        sac_values.append(sac_count / (n * m))
    return np.mean(sac_values)

def calculate_bic_nl(s_box):
    n = len(s_box)
    m = int(np.log2(n))
    bic_nl_values = []
    for bit1 in range(m):
        for bit2 in range(bit1 + 1, m):
            mask1 = 1 << bit1
            mask2 = 1 << bit2
            combined_mask = mask1 | mask2
            walsh = walsh_transform(s_box, combined_mask)
            max_walsh = np.max(np.abs(walsh))
            bic_nl = (2 ** (m - 1)) - (max_walsh // 2)
            bic_nl_values.append(bic_nl)
    return np.mean(bic_nl_values)

def calculate_bic_sac(s_box):
    n = len(s_box)
    bit_length = 8
    total_pairs = 0
    total_independence = 0

    for i in range(bit_length):
        for j in range(i + 1, bit_length):
            independence_sum = 0

            for x in range(n):
                for bit_to_flip in range(bit_length):
                    flipped_x = x ^ (1 << bit_to_flip)

                    y1 = s_box[x]
                    y2 = s_box[flipped_x]

                    b1_i = (y1 >> i) & 1
                    b1_j = (y1 >> j) & 1

                    b2_i = (y2 >> i) & 1
                    b2_j = (y2 >> j) & 1

                    independence_sum += ((b1_i ^ b2_i) ^ (b1_j ^ b2_j))

            pair_independence = independence_sum / (n * bit_length)
            total_independence += pair_independence
            total_pairs += 1

    bic_sac = total_independence / total_pairs
    return round(bic_sac, 5)

def calculate_lap(s_box):
    n = len(s_box)
    lap_values = []
    for input_mask in range(1, n):
        for output_mask in range(1, n):
            count = 0
            for x in range(n):
                input_parity = bin(x & input_mask).count("1") % 2
                output_parity = bin(s_box[x] & output_mask).count("1") % 2
                if input_parity == output_parity:
                    count += 1
            lap = abs(count - n // 2) / n
            lap_values.append(lap)
    return max(lap_values)

def calculate_dap(s_box):
    n = len(s_box)
    diff_table = np.zeros((n, n), dtype=int)
    for x1 in range(n):
        for x2 in range(n):
            input_diff = x1 ^ x2
            output_diff = s_box[x1] ^ s_box[x2]
            diff_table[input_diff][output_diff] += 1
    max_dap = 0
    for i in range(1, n):
        for j in range(n):
            probability = diff_table[i][j] / n
            if probability > max_dap:
                max_dap = probability
    return max_dap

# Streamlit GUI
st.title("S-Box Analysis Tool")
st.sidebar.header("Options")

# Upload S-Box file
uploaded_file = st.sidebar.file_uploader("Upload S-Box File (Excel)", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Uploaded S-Box")
    st.dataframe(df)

    s_box_array = df.values.flatten()

    # Operation selection
    operations = st.sidebar.multiselect("Select Operations", ["NL", "SAC", "LAP", "DAP", "BIC-SAC", "BIC-NL"])
    
    results = {}
    if "NL" in operations:
        results["Nonlinearity (NL)"] = calculate_nonlinearity(s_box_array)
    if "SAC" in operations:
        results["Strict Avalanche Criterion (SAC)"] = calculate_sac(s_box_array)
    if "BIC-NL" in operations:
        results["BIC Nonlinearity (BIC-NL)"] = calculate_bic_nl(s_box_array)
    if "BIC-SAC" in operations:
        results["BIC Strict Avalanche Criterion (BIC-SAC)"] = calculate_bic_sac(s_box_array)
    if "LAP" in operations:
        results["Linear Approximation Probability (LAP)"] = calculate_lap(s_box_array)
    if "DAP" in operations:
        results["Differential Approximation Probability (DAP)"] = calculate_dap(s_box_array)

    # Display results
    if results:
        st.subheader("Results")
        result_df = pd.DataFrame.from_dict(results, orient='index', columns=['Value'])
        st.table(result_df)

        # Export results
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            result_df.to_excel(writer, sheet_name='Results')
        st.download_button(
            label="Download Results",
            data=output.getvalue(),
            file_name="sbox_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

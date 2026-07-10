"""
Streamlit app: Extract & sum total values from a delimited "listItems" column.

Run with:
    streamlit run total_value_extractor.py
"""

import io
import re

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Total Value Extractor", layout="wide")
st.title("Extract Total Value from listItems Column")

# ---------------------------------------------------------------------------
# Core extraction logic
# ---------------------------------------------------------------------------
# Each cell can contain one or more item records separated by "---".
# Each record is pipe-delimited, and the total value for that record is
# always the numeric field immediately before "|USD|".
# Example: ...|4|1.25|5.00|USD|0.125  -> total = 5.00
TOTAL_PATTERN = re.compile(r"\|([\d.]+)\|USD\|")


def extract_total(cell):
    """
    Sum all record totals found in a single cell.
    Returns (total: float, status: str) where status flags data-quality issues:
      - "empty"      -> cell was NaN or blank string
      - "no_match"   -> cell had content but no '|USD|' pattern found (likely malformed)
      - "ok"         -> at least one total was successfully extracted
    """
    if pd.isna(cell) or str(cell).strip() == "":
        return float("nan"), "empty"

    matches = TOTAL_PATTERN.findall(str(cell))
    if not matches:
        return float("nan"), "no_match"

    try:
        total = sum(float(m) for m in matches)
    except ValueError:
        return float("nan"), "no_match"

    return total, "ok"


# ---------------------------------------------------------------------------
# UI: Upload
# ---------------------------------------------------------------------------
uploaded_file = st.file_uploader("Upload CSV or Excel file",
                                 type=["csv", "xlsx", "xls"])

if uploaded_file:
    file_name = uploaded_file.name
    base_name = file_name.rsplit(".", 1)[0]

    # --- Safely read the file ---------------------------------------------
    try:
        if file_name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(
            f"Could not read the file. It may be corrupted or in an unsupported format.\n\nDetails: {e}"
        )
        st.stop()

    if df.empty:
        st.warning("The uploaded file has no rows.")
        st.stop()

    if len(df.columns) == 0:
        st.error("The uploaded file has no columns.")
        st.stop()

    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    # Column selector, defaulting to "listItems" if present
    columns = df.columns.tolist()
    default_index = columns.index("listItems") if "listItems" in columns else 0
    col_name = st.selectbox(
        "Select the column containing listItems data",
        options=columns,
        index=default_index,
    )

    if st.button("Extract Total Value", type="primary"):
        result_df = df.copy()
        extracted = result_df[col_name].apply(extract_total)
        result_df["TotalValue (USD)"] = extracted.apply(lambda x: x[0])
        result_df["_ParseStatus"] = extracted.apply(
            lambda x: x[1])  # diagnostic only
        st.session_state["processed_df"] = result_df
        st.session_state["base_name"] = base_name

    # ---------------------------------------------------------------------
    # UI: Results + Download (persists across reruns via session_state)
    # ---------------------------------------------------------------------
    if "processed_df" in st.session_state:
        result_df = st.session_state["processed_df"]
        base_name = st.session_state["base_name"]

        st.subheader("Preview of Updated Data")
        st.dataframe(result_df.head(20))

        total_sum = result_df["TotalValue (USD)"].sum()
        st.metric("Sum of TotalValue (USD) across all rows",
                  f"${total_sum:,.2f}")

        # --- Data quality summary ------------------------------------------
        status_counts = result_df["_ParseStatus"].value_counts()
        empty_count = int(status_counts.get("empty", 0))
        no_match_count = int(status_counts.get("no_match", 0))

        if empty_count:
            st.info(
                f"{empty_count} row(s) had an empty '{col_name}' cell — TotalValue set to $0.00."
            )
        if no_match_count:
            st.warning(
                f"{no_match_count} row(s) had content in '{col_name}' but no '|USD|' pattern was found "
                f"(possible malformed data) — TotalValue set to $0.00. Review these rows before trusting the totals."
            )
            with st.expander(f"View the {no_match_count} unparsed row(s)"):
                st.dataframe(
                    result_df[result_df["_ParseStatus"] == "no_match"])

        st.subheader("Download Updated File")
        default_name = f"{base_name}_updated"
        output_name = st.text_input("Output file name (without extension)",
                                    value=default_name)

        # Build in-memory Excel file (drop internal diagnostic column before export)
        export_df = result_df.drop(columns=["_ParseStatus"], errors="ignore")
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            export_df.to_excel(writer, index=False, sheet_name="Sheet1")
        output.seek(0)

        st.download_button(
            label="Download as Excel",
            data=output,
            file_name=f"{output_name}.xlsx",
            mime=
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
else:
    st.info("Upload a CSV or Excel file to get started.")

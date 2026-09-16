"""
Surcharge Column Transformer — Streamlit App
----------------------------------------------
Takes an uploaded CSV/Excel shipping invoice file, converts selected
surcharge columns into MISC CHARGE DESCRIPTION / MISC NET AMOUNT pairs,
renumbers any pre-existing MISC CHARGE DESCRIPTION / MISC NET AMOUNT
columns to continue the sequence, previews the result, and lets the
user download the transformed file.

Run with:
    streamlit run surcharge_transformer_app.py
"""

import io
import re
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Surcharge Column Transformer", layout="wide")
st.title("Surcharge Column Transformer")
st.caption(
    "Upload a shipping invoice CSV/Excel file, choose which surcharge columns "
    "to convert into MISC CHARGE DESCRIPTION / MISC NET AMOUNT pairs, and "
    "download the transformed file.")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_SURCHARGE_COLUMNS = [
    "FUEL SURCHARGE AMOUNT",
    "RESIDENTIAL SURCHARGE AMOUNT",
    "DAS SURCHARGE AMOUNT",
    "SCC NET AMOUNT",
    "SCC FUEL SUCHARGE NET AMOUNT",
]

# Clean, human-readable labels for the known default columns. Anything the
# user selects beyond these gets a best-effort guess via guess_description().
DEFAULT_LABELS = {
    "FUEL SURCHARGE AMOUNT": "Fuel Surcharge",
    "RESIDENTIAL SURCHARGE AMOUNT": "Residential Surcharge",
    "DAS SURCHARGE AMOUNT": "DAS Surcharge",
    "SCC NET AMOUNT": "SCC",
    "SCC FUEL SUCHARGE NET AMOUNT": "SCC Fuel Surcharge",
}

# Matches "MISC CHARGE DESCRIPTION", "MISC CHARGE DESCRIPTION 3",
# or "MISC CHARGE DESCRIPTION.3" (and same patterns for MISC NET AMOUNT),
# so pre-existing numbered MISC columns in the source file are found
# regardless of which numbering style the file uses.
MISC_DESC_RE = re.compile(r"^MISC CHARGE DESCRIPTION\s*\.?\s*(\d+)?$",
                          re.IGNORECASE)
MISC_AMT_RE = re.compile(r"^MISC NET AMOUNT\s*\.?\s*(\d+)?$", re.IGNORECASE)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def guess_description(col_name: str) -> str:
    """Best-effort human-readable label for an arbitrary surcharge column."""
    name = col_name.strip()
    for suffix in (" NET AMOUNT", " AMOUNT"):
        if name.upper().endswith(suffix):
            name = name[:-len(suffix)]
            break
    label = " ".join(w.capitalize() for w in name.split())
    if "surcharge" not in label.lower():
        label += " Surcharge"
    return label


def find_existing_misc_pairs(columns):
    """
    Scan the file's columns for pre-existing MISC CHARGE DESCRIPTION /
    MISC NET AMOUNT pairs (however many there are — this scans dynamically
    rather than assuming a fixed count), matched up by their shared number,
    and returned in ascending numeric order.
    """
    desc_cols, amt_cols = {}, {}
    for col in columns:
        m = MISC_DESC_RE.match(str(col).strip())
        if m:
            desc_cols[int(m.group(1)) if m.group(1) else 0] = col
        m = MISC_AMT_RE.match(str(col).strip())
        if m:
            amt_cols[int(m.group(1)) if m.group(1) else 0] = col
    shared_nums = sorted(set(desc_cols) & set(amt_cols))
    return [(desc_cols[n], amt_cols[n]) for n in shared_nums]


def misc_col_name(base: str, index: int) -> str:
    """index 0 -> 'MISC CHARGE DESCRIPTION', index 1 -> 'MISC CHARGE DESCRIPTION.1', etc."""
    return base if index == 0 else f"{base}.{index}"


def load_file(uploaded_file) -> pd.DataFrame:
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        raw = uploaded_file.read()
        sample = raw[:5000].decode("utf-8", errors="ignore")
        # Auto-detect pipe- vs comma-delimited CSVs.
        delimiter = "|" if sample.count("|") > sample.count(",") else ","
        return pd.read_csv(io.BytesIO(raw), delimiter=delimiter, dtype=str)
    return pd.read_excel(uploaded_file, dtype=str)


def build_transformed_df(source_df, selected_columns, labels_by_column):
    """
    Convert each selected surcharge column into a MISC CHARGE DESCRIPTION /
    MISC NET AMOUNT pair, renumber any pre-existing MISC pairs to continue
    the sequence, and splice the consolidated MISC block back into the
    dataframe at the position the original surcharge/MISC columns occupied.
    """
    work_df = source_df.copy()
    existing_pairs = find_existing_misc_pairs(work_df.columns)

    involved_cols = list(selected_columns) + [
        c for pair in existing_pairs for c in pair
    ]
    insert_at = min(work_df.columns.get_loc(c) for c in involved_cols)

    new_block = pd.DataFrame(index=work_df.index)
    idx = 0

    # New pairs derived from the selected surcharge columns, in selection order.
    for src_col in selected_columns:
        label = labels_by_column[src_col]
        desc_name = misc_col_name("MISC CHARGE DESCRIPTION", idx)
        amt_name = misc_col_name("MISC NET AMOUNT", idx)
        s = work_df[src_col]
        has_value = s.notna() & (s.astype(str).str.strip() != "")
        new_block[desc_name] = [label if hv else "" for hv in has_value]
        new_block[amt_name] = s.where(has_value, "")
        idx += 1

    # Pre-existing MISC pairs, kept and renumbered to continue the sequence.
    for desc_col, amt_col in existing_pairs:
        desc_name = misc_col_name("MISC CHARGE DESCRIPTION", idx)
        amt_name = misc_col_name("MISC NET AMOUNT", idx)
        new_block[desc_name] = work_df[desc_col]
        new_block[amt_name] = work_df[amt_col]
        idx += 1

    drop_cols = set(involved_cols)
    before_cols = [
        c for c in work_df.columns[:insert_at] if c not in drop_cols
    ]
    remaining_cols = [c for c in work_df.columns if c not in drop_cols]
    after_cols = [c for c in remaining_cols if c not in before_cols]

    result_df = pd.concat(
        [work_df[before_cols], new_block, work_df[after_cols]], axis=1)
    return result_df, idx


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

uploaded_file = st.file_uploader("Upload CSV or Excel file",
                                 type=["csv", "xlsx", "xls"])

if uploaded_file is None:
    st.info("Upload a CSV or Excel file to begin.")
    st.stop()

# Reset downstream state if a new file is uploaded.
if st.session_state.get("_uploaded_name") != uploaded_file.name:
    st.session_state["_uploaded_name"] = uploaded_file.name
    st.session_state.pop("result_df", None)

df = load_file(uploaded_file)
st.success(
    f"Loaded **{uploaded_file.name}** — {df.shape[0]} rows, {df.shape[1]} columns"
)

all_columns = list(df.columns)
default_selected = [c for c in DEFAULT_SURCHARGE_COLUMNS if c in all_columns]
missing_defaults = [
    c for c in DEFAULT_SURCHARGE_COLUMNS if c not in all_columns
]
if missing_defaults:
    st.warning(
        f"Default surcharge columns not found in this file: {', '.join(missing_defaults)}"
    )

st.subheader("1. Select surcharge columns to convert")
selected_columns = st.multiselect(
    "Surcharge columns",
    options=all_columns,
    default=default_selected,
)

if selected_columns:
    st.subheader("2. Confirm MISC CHARGE DESCRIPTION labels")
    st.caption("Edit any label before processing if needed.")
    label_df = pd.DataFrame({
        "Source Column":
        selected_columns,
        "MISC CHARGE DESCRIPTION": [
            DEFAULT_LABELS.get(c, guess_description(c))
            for c in selected_columns
        ],
    })
    edited_labels = st.data_editor(
        label_df,
        hide_index=True,
        use_container_width=True,
        disabled=["Source Column"],
        key="label_editor",
    )

    if st.button("Process file", type="primary"):
        labels_by_column = dict(
            zip(edited_labels["Source Column"],
                edited_labels["MISC CHARGE DESCRIPTION"]))
        result_df, pair_count = build_transformed_df(df, selected_columns,
                                                     labels_by_column)
        st.session_state["result_df"] = result_df
        st.session_state["pair_count"] = pair_count

if "result_df" in st.session_state:
    result_df = st.session_state["result_df"]

    st.subheader("3. Preview")
    st.dataframe(result_df.head(50), use_container_width=True)
    st.caption(
        f"{result_df.shape[0]} rows x {result_df.shape[1]} columns — "
        f"{st.session_state['pair_count']} MISC CHARGE DESCRIPTION / MISC NET AMOUNT pairs "
        f"(0 to {st.session_state['pair_count'] - 1})")

    st.subheader("4. Download")
    original_stem = Path(uploaded_file.name).stem
    original_ext = Path(uploaded_file.name).suffix or ".xlsx"
    default_filename = f"{original_stem}_transformed{original_ext}"
    output_filename = st.text_input("Output file name", value=default_filename)

    if output_filename.lower().endswith(".csv"):
        buf = io.StringIO()
        result_df.to_csv(buf, index=False)
        file_bytes = buf.getvalue().encode("utf-8")
        mime = "text/csv"
    else:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            result_df.to_excel(writer, index=False, sheet_name="Transformed")
        file_bytes = buf.getvalue()
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    st.download_button(
        label="Download transformed file",
        data=file_bytes,
        file_name=output_filename,
        mime=mime,
    )

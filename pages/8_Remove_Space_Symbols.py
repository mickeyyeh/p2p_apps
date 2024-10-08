# import streamlit as st
# import pandas as pd
# import unicodedata
# import re
# from io import BytesIO
# import os

# # Function to clean data based on provided rules


# def clean_data(df, changes):
#     for change in changes:
#         selected_columns = change['columns']
#         chars_to_remove = change['chars']
#         remove_hidden = change['remove_hidden']

#         # Apply changes to selected columns or entire dataframe
#         if selected_columns:
#             df[selected_columns] = df[selected_columns].applymap(
#                 lambda x: remove_hidden_chars(x, chars_to_remove, remove_hidden))
#         else:
#             df = df.applymap(lambda x: remove_hidden_chars(
#                 x, chars_to_remove, remove_hidden))

#     return df

# # Function to remove hidden characters and specified characters


# def remove_hidden_chars(val, chars_to_remove, remove_hidden):
#     if isinstance(val, str):
#         val = unicodedata.normalize('NFKD', val)
#         # Remove hidden characters if the option is selected
#         if remove_hidden:
#             # Remove non-printable characters
#             val = re.sub(r'[^\x20-\x7E]', '', val)
#         if chars_to_remove:
#             val = re.sub(f"[{re.escape(chars_to_remove)}]", '', val)
#     return val

# # Function to handle file upload, cleaning, and download


# def export_and_clean_file(uploaded_file, changes, file_type):
#     if file_type == 'csv':
#         df = pd.read_csv(uploaded_file, dtype=str)  # Read everything as text
#     else:
#         df = pd.read_excel(uploaded_file, dtype=str)

#     df_cleaned = clean_data(df, changes)

#     # Create in-memory buffer for CSV and Excel files
#     buffer_csv = BytesIO()
#     buffer_excel = BytesIO()

#     # Save to CSV in memory
#     df_cleaned.to_csv(buffer_csv, index=False)
#     buffer_csv.seek(0)

#     # Save to Excel in memory
#     with pd.ExcelWriter(buffer_excel, engine='xlsxwriter') as writer:
#         df_cleaned.to_excel(writer, index=False)
#     buffer_excel.seek(0)

#     return df, df_cleaned, buffer_csv, buffer_excel


# # Streamlit app
# st.title('File Upload, Clean, and Download App')

# # File upload
# uploaded_file = st.file_uploader(
#     'Upload your file (Excel or CSV)', type=['xlsx', 'csv'])

# # Manage user changes
# if 'changes' not in st.session_state:
#     st.session_state.changes = []  # Store changes as a list of dictionaries

# if uploaded_file is not None:
#     # Determine file type
#     file_type = 'csv' if uploaded_file.name.endswith('.csv') else 'xlsx'

#     st.write('File uploaded successfully!')

#     # Load the data
#     if file_type == 'csv':
#         # Read CSV as text to preserve leading zeros
#         df = pd.read_csv(uploaded_file, dtype=str)
#     else:
#         # Read Excel as text to preserve leading zeros
#         df = pd.read_excel(uploaded_file, dtype=str)

#     st.subheader('Original Data')
#     st.dataframe(df)

#     # Column selection
#     columns = df.columns.tolist()
#     selected_columns = st.multiselect(
#         'Select specific columns to clean (leave empty to clean all)', columns)

#     # Input for characters or symbols to remove
#     chars_to_remove = st.text_input(
#         'Enter characters or symbols to remove (optional):', '')

#     # Checkbox to remove hidden characters
#     remove_hidden = st.checkbox(
#         'Remove hidden (non-printable) characters', value=True)

#     # Add change button
#     if st.button('Add Change'):
#         if chars_to_remove or remove_hidden:
#             # Add the new change to the session state
#             st.session_state.changes.append({
#                 'columns': selected_columns,
#                 'chars': chars_to_remove,
#                 'remove_hidden': remove_hidden,
#                 'description': f"Remove '{chars_to_remove}' from {', '.join(selected_columns) if selected_columns else 'all columns'}" + (' and hidden characters' if remove_hidden else '')
#             })

#     # Display all changes made so far
#     if st.session_state.changes:
#         st.subheader('Changes Made:')
#         for i, change in enumerate(st.session_state.changes):
#             # Checkbox to allow the user to select/unselect each change
#             if st.checkbox(change['description'], value=True, key=f'change_{i}'):
#                 change['apply'] = True
#             else:
#                 change['apply'] = False

#     # Apply changes and clean file
#     changes_to_apply = [
#         change for change in st.session_state.changes if change.get('apply')]
#     if changes_to_apply:
#         df, df_cleaned, buffer_csv, buffer_excel = export_and_clean_file(
#             uploaded_file, changes_to_apply, file_type)

#         # Show cleaned data
#         st.subheader('Cleaned Data')
#         st.dataframe(df_cleaned)

#         # File name editor
#         default_file_name = os.path.splitext(
#             uploaded_file.name)[0] + '_updated'
#         file_name_input = st.text_input(
#             'Edit file name for download:', default_file_name)

#         # Ensure valid file names
#         file_name_csv = file_name_input + '.csv'
#         file_name_excel = file_name_input + '.xlsx'

#         # Download buttons for cleaned files
#         st.download_button(
#             label='Download cleaned CSV',
#             data=buffer_csv,
#             file_name=file_name_csv,
#             mime='text/csv'
#         )

#         st.download_button(
#             label='Download cleaned Excel',
#             data=buffer_excel,
#             file_name=file_name_excel,
#             mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#         )


import streamlit as st
import pandas as pd
import unicodedata
import re
from io import BytesIO
import os
from typing import List, Dict, Any, Optional, Tuple


def clean_data(df: pd.DataFrame, changes: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Clean data based on provided rules.

    Args:
        df (pd.DataFrame): The DataFrame to be cleaned.
        changes (List[Dict[str, Any]]): A list of dictionaries containing cleaning rules.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    for change in changes:
        selected_columns: List[str] = change['columns']
        chars_to_remove: str = change['chars']
        remove_hidden: bool = change['remove_hidden']

        # Apply changes to selected columns or entire dataframe
        if selected_columns:
            df[selected_columns] = df[selected_columns].applymap(
                lambda x: remove_hidden_chars(
                    x, chars_to_remove, remove_hidden)
            )
        else:
            df = df.applymap(
                lambda x: remove_hidden_chars(
                    x, chars_to_remove, remove_hidden)
            )

    return df


def remove_hidden_chars(val: Any, chars_to_remove: str, remove_hidden: bool) -> Any:
    """
    Remove hidden characters and specified characters from a value.

    Args:
        val (Any): The value to be cleaned.
        chars_to_remove (str): Characters to remove from the value.
        remove_hidden (bool): Whether to remove hidden (non-printable) characters.

    Returns:
        Any: The cleaned value.
    """
    if isinstance(val, str):
        val = unicodedata.normalize('NFKD', val)
        # Remove hidden characters if the option is selected
        if remove_hidden:
            # Remove non-printable characters
            val = re.sub(r'[^\x20-\x7E]', '', val)
        if chars_to_remove:
            val = re.sub(f"[{re.escape(chars_to_remove)}]", '', val)
    return val


def export_and_clean_file(
    uploaded_file: st.runtime.uploaded_file_manager.UploadedFile,
    changes: List[Dict[str, Any]],
    file_type: str
) -> Tuple[pd.DataFrame, pd.DataFrame, BytesIO, BytesIO]:
    """
    Handle file upload, cleaning, and prepare for download.

    Args:
        uploaded_file (st.runtime.uploaded_file_manager.UploadedFile): The uploaded file.
        changes (List[Dict[str, Any]]): A list of dictionaries containing cleaning rules.
        file_type (str): The type of the file ('csv' or 'xlsx').

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, BytesIO, BytesIO]: Original DataFrame, cleaned DataFrame,
        CSV buffer, and Excel buffer.
    """
    if file_type == 'csv':
        df = pd.read_csv(uploaded_file, dtype=str)  # Read everything as text
    else:
        df = pd.read_excel(uploaded_file, dtype=str)

    df_cleaned = clean_data(df, changes)

    # Create in-memory buffer for CSV and Excel files
    buffer_csv = BytesIO()
    buffer_excel = BytesIO()

    # Save to CSV in memory
    df_cleaned.to_csv(buffer_csv, index=False)
    buffer_csv.seek(0)

    # Save to Excel in memory
    with pd.ExcelWriter(buffer_excel, engine='xlsxwriter') as writer:
        df_cleaned.to_excel(writer, index=False)
    buffer_excel.seek(0)

    return df, df_cleaned, buffer_csv, buffer_excel


# Streamlit app
st.title('File Upload, Clean, and Download App')

# File upload
uploaded_file: Optional[st.runtime.uploaded_file_manager.UploadedFile] = st.file_uploader(
    'Upload your file (Excel or CSV)', type=['xlsx', 'csv']
)

# Manage user changes
if 'changes' not in st.session_state:
    # Store changes as a list of dictionaries
    st.session_state.changes: List[Dict[str, Any]] = []

if uploaded_file is not None:
    # Determine file type
    file_type: str = 'csv' if uploaded_file.name.endswith('.csv') else 'xlsx'

    st.write('File uploaded successfully!')

    # Load the data
    if file_type == 'csv':
        # Read CSV as text to preserve leading zeros
        df: pd.DataFrame = pd.read_csv(uploaded_file, dtype=str)
    else:
        # Read Excel as text to preserve leading zeros
        df = pd.read_excel(uploaded_file, dtype=str)

    st.subheader('Original Data')
    st.dataframe(df)

    # Column selection
    columns: List[str] = df.columns.tolist()
    selected_columns: List[str] = st.multiselect(
        'Select specific columns to clean (leave empty to clean all)', columns
    )

    # Input for characters or symbols to remove
    chars_to_remove: str = st.text_input(
        'Enter characters or symbols to remove (optional):', ''
    )

    # Checkbox to remove hidden characters
    remove_hidden: bool = st.checkbox(
        'Remove hidden (non-printable) characters', value=True
    )

    # Add change button
    if st.button('Add Change'):
        if chars_to_remove or remove_hidden:
            # Add the new change to the session state
            st.session_state.changes.append({
                'columns': selected_columns,
                'chars': chars_to_remove,
                'remove_hidden': remove_hidden,
                'description': f"Remove '{chars_to_remove}' from {', '.join(selected_columns) if selected_columns else 'all columns'}" + (' and hidden characters' if remove_hidden else '')
            })

    # Display all changes made so far
    if st.session_state.changes:
        st.subheader('Changes Made:')
        for i, change in enumerate(st.session_state.changes):
            # Checkbox to allow the user to select/unselect each change
            apply_change: bool = st.checkbox(
                change['description'], value=True, key=f'change_{i}'
            )
            change['apply'] = apply_change

    # Apply changes and clean file
    changes_to_apply: List[Dict[str, Any]] = [
        change for change in st.session_state.changes if change.get('apply')
    ]
    if changes_to_apply:
        df, df_cleaned, buffer_csv, buffer_excel = export_and_clean_file(
            uploaded_file, changes_to_apply, file_type
        )

        # Show cleaned data
        st.subheader('Cleaned Data')
        st.dataframe(df_cleaned)

        # File name editor
        default_file_name: str = os.path.splitext(
            uploaded_file.name
        )[0] + '_updated'
        file_name_input: str = st.text_input(
            'Edit file name for download:', default_file_name
        )

        # Ensure valid file names
        file_name_csv: str = file_name_input + '.csv'
        file_name_excel: str = file_name_input + '.xlsx'

        # Download buttons for cleaned files
        st.download_button(
            label='Download cleaned CSV',
            data=buffer_csv,
            file_name=file_name_csv,
            mime='text/csv'
        )

        st.download_button(
            label='Download cleaned Excel',
            data=buffer_excel,
            file_name=file_name_excel,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        st.info('No changes selected to apply.')
else:
    st.info('Please upload a CSV or Excel file to proceed.')

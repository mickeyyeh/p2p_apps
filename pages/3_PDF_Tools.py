import streamlit as st
from PyPDF2 import PdfReader, PdfWriter

import os
import io


def merge_pdfs(pdf_files):
    # Create a BytesIO object to hold the merged PDF bytes
    merged_pdf_bytes = io.BytesIO()

    merger = PdfWriter()

    try:
        for pdf_file in pdf_files:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                merger.add_page(page)

        # Write the merged PDF to the BytesIO object
        merger.write(merged_pdf_bytes)
        # Reset the BytesIO object's position to the beginning
        merged_pdf_bytes.seek(0)

        return merged_pdf_bytes.getvalue()  # Return the bytes from the BytesIO object

    except Exception as e:
        st.error(f"Error merging PDFs: {e}")
        return None


def split_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    try:
        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            writer = PdfWriter()
            writer.add_page(page)
            split_pdf_bytes = io.BytesIO()
            writer.write(split_pdf_bytes)
            split_pdf_bytes.seek(0)

            st.download_button(
                label=f"Download Page {page_number + 1}",
                data=split_pdf_bytes.getvalue(),
                file_name=f"page_{page_number + 1}.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"Error splitting PDF: {e}")


def main():
    st.title("PDF Tools")

    option = st.selectbox(
        "Select an action",
        ("Merge PDFs", "Split PDF"))

    if option == "Merge PDFs":
        uploaded_files = st.file_uploader(
            "Upload PDF files to merge", accept_multiple_files=True)

        if uploaded_files:
            if st.button("Merge PDFs"):
                merged_pdf_bytes = merge_pdfs(uploaded_files)
                if merged_pdf_bytes:
                    st.success("PDFs merged successfully!")

                    # Offer download link for the merged PDF file
                    st.download_button(
                        label="Download Merged PDF",
                        data=merged_pdf_bytes,
                        file_name="merged_pdf.pdf",
                        mime="application/pdf"
                    )

    elif option == "Split PDF":
        uploaded_file = st.file_uploader(
            "Upload PDF file to split", type="pdf")

        if uploaded_file:
            if st.button("Split PDF"):
                split_pdf(uploaded_file)


if __name__ == "__main__":
    main()

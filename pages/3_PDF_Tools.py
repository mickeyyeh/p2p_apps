import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image


def merge_pdfs(pdf_files):
    merged_pdf_bytes = io.BytesIO()
    merger = fitz.open()

    try:
        for pdf_file in pdf_files:
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            merger.insert_pdf(pdf_document)

        merger.save(merged_pdf_bytes)
        merged_pdf_bytes.seek(0)
        return merged_pdf_bytes.getvalue()

    except Exception as e:
        st.error(f"Error merging PDFs: {e}")
        return None


def split_pdf(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    num_pages = len(pdf_document)

    try:
        for page_number in range(num_pages):
            writer = fitz.open()
            writer.insert_pdf(
                pdf_document, from_page=page_number, to_page=page_number)
            split_pdf_bytes = io.BytesIO()
            writer.save(split_pdf_bytes)
            split_pdf_bytes.seek(0)

            st.download_button(
                label=f"Download Page {page_number + 1}",
                data=split_pdf_bytes.getvalue(),
                file_name=f"page_{page_number + 1}.pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"Error splitting PDF: {e}")


def preview_pdf_pages(pdf_file, sort_order):
    # Convert PDF to images for preview with higher DPI
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images = []
    dpi = 600  # Increased DPI for sharper image quality

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(
            dpi / 72, dpi / 72))  # Set DPI
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append((page_number + 1, img))

    # Sort pages based on user input
    if sort_order == "Ascending":
        images = sorted(images, key=lambda x: x[0])
    elif sort_order == "Descending":
        images = sorted(images, key=lambda x: x[0], reverse=True)
    elif sort_order == "Alphabetical":
        # Convert page number to string for alphabetical sorting
        images = sorted(images, key=lambda x: str(x[0]))

    # Display images and options for deletion and reordering
    page_selection = []
    used_positions = set()
    new_order = {}

    st.write("### Preview Pages (Select Pages to Delete and Set Order)")

    for page_number, img in images:
        col1, col2 = st.columns([1, 1])
        with col1:
            delete_key = f"delete_{page_number}"
            delete = st.checkbox(f"Delete Page {page_number}", key=f"{
                                 delete_key}_{pdf_file.name}")
            if delete:
                page_selection.append(page_number)
        with col2:
            reorder_key = f"reorder_{page_number}"
            new_idx = st.number_input(f"New Position for Page {page_number}",
                                      value=page_number, key=f"{reorder_key}_{pdf_file.name}")
            if new_idx in used_positions:
                st.warning(
                    f"Position {new_idx} is already used. Please choose a different position.")
            else:
                used_positions.add(new_idx)
                new_order[page_number] = new_idx

    # Filter out deleted pages and sort based on new order
    edited_pages = [page for page in images if page[0] not in page_selection]
    edited_pages = sorted(
        edited_pages, key=lambda x: new_order.get(x[0], x[0]))

    # Display the preview images
    preview_images = [img for _, img in edited_pages]
    return preview_images


def main():
    st.title("PDF Tools")

    option = st.selectbox(
        "Select an action",
        ("Merge PDFs", "Split PDF")
    )

    if option == "Merge PDFs":
        uploaded_files = st.file_uploader(
            "Upload PDF files to merge", accept_multiple_files=True, type="pdf"
        )

        if uploaded_files:
            # Add sort order selection
            sort_order = st.selectbox(
                "Sort Pages",
                ["Original Order", "Ascending", "Descending", "Alphabetical"]
            )

            # If "Original Order" is selected, keep files in the order they were uploaded
            if sort_order == "Original Order":
                sort_order = "Ascending"  # Default to ascending to maintain the original order

            all_images = []
            for uploaded_file in uploaded_files:
                st.write(f"### Preview and Edit: {uploaded_file.name}")
                preview_images = preview_pdf_pages(uploaded_file, sort_order)
                all_images.extend(preview_images)

            if all_images:
                st.write("### Final Preview")
                # Display images in a scrollable container
                for img in all_images:
                    st.image(img, use_column_width=True)

                if st.button("Merge PDFs"):
                    # Create temporary PDFs from the preview images
                    temp_files = []
                    for img in all_images:
                        temp_pdf = io.BytesIO()
                        img.save(temp_pdf, format='PDF')
                        temp_pdf.seek(0)
                        temp_files.append(temp_pdf)

                    merged_pdf_bytes = merge_pdfs(temp_files)
                    if merged_pdf_bytes:
                        st.success("PDFs merged successfully!")
                        st.download_button(
                            label="Download Merged PDF",
                            data=merged_pdf_bytes,
                            file_name="merged_pdf.pdf",
                            mime="application/pdf"
                        )

    elif option == "Split PDF":
        uploaded_file = st.file_uploader(
            "Upload PDF file to split", type="pdf"
        )

        if uploaded_file:
            if st.button("Split PDF"):
                split_pdf(uploaded_file)


if __name__ == "__main__":
    main()

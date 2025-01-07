import streamlit as st
from pypdf import PdfReader, PdfWriter, PageObject
from datetime import datetime  # To get the current date

# App title
st.title("PDF Letterhead Overlay Tool")
st.markdown("""
Upload your letterhead (single-page PDF) and report (multi-page PDF). 
The tool will overlay the letterhead on every page of the report.
""")

# Streamlit File Uploads
letterhead_file = st.file_uploader("Upload Letterhead PDF", type=["pdf"])
report_file = st.file_uploader("Upload Report PDF", type=["pdf"])

if letterhead_file and report_file:
    try:
        # Create PdfReader for the uploaded files
        letterhead_reader = PdfReader(letterhead_file)
        report_reader = PdfReader(report_file)

        # Get the letterhead page (single-page)
        letterhead_page = letterhead_reader.pages[0]

        # Create a PdfWriter for the output PDF
        output_pdf = PdfWriter()

        # Process each page of the report
        for report_page in report_reader.pages:
            # Create a new blank page with the same dimensions as the report page
            new_page = PageObject.create_blank_page(
                width=report_page.mediabox.width,
                height=report_page.mediabox.height
            )

            # Merge the letterhead with the new page
            new_page.merge_page(letterhead_page)

            # Merge the report page onto the new page with letterhead
            new_page.merge_page(report_page)

            # Add the new page to the output PDF
            output_pdf.add_page(new_page)

        # Save the final PDF to a BytesIO object for downloading
        from io import BytesIO
        output_pdf_stream = BytesIO()
        output_pdf.write(output_pdf_stream)
        output_pdf_stream.seek(0)

        # Get the current date in YYYY-MM-DD format
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Provide a download link for the final PDF with date in the file name
        st.download_button(
            label="Download Final PDF",
            data=output_pdf_stream,
            file_name=f"Qurocare_Lab_Report_{current_date}.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")



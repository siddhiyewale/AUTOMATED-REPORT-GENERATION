# Importing libraries
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

# Read CSV
def load_dataset(csv_path):
    return pd.read_csv(csv_path)

# DataFrame
def compute_summary(dataframe):
    return dataframe.describe(include='all')

# Formatting
def draw_table(pdf, dataframe, x_offset, y_offset, title):
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x_offset, y_offset + 15, title)

    pdf.setFont("Helvetica", 9)
    columns = dataframe.columns.tolist()
    row_height = 15
    col_width = 100

    # Draw headers
    for i, col in enumerate(columns):
        pdf.drawString(x_offset + i * col_width, y_offset, str(col))

    # Draw rows
    for row_num, row in dataframe.iterrows():
        y = y_offset - (row_num + 1) * row_height
        for col_num, item in enumerate(row):
            pdf.drawString(x_offset + col_num * col_width, y, str(item))

#Generate Report
def create_pdf_report(summary_data, file_name, original_data):
    pdf = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    # Title (centered)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawCentredString(width / 2, height - 55, "Summary Report")

    # Timestamp (centered)
    pdf.setFont("Helvetica", 9)
    timestamp = f"Created on: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
    pdf.drawCentredString(width / 2, height - 70, timestamp)

    
    draw_table(pdf, original_data, x_offset=55, y_offset=height - 100, title="Original Data:")

    pdf.showPage()  # Start a new page

    #  Header 
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(55, height - 60, "Statistical Overview:")

    # Table form
    summary_data = summary_data.transpose()
    summary_data.insert(0, 'Metric', summary_data.index)
    summary_data.reset_index(drop=True, inplace=True)

    # Draw table
    draw_table(pdf, summary_data, x_offset=55, y_offset=height - 80, title="")
    #save the PDF
    pdf.save()

# Main
if __name__ == "__main__":
    # File paths
    source_file = "data.csv"
    report_file = "generated_report.pdf"

    try:
        dataset = load_dataset(source_file)
        stats = compute_summary(dataset)
        create_pdf_report(stats, report_file, dataset)
        print("Report generated at:", report_file)
    except Exception as err:
        # If any errors
        print("Failed to generate report:", err)

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from reportlab.platypus import Image
import numpy as np


def generate_report_on_past_dates():
    pass

def generate_report(records_arr, selected_date, file_path):
    # Create the PDF document
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []

    # Add Intro
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']

    intro_title = Paragraph("Water Level Monitoring System Report", title_style)
    intro_date = Paragraph(f"for {selected_date}", subtitle_style)
    elements.append(intro_title)
    elements.append(intro_date)
    elements.append(Spacer(1, 20))

    # Add Overview
    overview_title = Paragraph("1. Overview", subtitle_style)
    elements.append(overview_title)
    elements.append(Spacer(1, 12))
    
    # Create the water level plot
    times = [datetime.datetime.strptime(f"{selected_date} {record[0]}", "%Y/%m/%d %H:%M:%S") for record in records_arr]
    levels = [float(record[1]) for record in records_arr]

    plt.figure(figsize=(10, 5))
    plt.plot(times, levels, marker='o', linestyle='-', color='b')
    plt.title('Water Level Throughout the Day')
    plt.xlabel('Time')
    plt.ylabel('Water Level')
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Show every hour
    plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(interval=30))  # Show every 30 minutes as minor ticks
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot to a file
    plot_filename = 'water_level_plot.png'
    plt.savefig(plot_filename, bbox_inches='tight')  # Ensure the plot is saved correctly
    plt.close()
    
    # Add plot image to PDF
    elements.append(Image(plot_filename, width=500, height=250))  # Adjust size as needed
    elements.append(Spacer(1, 12))

    # Calculate and add statistics
    avg_level = np.mean(levels)
    highest_level = max(levels)
    highest_time = times[levels.index(highest_level)].strftime('%H:%M:%S')
    lowest_level = min(levels)
    lowest_time = times[levels.index(lowest_level)].strftime('%H:%M:%S')

    stats_text = (f"Average: {avg_level:.2f} Waterlevel<br/>"
                  f"Highest: {highest_level:.2f} Waterlevel ({highest_time})<br/>"
                  f"Lowest: {lowest_level:.2f} Waterlevel ({lowest_time})")
    stats_paragraph = Paragraph(stats_text, normal_style)
    elements.append(stats_paragraph)
    elements.append(Spacer(1, 20))

    # Add Data Dump
    data_dump_title = Paragraph("2. Data dump", subtitle_style)
    elements.append(data_dump_title)
    elements.append(Spacer(1, 12))

    # Add table of records
    table_data = [['Time', 'Water Level']] + records_arr
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Add Contact Developers
    contact_title = Paragraph("3. Contact developers", subtitle_style)
    contact_info = Paragraph("lara.aspa@gmail.com", normal_style)
    elements.append(contact_title)
    elements.append(contact_info)
    
    # Build the PDF
    doc.build(elements)

if __name__ == '__main__':
    print("Hello world")
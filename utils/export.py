
import csv
from fpdf import FPDF
from database.models import init_db, Attendance
from utils.helpers import format_timestamp
import os

Session = init_db()

def export_attendance_csv(filepath="reports/attendance.csv"):
    session = Session()
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    records = session.query(Attendance).all()
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Timestamp', 'Status'])
        for record in records:
            writer.writerow([record.name, format_timestamp(record.timestamp), record.status])

def export_attendance_pdf(filepath="reports/attendance.pdf"):
    session = Session()
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    records = session.query(Attendance).all()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Attendance Report", ln=True, align='C')
    pdf.ln(10)

    for record in records:
        line = f"Name: {record.name}, Time: {format_timestamp(record.timestamp)}, Status: {record.status}"
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(filepath)

import pandas as pd
from datetime import datetime
import os

def export_attendance_csv():
    if os.path.exists('reports/attendance.csv'):
        df = pd.read_csv('reports/attendance.csv')
        today = datetime.now().strftime('%Y-%m-%d')
        output_path = f'reports/attendance_{today}.csv'
        df.to_csv(output_path, index=False)
    else:
        print("[WARN] No attendance file found to export.")

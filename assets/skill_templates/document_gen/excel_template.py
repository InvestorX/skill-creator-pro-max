import openpyxl
from pathlib import Path

def setup_template(output_path: str):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Generated Template"
    
    # Header
    headers = ["ID", "Name", "Date", "Value"]
    for col, h in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=h)
        
    wb.save(output_path)
    print(f"Created basic Excel template at {output_path}")

if __name__ == "__main__":
    setup_template("template.xlsx")

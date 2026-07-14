import os
from fpdf import FPDF

class PDFReport(FPDF):
    def __init__(self, title):
        super().__init__()
        self.report_title = title
        
    def header(self):
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, self.report_title, border=0, align='R')
        # Line break
        self.ln(10)
        
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f'Page {self.page_no()}', border=0, align='C')

def convert_md_to_pdf(md_path, pdf_path, report_title):
    pdf = PDFReport(report_title)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("helvetica", size=10)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    in_table = False
    table_headers = []
    in_code_block = False
    
    for line in lines:
        line_str = line.strip()
        # Sanitize text for Latin-1 compatibility (Helvetica core font)
        line_str = line_str.replace('🟢', '[Healthy]')
        line_str = line_str.replace('🟡', '[Stable]')
        line_str = line_str.replace('🔴', '[Critical]')
        line_str = line_str.replace('—', '-')
        line_str = line_str.replace('–', '-')
        line_str = line_str.replace('’', "'")
        line_str = line_str.replace('‘', "'")
        line_str = line_str.replace('“', '"')
        line_str = line_str.replace('”', '"')
        
        try:
            line_str.encode('latin-1')
        except UnicodeEncodeError:
            line_str = line_str.encode('latin-1', errors='replace').decode('latin-1')
            
        print(f"[{report_title}] Processing: {line_str}")
        
        # Check for code block fences
        if line_str.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                pdf.set_font('courier', size=8.5)
            else:
                pdf.set_font('helvetica', size=10)
            continue
            
        if in_code_block:
            clean_line = line.replace('—', '-').replace('🟢', '[Healthy]').replace('🟡', '[Stable]').replace('🔴', '[Critical]')
            clean_line = clean_line.encode('latin-1', errors='replace').decode('latin-1')
            pdf.multi_cell(0, 4, clean_line)
            pdf.set_x(10.0)
            continue
            
        # Skip empty lines if not in table
        if not line_str:
            if not in_table:
                pdf.ln(3)
            continue
            
        # Skip markdown table separation lines
        if in_table and '---' in line_str:
            continue
            
        # Check for headings
        if line_str.startswith('# '):
            pdf.ln(4)
            pdf.set_font('helvetica', 'B', 15)
            pdf.set_text_color(0, 168, 150)  # Teal accent
            pdf.multi_cell(0, 10, line_str[2:])
            pdf.set_x(10.0)
            pdf.set_font('helvetica', size=10)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
        elif line_str.startswith('## '):
            pdf.ln(3)
            pdf.set_font('helvetica', 'B', 12)
            pdf.set_text_color(30, 34, 41)   # Dark neutral
            pdf.multi_cell(0, 8, line_str[3:])
            pdf.set_x(10.0)
            pdf.set_font('helvetica', size=10)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)
        elif line_str.startswith('### '):
            pdf.ln(2)
            pdf.set_font('helvetica', 'B', 10)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(0, 6, line_str[4:])
            pdf.set_x(10.0)
            pdf.set_font('helvetica', size=10)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)
        # Check for tables
        elif line_str.startswith('|'):
            in_table = True
            cells = [c.strip() for c in line_str.split('|')[1:-1]]
            
            page_width = pdf.epw
            col_width = page_width / len(cells)
            
            # Print header cells
            if not table_headers:
                table_headers = cells
                pdf.set_font('helvetica', 'B', 8)
                pdf.set_fill_color(240, 240, 240)
                for cell in cells:
                    pdf.cell(col_width, 7, cell, border=1, align='C', fill=True)
                pdf.ln(7)
                pdf.set_font('helvetica', size=8)
            else:
                # Body cells
                for cell in cells:
                    if 'Critical' in cell or 'Late' in cell or 'Lost' in cell:
                        pdf.set_text_color(230, 50, 50)
                    elif 'Healthy' in cell or 'On-Time' in cell or 'Champions' in cell:
                        pdf.set_text_color(0, 150, 130)
                    else:
                        pdf.set_text_color(0, 0, 0)
                    pdf.cell(col_width, 7, cell, border=1, align='L')
                pdf.ln(7)
                pdf.set_text_color(0, 0, 0)
        else:
            if in_table:
                # Table has ended
                in_table = False
                table_headers = []
                pdf.ln(2)
            
            # Check if list item
            if line_str.startswith('- ') or line_str.startswith('* '):
                pdf.set_font('helvetica', size=9.5)
                # Output a simple bullet character representation
                pdf.write(5, "* ")
                pdf.multi_cell(0, 5, line_str[2:])
                pdf.set_x(10.0)
                pdf.set_font('helvetica', size=10)
            else:
                pdf.multi_cell(0, 5, line_str)
                pdf.set_x(10.0)
                
    pdf.output(pdf_path)

if __name__ == '__main__':
    reports_dir = 'reports'
    print("Converting Executive_Report...")
    convert_md_to_pdf(
        os.path.join(reports_dir, 'Executive_Report.md'),
        os.path.join(reports_dir, 'Executive_Report.pdf'),
        'Olist E-Commerce Executive Report'
    )
    print("Converting Data_Dictionary...")
    convert_md_to_pdf(
        os.path.join(reports_dir, 'Data_Dictionary.md'),
        os.path.join(reports_dir, 'Data_Dictionary.pdf'),
        'Olist E-Commerce Data Dictionary'
    )
    print("Converting Business_Insights...")
    convert_md_to_pdf(
        os.path.join(reports_dir, 'Business_Insights.md'),
        os.path.join(reports_dir, 'Business_Insights.pdf'),
        'Olist E-Commerce Detailed Business Insights'
    )
    print("Converting Dashboard_Guide...")
    convert_md_to_pdf(
        os.path.join(reports_dir, 'Dashboard_Guide.md'),
        os.path.join(reports_dir, 'Dashboard_Guide.pdf'),
        'Olist E-Commerce Dashboard Guide'
    )
    print("PDF Generation complete!")

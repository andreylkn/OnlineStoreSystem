from managers.base_manager import BaseManager
from prettytable import PrettyTable

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from services.database import QUANTITY, EFFECTIVE_PRICE, SALE_DATE
from utils.calculation_utils import calculate_total_item_price

TABLE_HEADERS = ["Sale ID", "User ID", "Product ID", "Quantity",
                 "Effective Price", "Sale Date", "Line Total"]

class SaleReportManager(BaseManager):
    def get_report(self):
        start_date = input("Enter start date (YYYY-MM-DD): ") + " 00:00:00"
        end_date = input("Enter end date (YYYY-MM-DD): ") + " 23:59:59"

        rows = self._get_report_data(start_date, end_date)

        if not rows:
            print("No sales records found for the specified period.")

        return start_date, end_date, rows

    def print_report(self):
        start_date, end_date, rows = self.get_report()
        if rows:
            total_sales = 0.0
            table = PrettyTable()
            table.field_names = TABLE_HEADERS
            for row in rows:
                line_total = calculate_total_item_price(row[QUANTITY], row[EFFECTIVE_PRICE])
                total_sales += line_total
                table.add_row([row["id"], row["user_id"], row["product_id"], row[QUANTITY],
                               row[EFFECTIVE_PRICE], row[SALE_DATE], f"{line_total:.2f}"])

            print("\n--------------------- Sales Report ---------------------")
            print(table)
            print(f"\nTotal Sales Amount: {total_sales:.2f}")
        else:
            print("No sales records found for the specified period.")

    def export_report(self):
        start_date, end_date, rows = self.get_report()

        pdf_file = f"sales_report_{start_date[:10]}_to_{end_date[:10]}.pdf"

        # Set up the document
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Add report title and period
        elements.append(Paragraph("Sales Report", styles['Title']))
        elements.append(Paragraph(f"Period: {start_date[:10]} to {end_date[:10]}", styles['Normal']))
        elements.append(Spacer(1, 12))

        elements.append(
            self._create_table(
                self._get_table_data(rows)
            )
        )

        # Build the PDF
        doc.build(elements)
        print(f"Sales report exported successfully to {pdf_file}")

    # Create and style the table
    def _create_table(self, data):
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        return table

    def _get_table_data(self, rows):
        data = [TABLE_HEADERS]
        total_sales = 0.0
        if rows:
            for row in rows:
                line_total = calculate_total_item_price(row[QUANTITY], row[EFFECTIVE_PRICE])
                total_sales += line_total
                data.append([
                    row['id'],
                    row['user_id'],
                    row['product_id'],
                    row[QUANTITY],
                    f"{row[EFFECTIVE_PRICE]:.2f}",
                    row[SALE_DATE],
                    f"{line_total:.2f}"
                ])
            # Append a summary row with the total sales amount
            data.append(["", "", "", "", "", "Total Sales", f"{total_sales:.2f}"])
        else:
            data.append(["No sales records found for the specified period."])
        return data

    def _get_report_data(self, start_date, end_date):
        cursor = self._db.connection.cursor()
        cursor.execute(
            "SELECT * FROM sales WHERE sale_date BETWEEN ? AND ?",
            (start_date, end_date)
        )
        return cursor.fetchall()

from fpdf import FPDF
import os
import pilot as pilot_obj
import club as club_obj
import datetime
import pilot_log


class Invoice:
    X = 10  # Left side of the PDF page.

    def __init__(self, pilot):
        self.pilot = pilot

    def draw_box(self, pdf_obj, x, y, w, h, line_width, text_lines):
        """
          x and y are the coordinates of the upper left of the box.
          w is box width (going to right). h is box height (going down)
          line_width is the line width as defined by set_line_width
          text_lines is an array of lines to put in the box: no scaling; be careful of overflow.
        """
        if line_width != 0:
            pdf_obj.set_line_width(line_width)
            pdf_obj.rect(x, y, w, h)
        row_count = 1
        for line in text_lines:
            starting_text_y_position = y + pdf_obj.font_size * row_count * 1.1
            pdf_obj.text(x + 1, starting_text_y_position, line)
            row_count += 1

    def draw_header_and_logo(self, pdf):
        pdf.set_font("helvetica", size=18, style='B')
        pdf.cell(280, 10, txt=self.pilot.club.club_name, ln=1, align="C")
        pdf.set_font("helvetica", size=10)
        pdf.cell(280, 5, txt=self.pilot.club.club_addr1, ln=1, align="C")
        pdf.cell(280, 5, txt=self.pilot.club.club_addr2, ln=1, align="C")
        csz = self.pilot.club.club_city + ", " + self.pilot.club.club_state + " " + self.pilot.club.club_zip
        pdf.cell(280, 5, txt=csz, ln=1, align="C")
        if os.path.exists('plane_icon.jpg'):
            pdf.image("plane_icon.jpg", x=123, w=50)

    def compute_statement_number(self):
        d = datetime.datetime.now()
        month = d.strftime("%m")
        year = d.strftime("%y")
        return month + year + self.pilot.id

    def compute_statement_date(self):
        d = datetime.datetime.now()
        return d.strftime("%x")

    def draw_statement_number_block(self, pdf):
        pdf.set_font("helvetica", size=10, style='B')
        self.draw_box(pdf, 20, 35, 22, pdf.font_size + 1.5, 0, ["Statement #:"])
        self.draw_box(pdf, 32.4, 40, 10, pdf.font_size + 1.5, 0, ["Date:"])
        self.draw_box(pdf, 19, 45, 23, pdf.font_size + 1.5, 0, ["Member ID# :"])
        pdf.set_font("helvetica", size=10)
        self.draw_box(pdf, 45, 35, 12, pdf.font_size + 1.5, 0, [self.compute_statement_number()])
        self.draw_box(pdf, 45, 40, 12, pdf.font_size + 1.5, 0, [self.compute_statement_date()])
        self.draw_box(pdf, 45, 45, 12, pdf.font_size + 1.5, 0, [self.pilot.id])

    def draw_bill_to_block(self, pdf):
        pdf.set_font("helvetica", size=10, style='B')
        self.draw_box(pdf, 195, 35, 22, pdf.font_size + 1.5, 0, ["Bill To:"])
        pdf.set_font("helvetica", size=10)
        self.draw_box(pdf, 210, 35, 12, pdf.font_size + 1.5, 0, [self.pilot.name])
        self.draw_box(pdf, 210, 40, 12, pdf.font_size + 1.5, 0, [self.pilot.addr1])
        csz = self.pilot.city + ", " + self.pilot.state + " " + self.pilot.zip
        self.draw_box(pdf, 210, 45, 12, pdf.font_size + 1.5, 0, [csz])
        self.draw_box(pdf, 210, 51.5, 12, pdf.font_size + 1.5, 0, [self.pilot.email])

    def draw_table_header(self, pdf):
        """
        Draws the table header row.
        :param pdf:
        :return: The y coordinate of the end of the header.
        """
        headers = [['Date'], ['Type'], ['Tach Out'], ['Tach In'], ['Hobbs', 'Out'], ['Hobbs', 'In'],
                   ['Rate Tach', 'Time $/hr'],
                   ['Total', 'Tach'], ['Total', 'Hobbs'], ['Balance Due', 'Tach Time'],
                   ['Gallons', 'of Fuel'], ['Price', 'per Gallon'], ['Fuel'], ['Misc.', 'Expenses']]
        pdf.set_font("helvetica", size=8, style='B')
        x = self.X
        y = 65
        cell_width = (pdf.w - 20) / 14
        row_height = 2 * (pdf.font_size + 1.5)
        for col in headers:
            self.draw_box(pdf, x, y, cell_width, row_height, .5, col)
            x += cell_width
        return y + row_height

    def draw_table_log_rows(self, pdf, y):
        log_entries = []
        for l in self.pilot.logs:
            log_entries.append(l.get_log_as_array())

        pdf.set_font("helvetica", size=8)
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        for row in log_entries:
            x = self.X
            for col in row:
                self.draw_box(pdf, x, y, cell_width, row_height, .25, col)
                x += cell_width
            y += row_height
        return y

    def draw_table_monthly_due_row(self, pdf, y):
        monthly_due = [[['07/05/19'], ['$50.00'], ]]
        pdf.set_font("helvetica", size=8)
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        self.draw_box(pdf, self.X, y, cell_width, row_height, .25, monthly_due[0][0])
        self.draw_box(pdf, self.X + cell_width, y, cell_width * 8, row_height, .25, ["Monthly Due"])
        self.draw_box(pdf, self.X + cell_width * 9, y, cell_width, row_height, .25, monthly_due[0][1])
        self.draw_box(pdf, self.X + cell_width * 10, y, cell_width * 4, row_height, .25, '')
        return y + row_height

    def draw_total_row(self, pdf, y):
        totals = {
            "total_tach": "1.79",
            "total_hobbs": "2.1",
            "balance": "$214.68",
            "gallons": "40.2",
            "fuel": "$173.26",
            "misc": "$0.00"
        }
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        pdf.set_font("helvetica", size=8, style='B')
        self.draw_box(pdf, self.X + cell_width * 6, y, cell_width, row_height, 0, ["Total:"])
        pdf.set_font("helvetica", size=8)
        self.draw_box(pdf, self.X + cell_width * 7, y, cell_width, row_height, 0.25, [totals["total_tach"]])
        self.draw_box(pdf, self.X + cell_width * 8, y, cell_width, row_height, 0.25, [totals["total_hobbs"]])
        self.draw_box(pdf, self.X + cell_width * 9, y, cell_width, row_height, 0.25, [totals["balance"]])
        self.draw_box(pdf, self.X + cell_width * 10, y, cell_width, row_height, 0.25, [totals["gallons"]])
        self.draw_box(pdf, self.X + cell_width * 11, y, cell_width, row_height, 0.25, [''])
        self.draw_box(pdf, self.X + cell_width * 12, y, cell_width, row_height, 0.25, [totals["fuel"]])
        self.draw_box(pdf, self.X + cell_width * 13, y, cell_width, row_height, 0.25, [totals["misc"]])
        return y + row_height

    def draw_subtotal_row(self, pdf, y):
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        pdf.set_font("helvetica", size=8, style='B')
        self.draw_box(pdf, self.X + cell_width * 12, y, cell_width, row_height, 0, ["Subtotal:"])
        pdf.set_font("helvetica", size=8)
        self.draw_box(pdf, self.X + cell_width * 13, y, cell_width, row_height, .25, ["$41.42"])
        return y + row_height

    def draw_previous_balance_row(self, pdf, y):
        pdf.set_font("helvetica", size=8)
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        self.draw_box(pdf, self.X, y, cell_width * 4, row_height, 0, ["Past Amount Due:"])
        self.draw_box(pdf, self.X + cell_width * 2, y, cell_width, row_height, .25, ["-$451.85"])
        pdf.set_font("helvetica", size=8, style='B')
        self.draw_box(pdf, self.X + cell_width * 11, y, cell_width * 2, row_height, 0, ["Previous Balance:"])
        pdf.set_font("helvetica", size=8)
        self.draw_box(pdf, self.X + cell_width * 13, y, cell_width, row_height, .25, ["-516.85"])
        return y + row_height

    def draw_current_balance_due_row(self, pdf, y):
        pdf.set_font("helvetica", size=8)
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        self.draw_box(pdf, self.X, y, cell_width * 4, row_height, 0, ["Amount Paid:"])
        self.draw_box(pdf, self.X + cell_width * 2, y, cell_width, row_height, .25, ["$65.00"])
        pdf.set_font("helvetica", size=8, style='B')
        self.draw_box(pdf, self.X + cell_width * 7, y, cell_width * 2, row_height, 0, ["Make Checks To:"])
        self.draw_box(pdf, self.X + cell_width * 11, y, cell_width * 2, row_height, 0, ["Current Balance Due:"])
        pdf.set_font("helvetica", size=8)
        self.draw_box(pdf, self.X + cell_width * 13, y, cell_width, row_height, .25, ["-475.43"])
        return y + row_height

    def draw_make_checks_to_row(self, pdf, y):
        pdf.set_font("helvetica", size=8)
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        self.draw_box(pdf, self.X, y, cell_width * 4, row_height, 0, ["Previous Balance:"])
        self.draw_box(pdf, self.X + cell_width * 2, y, cell_width, row_height, .25, ["-516.85"])
        self.draw_box(pdf, self.X + cell_width * 7, y, cell_width * 3, row_height, 0, [self.pilot.club.club_name])
        return y + row_height

    def draw_prev_bal_subtotal_row(self, pdf, y):
        pdf.set_font("helvetica", size=8)
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        self.draw_box(pdf, self.X, y, cell_width * 4, row_height, 0, ["Previous Bal Subtotal:"])
        self.draw_box(pdf, self.X + cell_width * 2, y, cell_width, row_height, .25, ["-516.85"])
        return y + row_height

    def draw_payment_received_row(self, pdf, y):
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        pdf.set_font("helvetica", size=8, style='B')
        self.draw_box(pdf, self.X + cell_width * 7, y, cell_width * 3, row_height, 0, ["Send Payment To:"])
        self.draw_box(pdf, self.X + cell_width * 10, y, cell_width * 2, row_height, 0, ["Payment Received:"])
        pdf.set_font("helvetica", size=8)
        self.draw_box(pdf, self.X + cell_width * 13, y, cell_width, row_height, .25, ["0.00"])
        return y + row_height

    def draw_please_include_row(self, pdf, y):
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        pdf.set_font("helvetica", size=8, style='B')
        self.draw_box(pdf, self.X, y, cell_width * 3, row_height, 0, ["Please Include Statement"])
        pdf.set_font("helvetica", size=8)
        self.draw_box(pdf, self.X + cell_width * 7, y, cell_width * 2, row_height, 0, [self.pilot.club.bill_name])
        return y + row_height

    def draw_balance_forward_row(self, pdf, y):
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        pdf.set_font("helvetica", size=8, style='B')
        self.draw_box(pdf, self.X, y, cell_width * 3, row_height, 0, ["Number On Your Check"])
        pdf.set_font("helvetica", size=8)
        self.draw_box(pdf, self.X + cell_width * 7, y, cell_width * 2, row_height, 0, [self.pilot.club.bill_addr1])
        pdf.set_font("helvetica", size=8, style='B')
        self.draw_box(pdf, self.X + cell_width * 10, y, cell_width * 2, row_height, 0, ["Balance Forward:"])
        pdf.set_font("helvetica", size=8)
        self.draw_box(pdf, self.X + cell_width * 13, y, cell_width, row_height, .25, ["-$475.43"])
        return y + row_height

    def draw_last_line(self, pdf, y):
        cell_width = (pdf.w - 20) / 14
        row_height = pdf.font_size + 1.5
        pdf.set_font("helvetica", size=8)
        self.draw_box(pdf, self.X, y, cell_width * 3, row_height, 0, ["Terms: Full Payment by End of Billing Month"])
        csz = self.pilot.club.bill_city + ", " + self.pilot.club.bill_state + " " + self.pilot.club.bill_zip
        self.draw_box(pdf, self.X + cell_width * 7, y, cell_width * 2, row_height, 0, [csz])
        return y + row_height

    def draw_table(self, pdf):
        y = self.draw_table_header(pdf)
        y = self.draw_table_log_rows(pdf, y)
        y = self.draw_table_monthly_due_row(pdf, y)
        y = self.draw_total_row(pdf, y)
        y = self.draw_subtotal_row(pdf, y)
        y = self.draw_previous_balance_row(pdf, y)
        y = self.draw_current_balance_due_row(pdf, y)
        y = self.draw_make_checks_to_row(pdf, y)
        y = self.draw_prev_bal_subtotal_row(pdf, y)
        y = self.draw_payment_received_row(pdf, y)
        y = self.draw_please_include_row(pdf, y)
        y = self.draw_balance_forward_row(pdf, y)
        self.draw_last_line(pdf, y)

    def create_pdf_filename(self, output_directory):
        filename = self.pilot.name.replace(" ", "_")
        filename = self.pilot.id + "-" + filename
        filename = output_directory + "/" + filename + ".pdf"
        return filename

    def build_invoice_for_pilot(self, output_directory):
        pdf = FPDF(orientation='L', format='letter')
        pdf.add_page()
        self.draw_header_and_logo(pdf)
        self.draw_statement_number_block(pdf)
        self.draw_bill_to_block(pdf)
        self.draw_table(pdf)
        pdf.output(self.create_pdf_filename(output_directory))


def main():
    pdf = FPDF(orientation='L', format='letter')
    pdf.add_page()

    pilot_data = pilot_obj.Pilot("1", "Joe Smith", "Joe", "1010 Clay Street", "", "Somecity", "MN", "55355",
                                 "someone@email.com",
                                 "100", "40")

    club = club_obj.Club("Flying Club Name", "club_addr1", "club_addr2", "club city", "MN", "55555", "Club Bill Name",
                         "bill addr1", "bill_addr2", "Bill City", "WI", "66666")
    pilot_data.club = club

    a_log = pilot_log.Log("6/13/19", "Joe", "29265", "92.36", "90.57", "1.79", "116.9", "114.8", "2.1", "25.13", "4.31",
                          "108.31", "")
    log_entries = [a_log]

    pilot_data.logs = log_entries

    invoice = Invoice(pilot_data)
    invoice.build_invoice_for_pilot("output")


if __name__ == "__main__":
    main()

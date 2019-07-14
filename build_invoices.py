from fpdf import FPDF
import os

def draw_box(pdf_obj, x, y, w, h, line_width, text_lines):
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


def draw_header_and_logo(pdf):
    pdf.set_font("helvetica", size=18, style='B')
    pdf.cell(280, 10, txt="Litchfield Flying Club", ln=1, align="C")
    pdf.set_font("helvetica", size=10)
    pdf.cell(280, 5, txt="Litchfield Municipal Airport", ln=1, align="C")
    pdf.cell(280, 5, txt="23980 628th Avenue", ln=1, align="C")
    pdf.cell(280, 5, txt="Litchfield, MN 55355", ln=1, align="C")
    if os.path.exists('plane_icon.jpg'):
        pdf.image("plane_icon.jpg", x=123, w=50)


def draw_statement_number_block(pdf):
    pdf.set_font("helvetica", size=10, style='B')
    draw_box(pdf, 20, 35, 22, pdf.font_size + 1.5, 0, ["Statement #:"])
    draw_box(pdf, 32.4, 40, 10, pdf.font_size + 1.5, 0, ["Date:"])
    draw_box(pdf, 19, 45, 23, pdf.font_size + 1.5, 0, ["Member ID# :"])
    pdf.set_font("helvetica", size=10)
    draw_box(pdf, 45, 35, 12, pdf.font_size + 1.5, 0, ["71936"])
    draw_box(pdf, 45, 40, 12, pdf.font_size + 1.5, 0, ["07/05/19"])
    draw_box(pdf, 45, 45, 12, pdf.font_size + 1.5, 0, ["36"])


def draw_bill_to_block(pdf):
    pdf.set_font("helvetica", size=10, style='B')
    draw_box(pdf, 195, 35, 22, pdf.font_size + 1.5, 0, ["Bill To:"])
    pdf.set_font("helvetica", size=10)
    draw_box(pdf, 210, 35, 12, pdf.font_size + 1.5, 0, ["Mr. Joe Eltgroth"])
    draw_box(pdf, 210, 40, 12, pdf.font_size + 1.5, 0, ["3100 Jefferson Street"])
    draw_box(pdf, 210, 45, 12, pdf.font_size + 1.5, 0, ["Hutchinson, MN 55350"])
    draw_box(pdf, 210, 51.5, 12, pdf.font_size + 1.5, 0, ["the.pilots.email@gmail.com"])


def draw_table_header(pdf):
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
    x = 10
    y = 65
    cell_width = (pdf.w - 20) / 14
    row_height = 2 * (pdf.font_size + 1.5)
    for col in headers:
        draw_box(pdf, x, y, cell_width, row_height, .5, col)
        x += cell_width
    return y + row_height


def draw_table_log_rows(pdf, y):
    log_entries = [
        [['6/13/19'], ['265'], ['90.57'], ['92.36'], ['114.8'], ['116.9'], ['92'], ['1.79'], ['2.1'], ['$164.68'],
         ['25.13'], ['4.31'],
         ['$108.31'], ['']],
        [['6/13/19'], ['265'], [''], [''], [''], [''], ['92'], ['0'], ['0'], ['$0.00'], ['15.07'], ['4.31'],
         ['$64.95'], ['']],
        [[''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], [''], ['']],
    ]
    pdf.set_font("helvetica", size=8)
    cell_width = (pdf.w - 20) / 14
    row_height = pdf.font_size + 1.5
    for row in log_entries:
        x = 10
        for col in row:
            draw_box(pdf, x, y, cell_width, row_height, .25, col)
            x += cell_width
        y += row_height
    return y


def draw_table_monthly_due_row(pdf, y):
    monthly_due = [[['07/05/19'], ['$50.00'], ]]
    pdf.set_font("helvetica", size=8)
    cell_width = (pdf.w - 20) / 14
    row_height = pdf.font_size + 1.5
    x = 10
    draw_box(pdf, x, y, cell_width, row_height, .25, monthly_due[0][0])
    draw_box(pdf, x + cell_width, y, cell_width * 8, row_height, .25, ["Monthly Due"])
    draw_box(pdf, x + cell_width * 9, y, cell_width, row_height, .25, monthly_due[0][1])
    draw_box(pdf, x + cell_width * 10, y, cell_width * 4, row_height, .25, '')

    # for row in log_entries:
    #     y += row_height
    #     x = 10
    #     for col in row:
    #         draw_box(pdf, x, y, cell_width, row_height, .25, col)
    #         x += cell_width
    return y + row_height

def draw_table(pdf):
    y = draw_table_header(pdf)
    y = draw_table_log_rows(pdf, y)
    draw_table_monthly_due_row(pdf, y)


def main():
    pdf = FPDF(orientation='L', format='letter')
    pdf.add_page()
    draw_header_and_logo(pdf)
    draw_statement_number_block(pdf)
    draw_bill_to_block(pdf)
    draw_table(pdf)
    pdf.output("18-Eltgroth.pdf")


if __name__ == "__main__":
    main()

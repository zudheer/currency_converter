import io

import xlsxwriter


def generate_sub_category_excel(headers, converted_data):
    """Generate excel sheet converted."""
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    center_format = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter'})

    header_format = workbook.add_format({
        'align': 'center', 'bold': True})
    worksheet = workbook.add_worksheet("converted_rates")
    row = 0
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    row += 1
    for row_index, row_val in enumerate(converted_data):
        for col, header in enumerate(headers):
            val = row_val.get(header, "")
            worksheet.write(row + row_index, col, val, center_format)
    worksheet.set_column(0, len(headers), 20)
    workbook.close()

    # Rewind the buffer.
    output.seek(0)
    return output

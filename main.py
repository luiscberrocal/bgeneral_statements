import json
from datetime import datetime

from openpyxl import load_workbook, Workbook


def parse_statement(filename, **kwargs):
    first_data_row = kwargs.get('first_data_row', 9)
    sheet_name = kwargs.get('sheet_name', 'BGPMainScreen')
    # Cuenta	Tarjeta  	Fecha transacción	Fecha proceso	Descripción
    # Referencia	Categoría	Cargos (Db)	Pagos (Cr)

    mappings = {
        'account': {'name': 'Cuenta', 'col': 1},
        'card': {'name': 'Tarjeta', 'col': 2},
        'transaction_date': {'name': 'Fecha transacción', 'col': 3},
        'process_date': {'name': 'Fecha proceso', 'col': 4},
        'description': {'name': 'Descripcion', 'col': 5},
        'reference': {'name': 'Referencia', 'col': 8},
        'category': {'name': 'Categoría', 'col': 9},
        'charges': {'name': 'Cargos', 'col': 10},
        'payments': {'name': 'Pagos', 'col': 11},
    }

    wb = load_workbook(filename=filename, data_only=True)
    sheet = wb[sheet_name]
    row_num = 1
    row_data_list = list()
    row_dict = dict()
    for row in sheet.rows:
        row_dict = dict()
        if row_num >= first_data_row:
            try:
                charges = row[mappings['charges']['col']].value

                for attribute_name in mappings.keys():
                    row_dict[attribute_name] = mappings[attribute_name]
                    row_dict[attribute_name]['value'] = row[mappings[attribute_name]['col']].value
                    row_dict[attribute_name]['row_num'] = row_num
                    row_dict[attribute_name]['source_file'] = filename
                print(f'{row_num}. {charges} {row_dict["charges"]["value"]} {type(charges)}')
                row_data_list.append(row_dict)
            except Exception as e:
                raise e
        if row_num >= first_data_row:
            print(f'{row_num}.  {row_data_list[row_num - first_data_row]["charges"]["value"]}')
        print('-' * 60)
        row_num += 1
    print('86-' * 60)
    row_num = 86
    print(f'{row_num}.  {row_data_list[row_num - first_data_row]["charges"]["value"]}')
    return row_data_list


def write_to_excel(filename, data_list, **kwargs):
    wb = Workbook()
    sheet = wb.create_sheet()
    row = 1
    col = 1
    for attribute_name in data_list[0].keys():
        sheet.cell(row=row, column=col, value=data_list[0][attribute_name]['name'])
        col += 1
    row += 1
    for data_dict in data_list:
        col = 1
        for attribute_name in data_dict.keys():
            sheet.cell(row=row, column=col, value=data_dict[attribute_name]['value'])
            col += 1
        row += 1

    wb.save(filename)


if __name__ == '__main__':
    export_json = True
    filename = './data/ESTADO-DE-CUENTA-TARJETA-DE-CREDITO-2021-02-27.xlsx'
    row_list = parse_statement(filename)

    # print(row_list)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if export_json:
        json_output_file = f'./output/{timestamp}_estado_cuenta.json'
        with open(json_output_file, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(row_list))
    excel_output_file = f'./output/{timestamp}_estado_cuenta.xlsx'
    write_to_excel(excel_output_file, row_list)

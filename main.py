import json
from datetime import datetime

from openpyxl import load_workbook


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
    row_list = list()
    for row in sheet.rows:
        if row_num >= first_data_row:
            try:
                # charges = row[mappings['charges']['col']].value
                # print(f'{row_num}. {charges} {type(charges)}')
                row_dict = dict()
                for column_name in mappings.keys():
                    row_dict[column_name] = mappings[column_name]
                    row_dict[column_name]['value'] = row[mappings['charges']['col']].value
                    row_dict[column_name]['source_file'] = filename
                row_list.append(row_dict)

            except Exception as e:
                raise e
        row_num += 1

    return row_list


if __name__ == '__main__':
    filename = './data/ESTADO-DE-CUENTA-TARJETA-DE-CREDITO-2021-02-27.xlsx'
    row_list = parse_statement(filename)

    print(row_list)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_output_file = f'./output/{timestamp}_estado_cuenta.json'
    with open(json_output_file, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(row_list))

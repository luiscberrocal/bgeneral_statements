import json
import os

from config import base_settings

if __name__ == '__main__':
    main_path = base_settings.ROOT_DIR
    config_path = base_settings.ROOT_DIR / 'config'
    print(f'Path: {main_path}')
    print(f'Config Path: {config_path}')
    mappings = {
        'account': {'name': 'Cuenta', 'col': 1},
        'card': {'name': 'Tarjeta', 'col': 2},
        'transaction_date': {'name': 'Fecha transacción', 'col': 3},
        'process_date': {'name': 'Fecha proceso', 'col': 4},
        'description': {'name': 'Descripción', 'col': 5},
        'reference': {'name': 'Referencia', 'col': 8},
        'category': {'name': 'Categoría', 'col': 9},
        'charges': {'name': 'Cargos (Db)', 'col': 10},
        'payments': {'name': 'Pagos (Cr)', 'col': 11},
    }
    config_filename = os.path.join(config_path, 'credit_card_config.json')
    configuration = dict()
    configuration['mappings'] = mappings
    configuration['start_row'] = 9
    with open(config_filename, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(configuration))
    print(f'Wrote config file {config_filename}')


import json
import os

from config import base_settings


def set_configuration(filename, config_dict, **kwargs):
    over_write = kwargs.get('over_write', False)

    config_path = base_settings.ROOT_DIR / 'config'
    config_filename = os.path.join(config_path, filename)
    if (os.path.exists(config_filename) and over_write) or not (os.path.exists(config_filename)):
        with open(config_filename, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(config_dict))
        return config_filename
    else:
        return None


def get_configuration(filename):
    config_path = base_settings.ROOT_DIR / 'config'
    config_filename = os.path.join(config_path, filename)
    if not os.path.exists(config_filename):
        msg = f'Configuration file {config_filename} not found'
        raise Exception(msg)
    with open(config_filename, 'r') as json_file:
        config = json.load(json_file)
    return config


def is_credit_card_excel(filename, **kwargs):
    pass


if __name__ == '__main__':
    # main_path = base_settings.ROOT_DIR
    # config_path = base_settings.ROOT_DIR / 'config'
    # print(f'Path: {main_path}')
    # print(f'Config Path: {config_path}')
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
    configuration = dict()
    configuration['mappings'] = mappings
    configuration['start_row'] = 9
    config_filename = set_configuration('credit_card_config.json', configuration)
    if config_filename is not None:
        print(f'Wrote config file {config_filename}')
    else:
        print('File already exists. Run with over_write parameter')

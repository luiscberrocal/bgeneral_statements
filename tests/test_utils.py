import os

from utils import get_configuration, set_configuration


def test_get_configuration():
    config = get_configuration('credit_card_config.json')
    assert len(config['mappings']) == 9
    assert config['start_row'] == 9


def test_set_configuration():
    config = {'mappings': {'silly': 1, 'name': 'attr'}, 'start_row': 3}

    filename = set_configuration('credit_card_config_TEST.json', config)
    assert os.path.exists(filename) is True
    os.remove(filename)
    assert os.path.exists(filename) is False

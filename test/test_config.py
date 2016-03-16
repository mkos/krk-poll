import wios
import unittest
import mock


class TestConfig(unittest.TestCase):

    def run_config(self, return_value):
        wios.xml_http_request = mock.MagicMock(return_value=return_value)
        return wios.Config('someurl')

    def test_update_no_config_key(self):
        with self.assertRaises(wios.ResponseError):
            self.run_config({})

    def test_get_raw_config_sunny_day(self):
        config = self.run_config({'config': {}})
        self.assertEqual({}, config.get_raw_config(), 'Config should be empty')

    def test_get_raw_stations(self):
        config = self.run_config({'config': {'stations': []}})
        self.assertEqual([], config.get_raw_stations(), 'Config should be empty')

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

    def test_get_raw_stations_no_stations_key(self):
        config = self.run_config({'config': {}})
        with self.assertRaises(wios.ResponseError):
            config.get_raw_stations()

    def test_get_raw_stations_sunny_day(self):
        config = self.run_config({'config': {'stations': []}})
        self.assertEqual([], config.get_raw_stations(), 'Config should be empty')

    def test_get_raw_channels_no_channels_key(self):
        config = self.run_config({'config': {}})
        with self.assertRaises(wios.ResponseError):
            config.get_raw_channels()

    def test_get_raw_channels_sunny_day(self):
        config = self.run_config({'config': {'channels': []}})
        self.assertEqual([], config.get_raw_channels(), 'Config should be empty')

    def test_get_raw_params_no_params_key(self):
        config = self.run_config({'config': {}})
        with self.assertRaises(wios.ResponseError):
            config.get_raw_params()

    def test_get_raw_params_sunny_day(self):
        config = self.run_config({'config': {'params': []}})
        self.assertEqual([], config.get_raw_params(), 'Config should be empty')

    def test_get_raw_thresholds_no_thresholds_key(self):
        config = self.run_config({'config': {}})
        with self.assertRaises(wios.ResponseError):
            config.get_raw_thresholds()

    def test_get_raw_thresholds_sunny_day(self):
        config = self.run_config({'config': {'thresholds': []}})
        self.assertEqual([], config.get_raw_thresholds(), 'Config should be empty')
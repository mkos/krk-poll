import wios
import unittest
import mock


class TestConfig(unittest.TestCase):
    def setUp(self):

        wios.xml_http_request = mock.MagicMock(return_value={'config': {}})
        self.config = wios.Config('someurl')

    def test_config_get_raw_config(self):
        self.assertEqual({}, self.config.get_raw_config())

import unittest

import cm.lib.environ


class EnvironmentParsingTestCase(unittest.TestCase):

    def test_parse_list_from_scalar_returns_all_keys(self):
        env = {
            'foo': 'bar:baz:taz'
        }
        result = cm.lib.environ.parselist(env, 'foo')
        self.assertEqual(len(result), 3)

    def test_parse_list_from_scalar_returns_all_keys_by_custom_sep(self):
        env = {
            'foo': 'bar:baz;taz'
        }
        result = cm.lib.environ.parselist(env, 'foo', sep=';')
        self.assertEqual(len(result), 2)

    def test_parse_list_from_scalar_returns_custom_type(self):
        env = {
            'foo': 'bar:baz:taz'
        }
        result = cm.lib.environ.parselist(env, 'foo', cls=list)
        self.assertTrue(isinstance(result, list))

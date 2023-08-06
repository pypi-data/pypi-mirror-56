import os

import yaml
from yaml.parser import ParserError
import tempfile
import unittest

from dnry.config import ConfigFactory
from dnry.config.yaml import YamlSource


def make_config_with_temp(data: dict):
    _, file = tempfile.mkstemp()
    try:
        with open(file, 'w') as fd:
            yaml.dump(data, stream=fd, Dumper=yaml.SafeDumper)
        factory = ConfigFactory()
        factory.add_source(YamlSource(file))
        return factory.build()
    finally:
        os.unlink(file)


class TestYamlSource(unittest.TestCase):

    def test_single_key(self):
        conf = make_config_with_temp({"a": 1})
        val = conf.get("a")
        self.assertEqual(1, val)

    def test_deep_keys(self):
        conf = make_config_with_temp({"a": 1, "b": {"c": 2}})
        val = conf.get("b:c")
        self.assertEqual(2, val)

    def test_bad_yaml(self):
        _, file = tempfile.mkstemp()
        throw_error = False
        try:
            with open(file, 'w') as fd:
                fd.write(':')
            factory = ConfigFactory()
            factory.add_source(YamlSource(file))
            conf = factory.build()
        except ParserError:
            throw_error = True
        finally:
            os.unlink(file)

        self.assertTrue(throw_error)


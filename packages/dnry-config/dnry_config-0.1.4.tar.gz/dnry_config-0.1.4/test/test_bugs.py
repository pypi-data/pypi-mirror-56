import os
import unittest
from uuid import uuid4

from dnry.config import ConfigFactory
from dnry.config.yaml import YamlSource


class TestBugs(unittest.TestCase):

    def test_empty_yaml_file(self):
        temp_file = f"./{uuid4()}.yaml"
        with open(temp_file, 'w') as fd:
            fd.write('\n')
        try:
            fact = ConfigFactory()
            fact.add_source(YamlSource(temp_file))
            conf = fact.build()
            none_val = conf.get("no:key")
            self.assertIsNone(none_val)

        finally:
            os.remove(temp_file)

    def test_optional_flag(self):
        fact = ConfigFactory()
        fact.add_source(YamlSource(f"./{uuid4()}", required=False))
        conf = fact.build()
        none_val = conf.get("no:key")
        self.assertIsNone(none_val)

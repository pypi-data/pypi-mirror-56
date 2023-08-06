import unittest

from dnry.config import ConfigFactory
from dnry.config.in_memory import InMemorySource


class TestFactory(unittest.TestCase):
    def test_single_key(self):
        fact = ConfigFactory()
        fact.add_source(InMemorySource({"a": 1}))
        conf = fact.build()
        val = conf.get("a")
        self.assertEqual(1, val)

    def test_multi_key(self):
        fact = ConfigFactory()
        fact.add_source(InMemorySource({"a": 1, "b": 2}))
        conf = fact.build()
        val = conf.get("a")
        self.assertEqual(1, val)

    def test_merge(self):
        fact = ConfigFactory()
        fact.add_source(InMemorySource({"a": 1}))
        fact.add_source(InMemorySource({"b": 2}))
        conf = fact.build()
        self.assertEqual(1, conf.get("a"))
        self.assertEqual(2, conf.get("b"))

    def test_merge_duplicate_key(self):
        fact = ConfigFactory()
        fact.add_source(InMemorySource({"a": 1}))
        fact.add_source(InMemorySource({"a": 2}))
        conf = fact.build()
        self.assertEqual(2, conf.get("a"))

    def test_merge_deep1(self):
        fact = ConfigFactory()
        fact.add_source(InMemorySource({"a": {"b": 1}}))
        fact.add_source(InMemorySource({"a": {"c": 2}}))
        conf = fact.build()
        self.assertEqual(1, conf.get("a:b"))
        self.assertEqual(2, conf.get("a:c"))

    def test_merge_deep2(self):
        fact = ConfigFactory()
        fact.add_source(InMemorySource({"a": {"b": 1, "c": 3}}))
        fact.add_source(InMemorySource({"a": {"c": 2}}))
        conf = fact.build()
        self.assertEqual(1, conf.get("a:b"))
        self.assertEqual(2, conf.get("a:c"))

    def test_merge_deep3(self):
        fact = ConfigFactory()
        fact.add_source(InMemorySource({"a": {"b": [1], "c": 3}}))
        fact.add_source(InMemorySource({"a": {"c": 2, "b": [2]}}))
        conf = fact.build()
        self.assertEqual(1, conf.get("a:b")[0])
        self.assertEqual(2, conf.get("a:b")[1])

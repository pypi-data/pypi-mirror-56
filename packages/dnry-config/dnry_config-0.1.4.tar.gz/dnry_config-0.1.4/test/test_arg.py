import unittest
from argparse import ArgumentParser

from dnry.config.arg import ArgumentSource
from dnry.config import ConfigFactory


class TestArgSource(unittest.TestCase):
    def test_single_key(self):
        ap = ArgumentParser()
        ap.add_argument('-f', '--foo')
        fact = ConfigFactory()
        fact.add_source(ArgumentSource(ap, ["--foo", "bar"]))
        conf = fact.build()
        self.assertEqual("bar", conf.get("foo"))

    def test_single_key(self):
        ap = ArgumentParser()
        ap.add_argument('-f', '--foo')
        fact = ConfigFactory()
        fact.add_source(ArgumentSource(ap, ["--foo", "baz"]))
        conf = fact.build()
        self.assertEqual("baz", conf.get("foo"))

    def test_nested_key(self):
        ap = ArgumentParser()
        ap.add_argument('-f', '--foo:bar')
        fact = ConfigFactory()
        fact.add_source(ArgumentSource(ap, ["--foo:bar", "baz"]))
        conf = fact.build()
        self.assertEqual("baz", conf.get("foo:bar"))

    def test_many_nested_keys(self):
        ap = ArgumentParser()
        ap.add_argument('--foo:bar')
        ap.add_argument('--bar')
        ap.add_argument('--foo:baz')
        fact = ConfigFactory()
        fact.add_source(ArgumentSource(ap, ["--foo:bar", "a", "--bar", "b", "--foo:baz", "c"]))
        conf = fact.build()
        self.assertEqual("a", conf.get("foo:bar"))
        self.assertEqual("b", conf.get("bar"))
        self.assertEqual("c", conf.get("foo:baz"))

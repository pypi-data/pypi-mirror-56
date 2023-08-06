#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from taz.keyvault import KeyVault
import tests.config as cfg
import sys


class KeyvaultTests(unittest.TestCase):

    def setUp(self):
        self.keyvault = KeyVault(cfg.keyvault['name'])

    def test_exists(self):
        self.assertTrue(self.keyvault is not None)

    def test_secret(self):
        secret = self.keyvault.get_secret(cfg.keyvault['secret_name'], '')
        self.assertTrue(secret is not None)


if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()

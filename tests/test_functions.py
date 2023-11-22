from math import gcd

from unittest import TestCase

class TestFunctions(TestCase):
    
    def test_pgcd(self):
        self.assertEqual(31, gcd(40902, 24140))


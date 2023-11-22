from math import gcd

from unittest import TestCase

class TestFunctions(TestCase):
    
    def test_pgcd(self):
        self.assertEqual(34, gcd(40902, 24140))

    def test_pgcd2(self):
        self.assertEqual(1, gcd(1, 97))    

    def test_pgcd3(self):
        self.assertEqual(12, gcd(36, 120))

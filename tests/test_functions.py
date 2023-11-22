from math2.functions import pgcd

from unittest import TestCase

class TestFunctions(TestCase):
    
    def test_pgcd(self):
        self.assertEqual(34, pgcd(40902, 24140))


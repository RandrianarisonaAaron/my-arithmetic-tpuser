from math import gcd

from unittest import TestCase

class TestFunctions(TestCase):
    
    def test_pgcd(self):
        """Summary line.
        test pgcd entre les nombre 40902 et 24140
        """
        self.assertEqual(34, gcd(40902, 24140))

    def test_pgcd2(self):
        """Summary line.
        test pgcd entre les nombre 40902 et 24140
        """        self.assertEqual(1, gcd(1, 97))    

    def test_pgcd3(self):
        """Summary line.
        test pgcd entre les nombre 40902 et 24140
        """
        self.assertEqual(12, gcd(36, 120))

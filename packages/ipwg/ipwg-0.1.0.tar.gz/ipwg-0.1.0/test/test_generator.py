import unittest
import string

from ipwg import Generator


class TestGenerator(unittest.TestCase):

    def test_includes_lowers(self):
        g = Generator()
        g.lowers_enabled = True
        p = g.create_password(1)
        self.assertTrue(p in string.ascii_lowercase)

    def test_includes_uppers(self):
        g = Generator()
        g.uppers_enabled = True
        p = g.create_password(1)
        self.assertTrue(p in string.ascii_uppercase)

    def test_includes_digits(self):
        g = Generator()
        g.digits_enabled = True
        p = g.create_password(1)
        self.assertTrue(p in string.digits)

    def test_includes_specials(self):
        g = Generator()
        g.specials_enabled = True
        p = g.create_password(1)
        self.assertTrue(p in string.punctuation)

    def test_produces_correct_length(self):
        g = Generator()
        g.specials_enabled = True
        p = g.create_password(10)
        self.assertEqual(10, len(p))

    def test_produces_one_of_each(self):
        g = Generator()
        g.lowers_enabled = True
        g.uppers_enabled = True
        g.digits_enabled = True
        g.specials_enabled = True
        g.specials_count = 1
        g.digits_count = 1
        g.uppers_count = 1
        g.lowers_count = 1
        p = g.create_password(4)
        self.assertEqual(1, len([_ for _ in p if _ in Generator.lowers]))
        self.assertEqual(1, len([_ for _ in p if _ in Generator.uppers]))
        self.assertEqual(1, len([_ for _ in p if _ in Generator.digits]))
        self.assertEqual(1, len([_ for _ in p if _ in Generator.specials]))

    def test_at_least_one_upper(self):
        g = Generator()
        g.specials_enabled = True
        g.digits_enabled = True
        g.uppers_enabled = True
        g.lowers_enabled = True
        g.uppers_count = 1
        p = g.create_password(10)
        self.assertTrue(len([_ for _ in p if _ in Generator.uppers]) > 0)

    def test_at_least_one_lower(self):
        g = Generator()
        g.specials_enabled = True
        g.digits_enabled = True
        g.uppers_enabled = True
        g.lowers_enabled = True
        g.lowers_count = 1
        p = g.create_password(10)
        self.assertTrue(len([_ for _ in p if _ in Generator.lowers]) > 0)

    def test_at_least_one_digit(self):
        g = Generator()
        g.specials_enabled = True
        g.digits_enabled = True
        g.uppers_enabled = True
        g.lowers_enabled = True
        g.digits_count = 1
        p = g.create_password(10)
        self.assertTrue(len([_ for _ in p if _ in Generator.digits]) > 0)

    def test_at_least_one_special(self):
        g = Generator()
        g.specials_enabled = True
        g.digits_enabled = True
        g.uppers_enabled = True
        g.lowers_enabled = True
        g.specials_count = 1
        p = g.create_password(10)
        self.assertTrue(len([_ for _ in p if _ in Generator.specials]) > 0)

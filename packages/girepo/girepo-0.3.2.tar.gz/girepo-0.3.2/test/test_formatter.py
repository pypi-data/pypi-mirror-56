from unittest import TestCase

from girepo.formatter import beautify_text


class TestFormatter(TestCase):

    def test_beautify_text(self):
        test_data = [
            ("Hello World", "|", "Hello World"),
            ("Hello | World", "|", "Hello \| World"),
            ("Hello $ World", "$", "Hello \$ World"),
            ("Hello | World", "$", "Hello | World")
        ]

        for target, separator, expected in test_data:
            with self.subTest():
                actual = beautify_text(target, separator)
                self.assertEqual(expected, actual)

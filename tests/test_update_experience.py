import unittest
from datetime import date

from scripts.update_experience import tenure, update


class ExperienceTests(unittest.TestCase):
    def test_elapsed_months_and_plural(self):
        self.assertEqual(tenure(date(2021, 8, 1)), "0 meses")
        self.assertEqual(tenure(date(2021, 9, 1)), "1 mês")
        self.assertEqual(tenure(date(2022, 8, 1)), "1 ano")
        self.assertEqual(tenure(date(2026, 10, 31)), "5 anos 2 meses")

    def test_future_start_fails(self):
        with self.assertRaises(ValueError):
            tenure(date(2021, 7, 31))

    def test_update_only_matching_line(self):
        source = "[ UPPER / BIPPER ]  4 anos 10 meses\nother text"
        expected = "[ UPPER / BIPPER ]  5 anos 2 meses\nother text"
        self.assertEqual(update(source, date(2026, 10, 31)), expected)
        self.assertEqual(update(expected, date(2026, 10, 31)), expected)

    def test_missing_or_duplicate_line_fails(self):
        for source in ("no line", "[ UPPER / BIPPER ]  x\n[ UPPER / BIPPER ]  y"):
            with self.assertRaises(ValueError):
                update(source, date(2026, 10, 31))


if __name__ == "__main__":
    unittest.main()

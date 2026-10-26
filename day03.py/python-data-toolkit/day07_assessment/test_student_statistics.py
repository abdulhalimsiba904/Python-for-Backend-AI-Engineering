"""Run with: python -m unittest discover -s day07_assessment -v."""

import unittest

from student_statistics import calculate_statistics


class StatisticsTests(unittest.TestCase):
    def test_normal_scores(self):
        self.assertEqual(calculate_statistics([85, 72, 49, 90, 65, 38, 77]), {
            "total": 476, "average": 68.0, "highest": 90, "lowest": 38,
            "count": 7, "passed": 5, "failed": 2,
        })

    def test_empty_scores(self):
        self.assertEqual(calculate_statistics([]), {
            "total": 0, "average": None, "highest": None, "lowest": None,
            "count": 0, "passed": 0, "failed": 0,
        })

    def test_single_score_at_pass_boundary(self):
        self.assertEqual(calculate_statistics([50]), {
            "total": 50, "average": 50.0, "highest": 50, "lowest": 50,
            "count": 1, "passed": 1, "failed": 0,
        })

    def test_all_pass(self):
        self.assertEqual(calculate_statistics([50, 75, 100]), {
            "total": 225, "average": 75.0, "highest": 100, "lowest": 50,
            "count": 3, "passed": 3, "failed": 0,
        })

    def test_all_fail_including_zero(self):
        self.assertEqual(calculate_statistics([0, 25, 49]), {
            "total": 74, "average": 24.67, "highest": 49, "lowest": 0,
            "count": 3, "passed": 0, "failed": 3,
        })

    def test_decimal_scores_around_boundary(self):
        self.assertEqual(calculate_statistics([49.99, 50.0, 50.01]), {
            "total": 150.0, "average": 50.0, "highest": 50.01,
            "lowest": 49.99, "count": 3, "passed": 2, "failed": 1,
        })

    def test_average_rounding(self):
        self.assertEqual(calculate_statistics([1, 2, 2])["average"], 1.67)

    def test_repeated_scores(self):
        self.assertEqual(calculate_statistics([60, 60, 60]), {
            "total": 180, "average": 60.0, "highest": 60, "lowest": 60,
            "count": 3, "passed": 3, "failed": 0,
        })

    def test_input_is_unchanged(self):
        scores = [90, 0, 50, 49]
        calculate_statistics(scores)
        self.assertEqual(scores, [90, 0, 50, 49])


if __name__ == "__main__":
    unittest.main()

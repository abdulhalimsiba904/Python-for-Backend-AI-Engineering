"""Tests for the Mobile Money Transaction Analyzer."""

from copy import deepcopy
import unittest

from transaction_analyzer import count_transactions_by_category


class TransactionAnalyzerTests(unittest.TestCase):
    def test_sample_categories(self):
        transactions = [{"category": category} for category in
                        ["Food", "Transport", "food", "Bills", " transport ", "FOOD"]]
        self.assertEqual(count_transactions_by_category(transactions),
                         {"food": 3, "transport": 2, "bills": 1})

    def test_empty_list(self):
        self.assertEqual(count_transactions_by_category([]), {})

    def test_single_category(self):
        self.assertEqual(count_transactions_by_category([{"category": "Airtime"}]),
                         {"airtime": 1})

    def test_skips_missing_categories(self):
        self.assertEqual(count_transactions_by_category([{}, {"amount": 10}]), {})

    def test_skips_empty_and_whitespace_categories(self):
        transactions = [{"category": category} for category in ["", " ", "\t\n\r"]]
        self.assertEqual(count_transactions_by_category(transactions), {})

    def test_skips_none_and_non_string_categories(self):
        for category in [None, 0, 12, 1.5, True, False, [], {}, ["food"]]:
            with self.subTest(category=category):
                self.assertEqual(count_transactions_by_category(
                    [{"category": category}, {"category": "Bills"}]), {"bills": 1})

    def test_strips_tabs_and_newlines(self):
        self.assertEqual(count_transactions_by_category(
            [{"category": "\t Food\n"}, {"category": "food"}]), {"food": 2})

    def test_preserves_internal_spaces_and_supports_new_categories(self):
        transactions = [{"category": category} for category in
                        [" School Fees ", "SCHOOL FEES", "school  fees", "Savings"]]
        self.assertEqual(count_transactions_by_category(transactions),
                         {"school fees": 2, "school  fees": 1, "savings": 1})

    def test_mixed_valid_and_invalid_categories(self):
        transactions = [{}, {"category": None}, {"category": "Food", "amount": 0},
                        {"category": " "}, {"category": 5}, {"category": "FOOD"}]
        self.assertEqual(count_transactions_by_category(transactions), {"food": 2})

    def test_does_not_change_input(self):
        transactions = [{"category": " Food ", "amount": 20}, {}, {"category": [1]}]
        original = deepcopy(transactions)
        count_transactions_by_category(transactions)
        self.assertEqual(transactions, original)

    def test_calls_have_independent_counts(self):
        self.assertEqual(count_transactions_by_category([{"category": "Food"}]),
                         {"food": 1})
        self.assertEqual(count_transactions_by_category([{"category": "Bills"}]),
                         {"bills": 1})


if __name__ == "__main__":
    unittest.main()

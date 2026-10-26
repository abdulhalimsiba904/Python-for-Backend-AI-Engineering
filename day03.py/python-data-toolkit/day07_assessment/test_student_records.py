"""Tests for the Safe JSON File Reader using real temporary files."""

import json
from pathlib import Path
import tempfile
import unittest

from student_records import load_student_records


class StudentRecordsTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "records.json"

    def write_json_text(self, text):
        self.path.write_text(text, encoding="utf-8")

    def test_sample_students(self):
        path = Path(__file__).with_name("students.json")
        self.assertEqual(load_student_records(str(path)), [
            {"student_id": "UDS001", "name": "Amina", "score": 85},
            {"student_id": "UDS002", "name": "Musa", "score": 72},
            {"student_id": "UDS003", "name": "Fatima", "score": 91},
        ])

    def test_empty_list(self):
        self.write_json_text("[]")
        self.assertEqual(load_student_records(self.path), [])

    def test_list_contents_are_preserved(self):
        self.write_json_text('[null, true, 0, "Fatima", {"name": "Aminé"}, []]')
        self.assertEqual(load_student_records(self.path),
                         [None, True, 0, "Fatima", {"name": "Aminé"}, []])

    def test_missing_file_has_chained_cause(self):
        with self.assertRaisesRegex(ValueError, "not found") as caught:
            load_student_records(self.path)
        self.assertIsInstance(caught.exception.__cause__, FileNotFoundError)
        self.assertIn(str(self.path), str(caught.exception))

    def test_malformed_fixture_has_chained_cause(self):
        with self.assertRaisesRegex(ValueError, "Invalid JSON") as caught:
            load_student_records(Path(__file__).with_name("invalid_students.json"))
        self.assertIsInstance(caught.exception.__cause__, json.JSONDecodeError)

    def test_empty_file_is_invalid_json(self):
        self.write_json_text("")
        with self.assertRaisesRegex(ValueError, "Invalid JSON") as caught:
            load_student_records(self.path)
        self.assertIsInstance(caught.exception.__cause__, json.JSONDecodeError)

    def test_object_fixture_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "top-level.*list") as caught:
            load_student_records(Path(__file__).with_name("wrong_structure.json"))
        self.assertIsNone(caught.exception.__cause__)

    def test_other_non_list_values_are_rejected(self):
        for text in ['"students"', '42', 'true', 'false', 'null']:
            with self.subTest(text=text):
                self.write_json_text(text)
                with self.assertRaisesRegex(ValueError, "top-level.*list"):
                    load_student_records(self.path)


if __name__ == "__main__":
    unittest.main()

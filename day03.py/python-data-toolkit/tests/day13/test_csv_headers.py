"""Regression coverage for ambiguous CSV headers and safe CLI failures."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from data_toolkit.application import accepted_records
from data_toolkit.readers import read_csv

ROOT = Path(__file__).resolve().parents[2]


class CSVHeaderTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix='day13-headers-')
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        self.source = self.folder/'input.csv'

    def test_duplicate_header_is_rejected_without_altering_source(self) -> None:
        self.source.write_text('id,amount,amount,category\nT1,-100,25,food\n', encoding='utf-8')
        before = self.source.read_bytes()
        with self.assertRaisesRegex(ValueError, 'duplicate field names'):
            read_csv(self.source)
        self.assertEqual(self.source.read_bytes(), before)

    def test_cli_never_publishes_report_from_duplicate_headers(self) -> None:
        self.source.write_text('id,amount,amount,category\nPRIVATE-ID,-100,25,food\n',
                               encoding='utf-8')
        before = self.source.read_bytes()
        output = self.folder/'report.txt'
        environment = dict(os.environ)
        for name in ['GROQ_API_KEY', 'GROQ_MODEL', 'OPENAI_API_KEY', 'OPENAI_MODEL']:
            environment.pop(name, None)
        environment['PYTHONPATH'] = str(ROOT/'src')
        result = subprocess.run(
            [sys.executable, '-m', 'data_toolkit.cli', 'report', str(self.source),
             '--output', str(output)], cwd=ROOT, env=environment,
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '')
        self.assertIn('duplicate field names', result.stderr)
        self.assertNotIn('PRIVATE-ID', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertFalse(output.exists())
        self.assertEqual(list(self.folder.glob('.data-toolkit-*.tmp')), [])
        self.assertEqual(self.source.read_bytes(), before)

    def test_unique_headers_preserve_reader_metadata_and_canonical_contract(self) -> None:
        self.source.write_text('id,amount,category,note\n T1 ,25, Food ,public fixture\n',
                               encoding='utf-8')
        self.assertEqual(read_csv(self.source), [
            {'id': ' T1 ', 'amount': '25', 'category': ' Food ', 'note': 'public fixture'}])
        self.assertEqual(accepted_records(self.source), [
            {'transaction_id': 'T1', 'amount': 25.0, 'category': 'food'}])


if __name__ == '__main__':
    unittest.main()

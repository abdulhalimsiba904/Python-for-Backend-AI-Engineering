"""Offline integration tests across the public CLI and real file-processing modules."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from data_toolkit.application import accepted_records, load_records, render_report

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VALID_CSV = (
    'id,amount,category\n'
    ' A1 ,10.25, Food  Shop \n'
    'A2,20.75,food shop\n'
    'A3,9,Travel\n'
    'A4,40, travel \n'
)
EXPECTED_REPORT = (
    'Python Data Toolkit Report\n'
    'Count: 4\n'
    'Total: 80.00\n'
    'Average (2 decimals): 20.0\n'
    'Minimum: 9.0\n'
    'Maximum: 40.0\n'
    'Categories:\n'
    '  food shop: count=2, total=31.00\n'
    '  travel: count=2, total=49.00\n'
)


class ReportingWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix='toolkit-day12-')
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.source = self.folder / 'input records.csv'
        self.source.write_text(VALID_CSV, encoding='utf-8')
        self.original_source = self.source.read_bytes()

    def run_cli(self, *arguments: str | Path) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        for name in ('GROQ_API_KEY', 'GROQ_MODEL', 'OPENAI_API_KEY', 'OPENAI_MODEL'):
            environment.pop(name, None)
        environment['PYTHONPATH'] = str(PROJECT_ROOT / 'src')
        environment['PYTHONDONTWRITEBYTECODE'] = '1'
        return subprocess.run(
            [sys.executable, '-m', 'data_toolkit.cli', *map(str, arguments)],
            cwd=PROJECT_ROOT, env=environment, capture_output=True,
            text=True, encoding='utf-8', timeout=30,
        )

    def assert_source_unchanged(self) -> None:
        self.assertEqual(self.source.read_bytes(), self.original_source)

    def assert_no_temporary_exports(self) -> None:
        self.assertEqual(list(self.folder.rglob('.data-toolkit-*.tmp')), [])

    def test_csv_to_report_and_analysis(self) -> None:
        loaded = load_records(self.source)
        self.assertEqual(len(loaded), 4)
        self.assertEqual([row['amount'] for row in loaded], [10.25, 20.75, 9.0, 40.0])
        self.assertTrue(all(type(row['amount']) is float for row in loaded))
        records = accepted_records(self.source)
        self.assertEqual(records, [
            {'transaction_id': 'A1', 'amount': 10.25, 'category': 'food shop'},
            {'transaction_id': 'A2', 'amount': 20.75, 'category': 'food shop'},
            {'transaction_id': 'A3', 'amount': 9.0, 'category': 'travel'},
            {'transaction_id': 'A4', 'amount': 40.0, 'category': 'travel'},
        ])
        analysis = self.run_cli('analyze', self.source)
        self.assertEqual(analysis.returncode, 0, analysis.stderr)
        self.assertEqual(analysis.stderr, '')
        self.assertEqual(json.loads(analysis.stdout), {
            'count': 4, 'total': 80.0, 'average': 20.0,
            'minimum': 9.0, 'maximum': 40.0,
            'by_category': {'food shop': {'count': 2, 'total': 31.0},
                            'travel': {'count': 2, 'total': 49.0}},
        })
        destination = self.folder / 'export folder' / 'report.txt'
        # Explicit overwrite permission exercises the replace publication path.
        # Default no-overwrite hard-link publication is covered by Day 10 tests.
        report = self.run_cli('report', self.source, '--output', destination, '--force')
        self.assertEqual(report.returncode, 0, report.stderr)
        self.assertEqual(report.stderr, '')
        self.assertEqual(json.loads(report.stdout), {'written': str(destination), 'count': 4})
        self.assertTrue(destination.is_file())
        self.assertEqual(destination.read_text(encoding='utf-8'), EXPECTED_REPORT)
        self.assertEqual(render_report(records), EXPECTED_REPORT)
        self.assert_source_unchanged()
        self.assert_no_temporary_exports()

    def test_invalid_csv_does_not_publish_a_report(self) -> None:
        self.source.write_text(
            'id,amount,category\nGOOD,12,food\nPRIVATE-ID,not-money,travel\n',
            encoding='utf-8',
        )
        self.original_source = self.source.read_bytes()
        destination = self.folder / 'new directory' / 'report.txt'
        result = self.run_cli('report', self.source, '--output', destination)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '')
        self.assertIn('Row 2', result.stderr)
        self.assertIn('amount', result.stderr)
        self.assertNotIn('PRIVATE-ID', result.stderr)
        self.assertNotIn('not-money', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertFalse(destination.exists())
        self.assertFalse(destination.parent.exists())
        self.assert_source_unchanged()
        self.assert_no_temporary_exports()

    def test_invalid_csv_cannot_replace_an_existing_report_even_with_force(self) -> None:
        self.source.write_text('id,amount,category\nBAD,-1,food\n', encoding='utf-8')
        self.original_source = self.source.read_bytes()
        destination = self.folder / 'report.txt'
        destination.write_bytes(b'KEEP THIS REPORT')
        result = self.run_cli('report', self.source, '--output', destination, '--force')
        self.assertEqual(result.returncode, 1)
        self.assertIn('positive and finite', result.stderr)
        self.assertEqual(result.stdout, '')
        self.assertEqual(destination.read_bytes(), b'KEEP THIS REPORT')
        self.assert_source_unchanged()
        self.assert_no_temporary_exports()

    def test_duplicate_csv_ids_fail_after_trimming(self) -> None:
        self.source.write_text('id,amount,category\n A1 ,1,food\nA1,2,travel\n', encoding='utf-8')
        self.original_source = self.source.read_bytes()
        destination = self.folder / 'report.txt'
        result = self.run_cli('report', self.source, '--output', destination)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Row 2', result.stderr)
        self.assertIn('duplicate ID', result.stderr)
        self.assertFalse(destination.exists())
        self.assert_source_unchanged()
        self.assert_no_temporary_exports()

    def test_report_requires_explicit_overwrite_permission(self) -> None:
        destination = self.folder / 'report.txt'
        destination.write_bytes(b'EXISTING REPORT')
        denied = self.run_cli('report', self.source, '--output', destination)
        self.assertEqual(denied.returncode, 1)
        self.assertIn('--force', denied.stderr)
        self.assertEqual(denied.stdout, '')
        self.assertEqual(destination.read_bytes(), b'EXISTING REPORT')
        self.assert_no_temporary_exports()
        allowed = self.run_cli('report', self.source, '--output', destination, '--force')
        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        self.assertEqual(destination.read_text(encoding='utf-8'), EXPECTED_REPORT)
        self.assert_source_unchanged()
        self.assert_no_temporary_exports()

    def test_converted_json_cannot_be_its_own_output(self) -> None:
        canonical = self.folder / 'canonical.json'
        converted = self.run_cli('convert', self.source, '--output', canonical, '--force')
        self.assertEqual(converted.returncode, 0, converted.stderr)
        before = canonical.read_bytes()
        result = self.run_cli('convert', canonical, '--output', canonical, '--force')
        self.assertEqual(result.returncode, 1)
        self.assertIn('Output must differ from input', result.stderr)
        self.assertEqual(result.stdout, '')
        self.assertEqual(canonical.read_bytes(), before)
        self.assert_source_unchanged()
        self.assert_no_temporary_exports()

    def test_empty_csv_batch_keeps_report_contract(self) -> None:
        self.source.write_text('id,amount,category\n', encoding='utf-8')
        self.original_source = self.source.read_bytes()
        destination = self.folder / 'report.txt'
        result = self.run_cli('report', self.source, '--output', destination, '--force')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(destination.read_text(encoding='utf-8'),
                         'Python Data Toolkit Report\nCount: 0\nTotal: 0.00\n'
                         'Average (2 decimals): N/A\nMinimum: None\nMaximum: None\nCategories:\n')
        self.assert_source_unchanged()
        self.assert_no_temporary_exports()

    def test_report_retains_legacy_rounding(self) -> None:
        self.source.write_text('id,amount,category\nA1,0.1,food\nA2,0.2,food\n', encoding='utf-8')
        self.original_source = self.source.read_bytes()
        destination = self.folder / 'report.txt'
        result = self.run_cli('report', self.source, '--output', destination, '--force')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(destination.read_text(encoding='utf-8'),
                         'Python Data Toolkit Report\nCount: 2\nTotal: 0.30\n'
                         'Average (2 decimals): 0.15\nMinimum: 0.1\nMaximum: 0.2\n'
                         'Categories:\n  food: count=2, total=0.30\n')
        self.assert_source_unchanged()
        self.assert_no_temporary_exports()


if __name__ == '__main__':
    unittest.main()

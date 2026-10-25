"""DocumentRecord behavior checks using functions and plain assertions."""
from data_toolkit.models import DocumentRecord


def expect_error(error_type, operation) -> None:
    """Assert that an operation raises the expected exception type."""
    try:
        operation()
    except error_type:
        return
    raise AssertionError(f"Expected {error_type.__name__}")


def test_initial_attributes() -> None:
    record = DocumentRecord(" DOC-001 ", " transactions.json ", " JSON ")
    assert record.identifier == "DOC-001"
    assert record.filename == "transactions.json"
    assert record.document_type == "json"
    assert record.processing_status == "pending"
    assert record.validation_errors == []
    assert record.is_valid() is True


def test_supported_document_types_and_initial_statuses() -> None:
    for document_type in ("pdf", "csv", "json", "txt"):
        record = DocumentRecord("DOC-001", "input", document_type)
        assert record.document_type == document_type
    for status in ("pending", "processing", "completed", "failed"):
        record = DocumentRecord("DOC-001", "input.json", "json", status)
        assert record.processing_status == status
        assert record.is_valid() is (status != "failed")


def test_instances_have_independent_state() -> None:
    first = DocumentRecord("DOC-001", "first.json", "json")
    second = DocumentRecord("DOC-002", "second.csv", "csv")
    first.add_validation_error("Missing amount.")
    assert first.validation_errors == ["Missing amount."]
    assert second.validation_errors == []
    assert first.processing_status == "failed"
    assert second.processing_status == "pending"


def test_successful_status_transitions() -> None:
    record = DocumentRecord("DOC-001", "input.json", "json")
    assert record.mark_processing() is None
    assert record.processing_status == "processing"
    assert record.mark_completed() is None
    assert record.processing_status == "completed"
    assert record.is_valid() is True


def test_completion_requires_processing() -> None:
    record = DocumentRecord("DOC-001", "input.json", "json")
    expect_error(ValueError, record.mark_completed)
    assert record.processing_status == "pending"


def test_validation_errors_prevent_success() -> None:
    record = DocumentRecord("DOC-001", "input.json", "json")
    record.mark_processing()
    record.add_validation_error(" Missing category. ")
    assert record.validation_errors == ["Missing category."]
    assert record.processing_status == "failed"
    assert record.is_valid() is False
    expect_error(ValueError, record.mark_completed)
    expect_error(ValueError, record.mark_processing)
    assert record.processing_status == "failed"


def test_mark_failed_records_reason() -> None:
    record = DocumentRecord("DOC-001", "input.json", "json")
    record.mark_processing()
    record.mark_failed("Unable to read the file.")
    record.add_validation_error("Processing did not finish.")
    assert record.processing_status == "failed"
    assert record.validation_errors == [
        "Unable to read the file.", "Processing did not finish."
    ]


def test_invalid_identifiers() -> None:
    for identifier in ("", "   "):
        expect_error(ValueError, lambda: DocumentRecord(identifier, "input.json", "json"))
    for identifier in (None, 123, True):
        expect_error(TypeError, lambda: DocumentRecord(identifier, "input.json", "json"))


def test_invalid_filenames() -> None:
    for filename in ("", " \t "):
        expect_error(ValueError, lambda: DocumentRecord("DOC-001", filename, "json"))
    for filename in (None, 123):
        expect_error(TypeError, lambda: DocumentRecord("DOC-001", filename, "json"))


def test_invalid_document_types() -> None:
    for document_type in ("", " ", "exe", "xml"):
        expect_error(ValueError, lambda: DocumentRecord("DOC-001", "input", document_type))
    expect_error(TypeError, lambda: DocumentRecord("DOC-001", "input", None))


def test_invalid_processing_statuses() -> None:
    for status in ("", "done", "PROCESSING", "unknown"):
        expect_error(ValueError, lambda: DocumentRecord("DOC-001", "input.json", "json", status))
    expect_error(TypeError, lambda: DocumentRecord("DOC-001", "input.json", "json", 123))
    record = DocumentRecord("DOC-001", "input.json", "json")
    expect_error(AttributeError, lambda: setattr(record, "processing_status", "unknown"))
    assert record.processing_status == "pending"


def test_invalid_error_messages_do_not_change_state() -> None:
    for method_name in ("mark_failed", "add_validation_error"):
        record = DocumentRecord("DOC-001", "input.json", "json")
        method = getattr(record, method_name)
        for message in ("", "   "):
            expect_error(ValueError, lambda: method(message))
        for message in (None, 123):
            expect_error(TypeError, lambda: method(message))
        assert record.processing_status == "pending"
        assert record.validation_errors == []


def test_terminal_records_require_a_new_attempt() -> None:
    record = DocumentRecord("DOC-001", "input.json", "json")
    record.mark_processing()
    expect_error(ValueError, record.mark_processing)
    record.mark_completed()
    expect_error(ValueError, record.mark_processing)
    expect_error(ValueError, record.mark_completed)
    # A later discovered problem invalidates a previously completed record.
    record.add_validation_error("A problem was found afterward.")
    assert record.processing_status == "failed"
    record.validation_errors.clear()
    assert record.is_valid() is False
    expect_error(ValueError, record.mark_processing)


def test_summary_does_not_include_error_contents() -> None:
    record = DocumentRecord("DOC-001", "input.json", "json")
    assert record.get_summary() == "DOC-001 | input.json | JSON | pending | errors: 0"
    record.mark_failed("PRIVATE-CONTENT")
    summary = record.get_summary()
    assert summary == "DOC-001 | input.json | JSON | failed | errors: 1"
    assert "PRIVATE-CONTENT" not in summary

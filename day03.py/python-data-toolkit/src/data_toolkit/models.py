"""Simple document metadata and processing state for the Day 6 practical."""


def _required_text(value: str, field_name: str) -> str:
    """Return trimmed required text without echoing invalid input."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    if not value.strip():
        raise ValueError(f"{field_name} must not be blank.")
    return value.strip()


class DocumentRecord:
    """Keep one document's metadata, status, and validation errors together.

    Identifiers are supplied by the caller, which manages their uniqueness.
    A record represents one attempt; create a new record to retry a failure.
    PDF and TXT are supported metadata types, not new transaction readers.
    """

    def __init__(
        self,
        identifier: str,
        filename: str,
        document_type: str,
        processing_status: str = "pending",
    ) -> None:
        """Validate metadata and create a separate error list per instance."""
        self.identifier = _required_text(identifier, "identifier")
        self.filename = _required_text(filename, "filename")
        self.document_type = _required_text(document_type, "document_type").lower()
        if self.document_type not in {"pdf", "csv", "json", "txt"}:
            raise ValueError("Supported document types are pdf, csv, json, and txt.")
        if not isinstance(processing_status, str):
            raise TypeError("processing_status must be a string.")
        if processing_status not in {"pending", "processing", "completed", "failed"}:
            raise ValueError("Status must be pending, processing, completed, or failed.")
        self._processing_status = processing_status
        self.validation_errors: list[str] = []

    @property
    def processing_status(self) -> str:
        """Read status; use the named methods to change it safely."""
        return self._processing_status

    def mark_processing(self) -> None:
        """Start a pending, valid record; reject duplicate or retried starts."""
        if self._processing_status != "pending" or not self.is_valid():
            raise ValueError("Only a pending document without errors can start.")
        self._processing_status = "processing"

    def mark_completed(self) -> None:
        """Complete a processing record only when it has no errors."""
        if self._processing_status != "processing" or not self.is_valid():
            raise ValueError("Only a processing document without errors can complete.")
        self._processing_status = "completed"

    def mark_failed(self, error_message: str) -> None:
        """Record a safe failure reason and mark this attempt failed."""
        self.add_validation_error(error_message)

    def add_validation_error(self, error_message: str) -> None:
        """Append a nonblank error and invalidate even a completed record."""
        message = _required_text(error_message, "error_message")
        self.validation_errors.append(message)
        self._processing_status = "failed"

    def is_valid(self) -> bool:
        """Return whether no errors or failure have been recorded.

        This does not read a file or validate its contents. A pending record
        can be valid without having been processed yet.
        """
        return not self.validation_errors and self._processing_status != "failed"

    def get_summary(self) -> str:
        """Return display metadata and an error count, not error contents."""
        return (
            f"{self.identifier} | {self.filename} | {self.document_type.upper()} | "
            f"{self.processing_status} | errors: {len(self.validation_errors)}"
        )

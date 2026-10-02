class NotFoundError(LookupError):
    """A requested patient, practitioner or appointment does not exist."""


class BookingConflictError(ValueError):
    """The practitioner already has a SCHEDULED appointment at that time."""
